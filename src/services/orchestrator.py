from aiohttp import ClientSession
from services.bitrix import BitrixContactService
from services.kad import KadService


class OrchestratorService:

    def __init__(
            self,
            session: ClientSession,

    ):
        self.session = session
        self.contact_service: BitrixContactService = BitrixContactService(session)
        self.kad_service: KadService = KadService(session)

    async def process_clients(self, count: int):
        """Процесс поиска информации о клиентах на федресурсе"""
        clients = await self.contact_service.get_contacts()

        for client in clients[:count]:
            await self.process_single_client(client)

    async def process_single_client(self, client):
        kad_info_client = await self.get_kad_info_for_client(client) # получаем ЗАКЭШИРОВАН ЛИ ОН И ДАННЫЕ КЭША, ЛИБО search_person

    async def get_kad_info_for_client(self, client):
        search_results = await self.kad_service.search_case(client.get("UF_CRM_FEDRESURS_IP"))

        for search_result in search_results:
            case_id = search_result.get("caseId")
            kad_info_client = await self.kad_service.get_case_info(case_id)

            print(kad_info_client)
