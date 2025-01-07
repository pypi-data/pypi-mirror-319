import argparse
import asyncio
import json
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse, urlunparse

import socketio
import structlog

import rasa.cli.utils
import rasa.shared.utils.cli
from rasa.studio.auth import KeycloakToken, KeycloakTokenReader
from rasa.studio.config import StudioConfig
from rasa_sdk.executor import ActionExecutor, ActionMissingDomainException

from rasa.studio.upload import is_auth_working

structlogger = structlog.get_logger()


def handle_actions(args: argparse.Namespace) -> None:
    assistant_name = args.assistant_name[0]
    studio_config = StudioConfig.read_config()
    endpoint = studio_config.studio_url
    verify = not studio_config.disable_verify

    if not endpoint:
        rasa.shared.utils.cli.print_error_and_exit(
            "No GraphQL endpoint found in config. Please run `rasa studio config`."
        )

    executor = load_executor(args.actions)

    parsed_url = urlparse(endpoint)
    websocket_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))

    if not is_auth_working(endpoint, verify):
        rasa.shared.utils.cli.print_error_and_exit(
            "Authentication is invalid or expired. Please run `rasa studio login`."
        )
        return

    asyncio.run(open_webhook(websocket_url, assistant_name, executor))


def auth_header(token: KeycloakToken) -> Dict[str, Any]:
    return {"Authorization": f"{token.token_type} {token.access_token}"}


def parse_webhook(plaintext: str) -> Dict[str, Any]:
    request = json.loads(plaintext)
    structlogger.debug("reverse.proxy.webhook.parse", request=request)
    return request


async def open_webhook(
    endpoint: str, assistant_name: str, executor: ActionExecutor
) -> Tuple[str, bool]:
    """Makes a request to the studio endpoint to upload data.

    Args:
        endpoint: The studio endpoint
        assistant_name: The name of the assistant
        executor: The action executor
    """
    token = KeycloakTokenReader().get_token()

    sio = socketio.AsyncClient(reconnection=True)
    headers = auth_header(token)

    @sio.on("message")
    async def handle_action_call(data: Optional[Dict[str, Any]]):
        structlogger.debug("reverse.proxy.webhook.handle_action_call")
        if not data:
            structlogger.error(
                "reverse.proxy.webhook.handle_action_call.invalid_request", data=data
            )
            status = 400
            response = {"error": "Invalid request, missing body."}
        else:
            status, response = await trigger_action(data, executor, auto_reload=True)
        return {"response": response, "status": status}

    @sio.on("disconnect")
    async def disconnect():
        structlogger.info(
            "reverse.proxy.webhook.handle_disconnect",
            event_info=(
                "Disconnected from the server, this "
                "can happen if the server is either unavailable "
                "or if the authentication token has expired."
            ),
        )

    await sio.connect(
        endpoint + "?assistantName=" + assistant_name,
        socketio_path="/api/v1/websocket-actions",
        headers=headers,
    )

    rasa.shared.utils.cli.print_success("Started action server, waiting for requests")
    await sio.wait()


def load_executor(action_package_name: str) -> ActionExecutor:
    executor = ActionExecutor()
    executor.register_package(action_package_name)
    return executor


async def trigger_action(
    action_call: Dict[str, Any], executor: ActionExecutor, auto_reload: bool = False
) -> Tuple[int, Dict[str, Any]]:
    from rasa_sdk import utils
    from rasa_sdk.interfaces import ActionExecutionRejection, ActionNotFoundException

    utils.check_version_compatibility(action_call.get("version"))

    if auto_reload:
        executor.reload()
    try:
        result = await executor.run(action_call)
        return 200, result.model_dump() if result else None
    except ActionExecutionRejection as e:
        structlogger.debug(
            "reverse.proxy.webhook.trigger_action.rejection",
            error=e.message,
            action_name=e.action_name,
        )
        body = {"error": e.message, "action_name": e.action_name}
        return 404, body
    except ActionMissingDomainException as e:
        structlogger.debug(
            "reverse.proxy.webhook.trigger_action.missing_domain",
            error=e.message,
            action_name=e.action_name,
        )
        body = {"error": e.message, "action_name": e.action_name}
        return 449, body
    except ActionNotFoundException as e:
        structlogger.error(
            "reverse.proxy.webhook.trigger_action.not_found",
            error=e.message,
            action_name=e.action_name,
        )
        body = {"error": e.message, "action_name": e.action_name}
        return 404, body
