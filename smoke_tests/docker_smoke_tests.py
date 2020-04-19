import docker
import pytest
import requests
import subprocess
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ['docker_compose']


def docker_exec(container, command):
    return container.exec_run(
        cmd=command.split(),
        stdout=True,
        stderr=True,
        tty=True,
        workdir='/app'
    )


@pytest.fixture(scope='module')
def wait_for_api(module_scoped_container_getter):
    request_session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )
    request_session.mount('http://', HTTPAdapter(max_retries=retries))
    service_info = module_scoped_container_getter.get('lafilmoapi')
    network_info = service_info.network_info[0]
    api_url = f'http://localhost:{network_info.host_port}/api/'
    client = docker.from_env()
    container = client.containers.get(service_info.name)
    makemigrations_code, output = docker_exec(container, 'python manage.py migrate')
    assert makemigrations_code == 0
    migrate_code, output = docker_exec(container, 'python manage.py migrate')
    assert migrate_code == 0
    assert request_session.get(api_url)
    return request_session, api_url


def test_should_connect_to_films_endpoint(wait_for_api):
    request_session, api_url = wait_for_api

    response = request_session.get(api_url)

    assert response.status_code == 200
    assert response.content == b'[]'
