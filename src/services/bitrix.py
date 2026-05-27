from aiohttp import ClientSession
from typing import Literal, Optional

from config import settings
from constants import BitrixContactConstants, BitrixKadConstants, BitrixKadEventsConstants, BitrixFieldsConstants


class BitrixService:

    def __init__(
            self,
            http_session: ClientSession,
            fields
    ):
        self.http_session = http_session
        self.fields = fields

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

    async def get_fields(self):
        response = await self.send_request(
            "crm.item.fields",
            json={
                "entityTypeId": self.fields.entity_type_id
            }
        )
        return response


class BitrixKadService(BitrixService):

    def __init__(self, http_session: ClientSession):
        super().__init__(
            http_session=http_session,
            fields=BitrixKadConstants
        )

    async def create_one(
        self, fields: dict
    ):

        response = await self.send_request(
            "crm.item.add",
            json={
                "entityTypeId": self.fields.entity_type_id,
                "fields": fields,
                "useOriginalUfNames": "N"
            }
        )
        return response

    async def find_by_element_id(
            self, element_id: int
    ):
        response = await self.send_request(
            "crm.item.list",
            json={
                "entityTypeId": self.fields.entity_type_id,
                "select": ["ID", self.fields.element_id],
                "filter": {
                    self.fields.element_id: element_id
                },
                "useOriginalUfNames": "N"
            }
        )
        return response


class BitrixKadEventsService(BitrixService):

    def __init__(self, http_session: ClientSession):
        super().__init__(
            http_session=http_session,
            fields=BitrixKadEventsConstants
        )

    async def create_one(
        self, fields: dict
    ):

        response = await self.send_request(
            "crm.item.add",
            json={
                "entityTypeId": self.fields.entity_type_id,
                "fields": fields,
                "useOriginalUfNames": "N"
            }
        )
        return response

    async def find_by_element_id(
            self, element_id: int
    ):
        response = await self.send_request(
            "crm.item.list",
            json={
                "entityTypeId": self.fields.entity_type_id,
                "select": ["ID", self.fields.element_id],
                "filter": {
                    self.fields.element_id: element_id
                },
                "useOriginalUfNames": "N"
            }
        )
        return response


class BitrixContactService(BitrixService):

    def __init__(self, http_session: ClientSession):
        super().__init__(
            http_session=http_session,
            fields=BitrixContactConstants
        )

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
                    f"!={self.fields.bankruptcy_case_number}": ""
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
