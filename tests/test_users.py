import pytest
import requests
import requests_mock

# The base URL of the API we're testing
BASE_URL = "http://127.0.0.1:8000/users/"

@pytest.fixture(scope='module')
def valid_credentials():
    return {
        'username': 'admin',
        'password': 'qwerty'
    }

@pytest.fixture
def mock_server():
    with requests_mock.Mocker() as m:
        # Mocking valid authentication response
        m.get(f"{BASE_URL}?username=admin&password=qwerty", text="Authentication successful", status_code=200)

        # Mocking invalid authentication response
        m.get(f"{BASE_URL}?username=admin&password=adminLinks", text="Unauthorized", status_code=401)
        
        yield m

def test_user_authentication(valid_credentials, mock_server):
    url = f"{BASE_URL}?username={valid_credentials['username']}&password={valid_credentials['password']}"
    
    response = requests.get(url)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text == "Authentication successful", f"Unexpected response text: {response.text}"

def test_invalid_user_authentication(mock_server):
    url = f"{BASE_URL}?username=admin&password=adminLinks"
    
    response = requests.get(url)

    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"
    assert response.text == "Unauthorized", f"Unexpected response text: {response.text}"
