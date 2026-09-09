import subprocess
import time

import pytest
import requests


BASE_URL = "http://127.0.0.1:3000"


@pytest.fixture(scope="module")
def server():
    process = subprocess.Popen(["python", "app.py"])

    for _ in range(30):
        try:
            response = requests.get(f"{BASE_URL}/health")

            if response.status_code == 200:
                break

        except requests.ConnectionError:
            time.sleep(1)

    else:
        process.terminate()
        pytest.fail("L'application n'a pas démarré")

    yield

    process.terminate()
    process.wait()


def test_application_is_available(server):
    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_home_endpoint(server):
    response = requests.get(f"{BASE_URL}/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["message"] == "Hello from Docker + Azure CI/CD!"