from postman import MonitorInfo
from tp import TpRelease
from typing import Tuple, Iterator, List, Optional


def build_telegram_message(monitor: MonitorInfo, release: Optional[TpRelease], args: Iterator[Tuple[str, str]]) -> str:
    result: str = str(monitor)
    if release is None:
        result += f'''
Релиз не найден        
        '''
    else:
        result += f'''
Ссылка на релиз: {release.markdown()}
        '''
    params: List[str] = []

    for k, v in args:
        params.append(f'''
{k}: {v}        
        ''')

    result += ''.join(params)

    return result
