import argparse
from typing import Generator, List

from probely.cli.commands.findings.schemas import FindingsApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.cli.renderers import OutputRenderer
from probely.cli.tables.finding_table import FindingTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.managers import FindingManager
from probely.sdk.models import Finding


def findings_get_command_handler(args: argparse.Namespace):
    filters = prepare_filters_for_api(FindingsApiFiltersSchema, args)

    findings_ids = args.findings_ids

    if filters and args.findings_ids:
        raise ProbelyCLIValidation("filters and Finding IDs are mutually exclusive.")

    if args.findings_ids:
        findings: Generator[Finding] = FindingManager().retrieve_multiple(findings_ids)
    else:
        findings: Generator[Finding] = FindingManager().list(filters=filters)

    renderer = OutputRenderer(
        records=findings,
        table_cls=FindingTable,
        command_args=args,
    )
    renderer.render()
