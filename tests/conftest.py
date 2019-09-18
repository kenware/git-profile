import os

import pytest
import requests
from app.routes import app
from app.constants import constants
from app.utils import get_github_url

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def mock_test(requests_mock):
    requests_mock.get(get_github_url('pygame'), text="call_back('github_data')")
    return requests.get(get_github_url('pygame')).text

@pytest.fixture
def mock_test2(requests_mock):
    requests_mock.get(constants['bitbucket_url'].format('pygame'), text="bitbucket_data")
    return requests.get(constants['bitbucket_url'].format('pygame')).text

@pytest.fixture
def mock_test3(mocker):
    mocker.patch('app.routes.prepare_github_data', return_value=4)
    mocker.patch('app.routes.prepare_bitbucket_data', return_value={'total_forked_repo': 2, 'total_repo': 4})