from typing import Any, Dict

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS


@pytest.mark.parametrize(
    ("body", "expected_status"),
    [
        (
            {"name": "test", "status": "waiting", "deadline": "2024-08-23T00:49:16.416Z", "odds": 2.22},
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_create_event(
    client: AsyncClient,
    body: Dict[str, Any],
    expected_status: int,
) -> None:
    response = await client.post(
        URLS["event"]["create"],
        json=body,
    )

    assert response.status_code == expected_status
