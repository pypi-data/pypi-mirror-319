import argparse
import logging
from typing import Dict

from probely.cli.common import validate_and_retrieve_yaml_content
from probely.cli.renderers import OutputRenderer
from probely.cli.tables.extra_hosts_table import ExtraHostTable
from probely.sdk.managers import ExtraHostManager
from probely.sdk.models import ExtraHost

logger = logging.getLogger(__name__)


def generate_payload_from_args(args: argparse.Namespace) -> Dict:
    """
    Generate payload for creating an Extra Host by prioritizing command line arguments
    and using file input as a fallback.
    """
    yaml_file_path = args.yaml_file_path
    file_content = validate_and_retrieve_yaml_content(yaml_file_path)

    command_arguments = {
        "target_id": args.target_id,
        "host": args.host or file_content.get("host"),
        "include": args.include or file_content.get("include"),
        "name": args.name or file_content.get("name"),
        "desc": args.desc or file_content.get("desc"),
        "file_input": file_content,
    }

    return command_arguments


def extra_hosts_add_command_handler(args: argparse.Namespace):
    payload = generate_payload_from_args(args)

    logger.debug("extra-host `add` extra_payload: {}".format(payload["file_input"]))

    extra_host: ExtraHost = ExtraHostManager().create(
        target_id=payload["target_id"],
        host=payload["host"],
        include=payload["include"],
        name=payload["name"],
        desc=payload["desc"],
        extra_payload=payload["file_input"],
    )

    renderer = OutputRenderer(
        records=[extra_host],
        table_cls=ExtraHostTable,
        command_args=args,
    )
    renderer.render()
