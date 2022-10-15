from dataclasses import dataclass
import requests
from typing import List


@dataclass
class TpRelease:
    id: int
    name: str


class TargetProcess:
    def __init__(self, url: str, access_token: str):
        self._url = url
        self._access_token_part = f'access_token={access_token}'
        self._access_token = access_token

    def get_last_release(self, filter_field: str, filter_value: str) -> TpRelease:
        parts: List[str] = [
            f'where={filter_field} contains \'{filter_value}\'',
            'orderByDesc=CreateDate',
            'include=[Name]',
            'take=1',
            'format=json'
        ]
        url: str = f'{self._url}/api/v1/releases?{self._access_token_part}&{"&".join(parts)}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(str(response))

        data = response.json()['Items'][0]
        return TpRelease(data['Id'], data['Name'])

    def build_url(self, entity_id: int):
        return f'{self._url}/entity/{entity_id}'