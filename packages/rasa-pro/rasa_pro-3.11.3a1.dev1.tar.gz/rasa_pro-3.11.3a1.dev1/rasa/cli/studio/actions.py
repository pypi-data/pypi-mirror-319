import argparse
from typing import List

from rasa.cli import SubParsersAction
from rasa.shared.constants import DEFAULT_ACTIONS_PATH

from rasa.studio.actions import handle_actions
from rasa_sdk.cli.arguments import action_arg


def add_subparser(
    subparsers: SubParsersAction, parents: List[argparse.ArgumentParser]
) -> None:
    """Add the studio actions parser.

    Args:
        subparsers: subparser we are going to attach to
        parents: Parent parsers, needed to ensure tree structure in argparse
    """
    actions_parser = subparsers.add_parser(
        "actions",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help=("Run Rasa actions server locally and connect it to studio."),
    )

    actions_parser.set_defaults(func=handle_actions)

    set_studio_actions_arguments(actions_parser)


def set_studio_actions_arguments(parser: argparse.ArgumentParser) -> None:
    """Add arguments for running `rasa studio download`."""
    parser.add_argument(
        "assistant_name",
        default=None,
        nargs=1,
        type=str,
        help="Name of the assistant on Rasa Studio",
    )

    parser.add_argument(
        "--actions",
        type=action_arg,
        default=DEFAULT_ACTIONS_PATH,
        help="name of action package to be loaded",
    )
