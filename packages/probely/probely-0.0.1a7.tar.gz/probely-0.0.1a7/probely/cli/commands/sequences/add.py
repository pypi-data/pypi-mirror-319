import argparse
import json
import logging
from typing import Dict, List

from probely import Sequence, SequenceManager
from probely.cli.common import validate_and_retrieve_yaml_content
from probely.cli.renderers import OutputRenderer
from probely.cli.tables.sequences_table import SequenceTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.enums import SequenceTypeEnum

logger = logging.getLogger(__name__)


def get_type(args, file_input):
    if args.type:  # should be validated by argparse
        return SequenceTypeEnum[args.type]

    if file_input.get("type", None):
        try:
            sequence_type = SequenceTypeEnum.get_by_api_response_value(
                file_input.get("type")
            )
            return sequence_type
        except ValueError:
            raise ProbelyCLIValidation(
                "sequence type '{}' from file is not a valid option".format(
                    file_input["type"]
                )
            )


def _get_sequence_steps_from_path(args, file_input):
    # We pop because we allow file path on the content where API receives objects
    sequence_steps_file_path = file_input.pop("content", None)

    if args.sequence_steps_file_path:
        sequence_steps_file_path = args.sequence_steps_file_path

    if not sequence_steps_file_path:
        raise ProbelyCLIValidation("'sequence-steps-file' is required")

    with open(sequence_steps_file_path, "r") as f:
        try:
            sequence_steps: List[Dict] = json.load(f)
        except json.decoder.JSONDecodeError:
            raise ProbelyCLIValidation("Provided file has invalid JSON content")

    file_input["content"] = json.dumps(sequence_steps)

    return sequence_steps


def get_command_arguments(args: argparse.Namespace) -> Dict:
    file_input = validate_and_retrieve_yaml_content(args.yaml_file_path)

    command_arguments = {
        "target_id": args.target_id,
        "name": args.name or file_input.get("name"),
        "type": get_type(args, file_input),
        "enabled": args.enabled or file_input.get("enabled"),
        "sequence_steps": _get_sequence_steps_from_path(args, file_input),
        "requires_authentication": args.requires_authentication
        or file_input.get("requires_authentication"),
        "extra_payload": file_input,
    }

    return command_arguments


def sequences_add_command_handler(args: argparse.Namespace):
    command_arguments = get_command_arguments(args)

    logger.debug(
        "sequence add extra_payload: {}".format(command_arguments["extra_payload"])
    )

    if not command_arguments["name"]:
        raise ProbelyCLIValidation("'name' is required")

    sequence: Sequence = SequenceManager().create(
        target_id=command_arguments["target_id"],
        name=command_arguments["name"],
        sequence_steps=command_arguments["sequence_steps"],
        sequence_type=command_arguments["type"],
        enabled=command_arguments["enabled"],
        requires_authentication=command_arguments["requires_authentication"],
        extra_payload=command_arguments["extra_payload"],
    )

    renderer = OutputRenderer(
        records=[sequence],
        table_cls=SequenceTable,
        command_args=args,
    )
    renderer.render()
