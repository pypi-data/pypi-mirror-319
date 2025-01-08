from typing import Generator, List

from probely.cli.commands.targets.schemas import TargetLabelApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.cli.renderers import OutputRenderer
from probely.cli.tables.target_labels import TargetLabelsTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.managers import TargetLabelManager
from probely.sdk.models import TargetLabel


def target_labels_get_command_handler(args):
    """
    Lists all accessible target labels of client
    """
    filters = prepare_filters_for_api(TargetLabelApiFiltersSchema, args)
    target_label_ids = args.target_label_ids

    if filters and target_label_ids:
        raise ProbelyCLIValidation(
            "filters and Target Label IDs are mutually exclusive."
        )

    if target_label_ids:
        target_labels: List[
            TargetLabel
        ] = TargetLabelManager().unoptimized_get_multiple(
            [{"id": id_} for id_ in target_label_ids]
        )
    else:
        target_labels: Generator[TargetLabel] = TargetLabelManager().list(
            filters=filters
        )

    renderer = OutputRenderer(
        records=target_labels,
        table_cls=TargetLabelsTable,
        command_args=args,
    )
    renderer.render()
