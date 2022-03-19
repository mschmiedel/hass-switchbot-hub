from __future__ import annotations

from aiohttp import ClientSession

API_BASE_URL = 'https://api.switch-bot.com/v1.0/'


class SwitchBotClient:
    def __init__(self, session: ClientSession, token: str):
        self._session = session
        self._token = token
        self._headers = {
            'Authorization': self._token,
            'Content-Type': 'application/json; charset=utf-8',
        }

    async def get(self, endpoint: str, raise_for_status=True, **kwargs) -> any:
        async with self._session.get(API_BASE_URL + endpoint, headers=self._headers, raise_for_status=raise_for_status, **kwargs) as request:
            return await request.json()

    async def post(self, endpoint: str, data: any = None, raise_for_status=True, **kwargs) -> any:
        async with self._session.post(API_BASE_URL + endpoint, headers=self._headers, json=data, raise_for_status=raise_for_status, **kwargs) as request:
            return await request.json()
