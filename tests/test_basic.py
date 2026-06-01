import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/")
    assert r.status_code == 200
    assert "GigaLinks API" in r.json().get("message", "")


@pytest.mark.asyncio
async def test_projects_list():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/projects")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
