from __future__ import annotations
import logging
import time
import hashlib
import hmac
import base64
import uuid
from aiohttp import ClientSession

API_BASE_URL = 'https://api.switch-bot.com/v1.1/'

_LOGGER = logging.getLogger(__name__)

class SwitchBotClient:
    def __init__(self, session: ClientSession, token: str, secret: str):
        self._session = session
        self._token = token
        self._secret = secret


    def getHeaders(self):
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(self._token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(self._secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        return {
            'Authorization': self._token,
            't': str(t),
            'sign': str(sign, 'utf-8'),
            'nonce': str(nonce),
            'Content-Type': 'application/json; charset=utf-8',
        }


    async def get(self, endpoint: str, raise_for_status=True, **kwargs) -> any:
        async with self._session.get(API_BASE_URL + endpoint, headers=self.getHeaders(), raise_for_status=raise_for_status, **kwargs) as request:
            return await request.json()

    async def post(self, endpoint: str, data: any = None, raise_for_status=True, **kwargs) -> any:
        async with self._session.post(API_BASE_URL + endpoint, headers=self.getHeaders(), json=data, raise_for_status=raise_for_status, **kwargs) as request:
            return await request.json()
