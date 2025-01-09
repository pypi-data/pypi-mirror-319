import asyncio
from datasette.app import Datasette
import pytest
from datasette_auth_headers import PLUGIN_NAME, ID_HEADER_CONFIG_KEY


TEST_HEADER = "X-Authentik-User"


@pytest.fixture
def instance():
    return Datasette(
        memory=True,
        metadata={
            "plugins": {
                PLUGIN_NAME: {
                    ID_HEADER_CONFIG_KEY: TEST_HEADER,
                }
            }
        },
    )


@pytest.mark.asyncio
async def test_plugin_is_installed(instance):
    response = await instance.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-auth-headers" in installed_plugins


@pytest.mark.asyncio
async def test_plugin_sets_actor_when_header_present(instance):
    value = "gazpacho"
    response = await instance.client.get("/-/actor.json", headers={TEST_HEADER: value})
    assert response.status_code == 200
    assert response.json()["actor"]["id"] == value


@pytest.mark.asyncio
async def test_plugin_excludes_actor_when_header_missing(instance):
    response = await instance.client.get("/-/actor.json")
    assert response.status_code == 200
    assert response.json()["actor"] is None


@pytest.mark.asyncio
async def test_plugin_case_insensitive_header():
    value = "gazpacho"

    instance = Datasette(
        memory=True,
        metadata={
            "plugins": {
                PLUGIN_NAME: {
                    ID_HEADER_CONFIG_KEY: TEST_HEADER.upper(),
                }
            }
        },
    )

    response = await instance.client.get("/-/actor.json", headers={TEST_HEADER: value})
    assert response.status_code == 200
    assert response.json()["actor"]["id"] == value
