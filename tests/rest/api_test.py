import pytest
from app.api import api_application
import http.client
import os
from urllib.request import urlopen

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
DEFAULT_TIMEOUT = 2  # in secs

@pytest.fixture
def client():
    api_application.testing = True
    return api_application.test_client()

@pytest.mark.api
class TestApi:

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        assert response.status == http.client.OK

    def test_api_add_success(self, client):
        response = client.get('/calc/add/2/3')
        assert response.status_code == 200
        assert response.data.decode() == "5"

    def test_api_substract_success(self, client):
        response = client.get('/calc/substract/13/5')
        assert response.status_code == 200
        assert response.data.decode() == "8"

    def test_api_divide_by_zero(self, client):
        response = client.get('/calc/divide/1/0')
        assert response.status_code == 400
    
    def test_api_log10_fail(self, client):
        response = client.get('/calc/log10/-5')
        assert response.status_code == 400
