from aiohttp import ClientSession
from typing import Literal, Optional

from config import settings
from constants import BitrixContactConstants
from utils.session_manager import SessionManager


class BitrixService:

    def __init__(
            self,
            http_session: ClientSession = SessionManager.get_session(),
    ):
        self.http_session = http_session

    async def _request(self, method, url, params, json):
        return await self.http_session.request(
            method=method,
            url=url,
            params=params,
            json=json,
        )

    async def send_request(
        self,
        endpoint: str,
        method: Literal['get', 'post'] = 'post',
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        url = f"{settings.bitrix.webhook_url}/{endpoint}.json"

        response = await self._request(
            method=method,
            url=url,
            params=params,
            json=json
        )
        return await response.json()

class BitrixContactService(BitrixService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = BitrixContactConstants()

    async def get_fields(self):
        response = await self.send_request(
            "crm.item.fields",
            json={
                "entityTypeId": 3
            }
        )
        return response

    async def get_contacts(self, start: Optional[int] = 0):
        response = await self.send_request(
            "crm.contact.list",
            json={
                "select": [
                    "ID",
                    "NAME",
                    "SECOND_NAME",
                    "LAST_NAME",
                    self.fields.inn,
                    self.fields.fedresurs_monitoring,
                    self.fields.date_updated_fedresurs,
                    self.fields.bankruptcy_case_number,
                    self.fields.fedresurs_found,
                    "BIRTHDATE",
                ],
                "filter": {
                    "ID": "15151",
                    # self.fields.fedresurs_monitoring: "1", # мониторинг в федресурсе
                    # f"={self.fields.fedresurs_found}": "", # Только необработанные ранее
                    # "!=NAME": "",               # только с заполненными колями
                    # "!=SECOND_NAME": "",        # только с заполненными колями
                    # "!=LAST_NAME": "",          # только с заполненными колями
                    # "!=BIRTHDATE": ""           # только с заполненными колями
                },
                "order": {
                    # self.fields.date_updated_fedresurs: "ASC",  # "ASC", "DESC"
                    # "BIRTHDATE": "DESC"
                },
                "start": start
            }
        )
        try:
            return response["result"]
        except KeyError:
            print(f"error response: {response}")
            raise
