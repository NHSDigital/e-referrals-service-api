import requests

from enum import Enum


class HttpMethod(Enum):
    """Provides enum detailing standard HTTP verbs that can be used as part of calling an endpoint"""

    GET = requests.get
    POST = requests.post
