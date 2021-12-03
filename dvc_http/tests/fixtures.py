import os

import pytest


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(os.path.dirname(__file__), "docker-compose.yml")


@pytest.fixture
def make_http():
    def _make_http():
        raise NotImplementedError

    return _make_http


@pytest.fixture
def http(make_http):
    return make_http()

