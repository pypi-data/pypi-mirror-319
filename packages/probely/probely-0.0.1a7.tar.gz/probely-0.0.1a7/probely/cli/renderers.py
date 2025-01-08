import argparse
import json
import sys
import textwrap
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Type, Union

import yaml
from dateutil import parser
from rich.console import Console

from probely.cli.enums import OutputEnum
from probely.cli.tables.base_table import BaseOutputTable
from probely.constants import TARGET_NEVER_SCANNED_OUTPUT, UNKNOWN_VALUE_OUTPUT
from probely.sdk.enums import ProbelyCLIEnum
from probely.sdk.models import SdkBaseModel, Target
from probely.sdk.schemas import FindingLabelDataModel, TargetLabelDataModel
from probely.settings import CLI_DEFAULT_OUTPUT_FORMAT


class OutputRenderer:
    """
    Class responsible for rendering output in various formats (JSON, YAML, TABLE, IDS).
    """

    def __init__(
        self,
        records: Iterable[
            Union[Dict, SdkBaseModel]
        ],  # NOTE: after ending SDK refactor, we will use only SdkBaseModel
        command_args: argparse.Namespace,
        table_cls: Optional[Type[BaseOutputTable]] = None,
    ):
        self.records = records
        self.table_cls = table_cls

        self.console = command_args.console

        default_output_format = OutputEnum[CLI_DEFAULT_OUTPUT_FORMAT]
        output_format = (
            OutputEnum[command_args.output_format]
            if command_args.output_format
            else default_output_format
        )
        self.output_type = output_format

    def render(self) -> None:
        if self.output_type == OutputEnum.JSON:
            self._render_json()
        elif self.output_type == OutputEnum.YAML:
            self._render_yaml()
        elif self.output_type == OutputEnum.IDS_ONLY:
            self._render_ids_only()
        else:
            self._render_table()

    def _render_ids_only(self) -> None:
        for record in self.records:
            if isinstance(
                record, dict
            ):  # NOTE: temporary solution while transitioning to OOP approach
                self.console.print(record["id"])
            else:
                self.console.print(record.id)

    def _render_json(self) -> None:
        self.console.print("[")
        first = True
        for record in self.records:
            if not first:
                self.console.print(",")

            if hasattr(record, "to_json"):
                # NOTE: just temporary solution while we finish SDK refactor and start using OOP approach everywhere
                self.console.print(record.to_json(indent=2))
            else:
                self.console.print(json.dumps(record, indent=2))
            first = False
        self.console.print("]")

    def _render_yaml(self) -> None:
        for record in self.records:
            if hasattr(record, "to_dict"):
                record = record.to_dict(mode="json")
            self.console.print(yaml.dump([record], indent=2, width=sys.maxsize))

    def _render_table(self) -> None:
        table = self.table_cls.create_table(show_header=True)
        self.console.print(table)

        for record in self.records:
            table = self.table_cls.create_table(show_header=False)
            self.table_cls.add_row(table, record)
            self.console.print(table)


def get_printable_enum_value(enum: Type[ProbelyCLIEnum], api_enum_value: str) -> str:
    try:
        value_name: str = enum.get_by_api_response_value(api_enum_value).name
        return value_name
    except ValueError:
        return UNKNOWN_VALUE_OUTPUT  # TODO: scenario that risk enum updated but CLI is forgotten


def get_printable_labels(
    labels: List[Union[TargetLabelDataModel, FindingLabelDataModel]] = None
) -> str:
    if labels is None:
        return "UNKNOWN_LABELS"

    labels_names = []
    try:
        for label in labels:
            truncated_label = textwrap.shorten(label.name, width=16, placeholder="...")
            labels_names.append(truncated_label)
    except:
        return "UNKNOWN_LABELS"

    printable_labels = ", ".join(labels_names)

    return printable_labels


def get_printable_date(
    date_input: Union[str, datetime, None],
    default_string: Union[str, None] = None,
) -> str:
    if isinstance(date_input, str):
        date_obj = parser.isoparse(date_input)
    elif isinstance(date_input, datetime):
        date_obj = date_input
    else:
        date_obj = None

    if date_obj:
        return date_obj.strftime("%Y-%m-%d %H:%M")

    if default_string:
        return default_string

    return ""


def get_printable_last_scan_date(target: Target) -> str:
    if not target.last_scan:
        return TARGET_NEVER_SCANNED_OUTPUT

    return get_printable_date(target.last_scan.started, TARGET_NEVER_SCANNED_OUTPUT)
