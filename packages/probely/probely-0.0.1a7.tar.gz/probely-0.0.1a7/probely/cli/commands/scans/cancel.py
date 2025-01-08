import logging
from typing import Generator, List

from probely.cli.commands.scans.schemas import ScanApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.cli.renderers import OutputRenderer
from probely.cli.tables.scan_table import ScanTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.managers import ScanManager
from probely.sdk.models import Scan

logger = logging.getLogger(__name__)


def scans_cancel_command_handler(args):
    scan_ids = args.scan_ids
    filters = prepare_filters_for_api(ScanApiFiltersSchema, args)

    if not scan_ids and not filters:
        raise ProbelyCLIValidation("Expected scan_ids or filters")

    if filters and scan_ids:
        raise ProbelyCLIValidation("Filters and Scan IDs are mutually exclusive")

    if filters:
        scans = ScanManager().list(filters=filters)
        searched_scan_ids = [scan.id for scan in scans]

        if not searched_scan_ids:
            raise ProbelyCLIValidation("Selected Filters returned no results")

        scan_ids = searched_scan_ids

    logger.debug("Cancelling scan for scan ids: {}".format(scan_ids))

    if len(scan_ids) == 1:
        scan = ScanManager().cancel(scan_ids[0])
        canceled_scans: List[Scan] = [scan]
    else:
        canceled_scans: Generator[Scan] = ScanManager().bulk_cancel(scan_ids)

    renderer = OutputRenderer(
        records=canceled_scans,
        table_cls=ScanTable,
        command_args=args,
    )
    renderer.render()
