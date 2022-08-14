import json
import os
from typing import Optional


class Config:
    def __init__(self, file: str):
        self.file = file
        self._load()

    def _load(self):
        if not os.path.exists(self.file):
            raise FileNotFoundError(f'file {self.file} not exist')

        with open(self.file) as f:
            self.data = json.load(f)

    def get(self, key: str) -> Optional[str]:
        try:
            return str(self.data[key])
        except KeyError:
            return None
