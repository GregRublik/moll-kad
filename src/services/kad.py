from aiohttp import ClientSession
from config import settings

class KadService:

    base_url = "https://api-cloud.ru/api/kad_arbitr.php"

    def __init__(self, session: ClientSession):
        self.session = session
        self.token = settings.kad.api_key


    async def search_case(self, num_deal: str):
        result = await self.session.get(
            self.base_url,
            params={
                "type": "search",
                "CaseNumber": num_deal,
                "token": self.token
            }
        )
        try:
            if result.status == 200:
                result = await result.json()
                return result["Result"]
            else:
                return await result.json()
        except KeyError:
            print(result)
            raise

    async def get_case_info(self, id_deal: str):
        result = await self.session.get(
            self.base_url,
            params={
                "type": "caseInfo",
                "token": self.token,
                "CaseId": id_deal,

            },
        )
        if result.status == 200:
            result = await result.json()
            return result["Result"]
        else:
            return await result.json()
