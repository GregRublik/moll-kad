from aiohttp import ClientSession

class KadService:

    base_url = "https://api-cloud.ru/api/kad_arbitr.php"

    def __init__(self, session: ClientSession):
        self.session = session


    async def search_case(self, num_deal: str, token: str):
        result = await self.session.get(
            self.base_url,
            params={
                "type": "search",
                "CaseNumber": num_deal,
                "token": token
            }
        )

        return await result.json()

    async def get_case_info(self, id_deal: str, token: str):
        result = await self.session.get(
            self.base_url,
            params={
                "type": "caseInfo",
                "token": token,
                "CaseId": id_deal,

            },
        )

        return await result.json()
