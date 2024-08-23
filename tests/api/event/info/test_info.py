from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("event_id", "expected_status", "fixtures"),
    [
        (
            "0",
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / "line_provider.event.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_event(
    client: AsyncClient,
    event_id: str,
    expected_status: int,
) -> None:
    response = await client.get(
        "".join([URLS["event"]["info"], event_id]),
    )
    assert response.status_code == expected_status
