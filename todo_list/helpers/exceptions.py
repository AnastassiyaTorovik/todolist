from typing import Dict, Union


class BadRequestException(Exception):
    def __init__(self, message: Dict[str, Union[int, str]]):
        self.message = message, message.get('status')

    def __str__(self):
        return f'[{self.message[0]["title"]}]: {self.message[0]["detail"]}'


def get400(detail: str, title: str = 'Bad Request') -> BadRequestException:
    return BadRequestException({
        'title': title,
        'status': 400,
        'type': 'about:blank',
        'detail': detail
    })


def get404(detail: str) -> BadRequestException:
    return BadRequestException({
        'title': 'Not Found',
        'status': 404,
        'type': 'about:blank',
        'detail': detail
    })