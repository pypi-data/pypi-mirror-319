import logging
from typing import Dict, Generator, List, Optional

from probely.exceptions import ProbelyObjectsNotFound, ProbelyRequestFailed

from ..settings import (
    PROBELY_API_PAGE_SIZE,
    PROBELY_API_TARGETS_DETAIL_URL,
    PROBELY_API_TARGETS_URL,
)
from .client import ProbelyAPIClient

logger = logging.getLogger(__name__)


# TODO: REMOVE
def retrieve_targets(targets_ids: List[str]) -> List[Dict]:
    retrieved_targets = []
    for target_id in targets_ids:
        retrieved_targets.append(retrieve_target(target_id))

    return retrieved_targets


# TODO: REMOVE
def retrieve_target(target_id: str) -> Dict:
    url = PROBELY_API_TARGETS_DETAIL_URL.format(id=target_id)
    resp_status_code, resp_content = ProbelyAPIClient.get(url)
    if resp_status_code == 404:
        raise ProbelyObjectsNotFound(target_id)

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content


# TODO: REMOVE
def list_targets(targets_filters: Optional[Dict] = None) -> Generator[Dict, None, None]:
    filters = targets_filters or {}
    page = 1

    while True:
        query_params = {
            "ordering": "-changed",
            "length": PROBELY_API_PAGE_SIZE,
            "page": page,
            **filters,
        }

        resp_status_code, resp_content = ProbelyAPIClient.get(
            PROBELY_API_TARGETS_URL,
            query_params=query_params,
        )

        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)

        results = resp_content["results"]
        total_pages_count = resp_content.get("page_total")

        for result in results:
            yield result

        if page >= total_pages_count:
            break

        page += 1
