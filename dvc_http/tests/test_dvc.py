import pytest
from dvc.testing.test_api import TestAPI  # noqa, pylint: disable=unused-import
from dvc.testing.test_remote import (  # noqa, pylint: disable=unused-import
    TestRemote,
)
from dvc.testing.test_workspace import (  # noqa, pylint: disable=unused-import
    TestAdd,
    TestImport,
)


@pytest.fixture
def cloud_name():
    return "http"


@pytest.fixture
def remote(make_remote, cloud_name):
    yield make_remote(name="upstream", typ=cloud_name)


@pytest.fixture
def workspace(make_workspace, cloud_name):
    pytest.skip("broken")


@pytest.fixture
def stage_md5():
    pytest.skip("broken")


@pytest.fixture
def is_object_storage():
    return False


@pytest.fixture
def dir_md5():
    pytest.skip("broken")


@pytest.fixture
def hash_name():
    return "checksum"


@pytest.fixture
def hash_value():
    pytest.skip("broken")


@pytest.fixture
def dir_hash_value(dir_md5):
    pytest.skip("broken")
