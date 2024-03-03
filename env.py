from os import environ
from typing import Final


class Keys:
    TOKEN: Final = environ.get('TOKEN', 'token')
    API_KEY: Final = environ.get('API_KEY', 'api_key')
    ADMIN_ID: Final = environ.get('ADMIN_ID', 'admin_id')