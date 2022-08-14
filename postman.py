import requests
from typing import Dict, Any
from dataclasses import dataclass


@dataclass()
class MonitorInfo:
    name: str
    status_of_last_run: str
    requests_total: int
    tests_total: int
    tests_failed: int


BASE_URL: str = 'https://api.getpostman.com/'


def get_url(path: str) -> str:
    return f'{BASE_URL}/{path}'


class Postman:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_monitor(self, guid: str) -> MonitorInfo:
        response = requests.get(get_url(f'monitors/{guid}'), headers=self.get_auth_header())
        if response.status_code is not 200:
            raise ValueError(response.__str__())
        json = response.json()
        return MonitorInfo(
            json['name'],
            json['lastRun']['status'],
            json['stats']['requests']['total'],
            json['assertions']['total'],
            json['assertions']['failed']
        )

    def get_auth_header(self) -> Dict[str, str]:
        return {'Authorization': f'Bearer {self.api_key}'}
