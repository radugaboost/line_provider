from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.models.line_provider.event import Event

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("event_id", "body", "expected_status", "fixtures"),
    [
        (
            "1",
            {"name": "test13"},
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / "line_provider.event.json",
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_update_event(
    client: AsyncClient,
    event_id: str,
    body: Dict[str, Any],
    expected_status: int,
    db_session: AsyncSession,
) -> None:
    obj = await db_session.get(Event, int(event_id))

    assert obj is not None
    assert int(event_id) == obj.id

    test_name = obj.name

    response = await client.put(
        "".join([URLS["event"]["update"], event_id]),
        json=body,
    )

    updated_obj = await db_session.get(Event, int(event_id))
    assert updated_obj is not None

    assert test_name != updated_obj.name
    assert response.status_code == expected_status
