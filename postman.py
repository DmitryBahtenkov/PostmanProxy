import requests
from typing import Dict
from dataclasses import dataclass
import json


@dataclass()
class MonitorInfo:
    name: str
    status_of_last_run: str
    requests_total: int
    tests_total: int
    tests_failed: int

    def __str__(self):
        return f'''
Монитор: {self.name}
Статус: {self.status_of_last_run}
Всего тестов: {self.tests_total}
Не пройдено: {self.tests_failed}
Всего запросов: {self.requests_total}
        '''


BASE_URL: str = 'https://api.getpostman.com'


def get_url(path: str) -> str:
    return f'{BASE_URL}/{path}'


class Postman:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_monitor(self, guid: str) -> MonitorInfo:
        response = requests.get(get_url(f'monitors/{guid}'), headers=self.get_auth_header())
        if response.status_code != 200:
            raise ValueError(response.__str__())
        monitor = response.json()['monitor']
        return MonitorInfo(
            monitor['name'],
            monitor['lastRun']['status'],
            monitor['lastRun']['stats']['requests']['total'],
            monitor['lastRun']['stats']['assertions']['total'],
            monitor['lastRun']['stats']['assertions']['failed']
        )

    def get_auth_header(self) -> Dict[str, str]:
        return {'X-API-Key': self.api_key}
