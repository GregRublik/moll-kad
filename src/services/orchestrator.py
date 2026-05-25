from aiohttp import ClientSession
from services.bitrix import BitrixContactService, BitrixKadService, BitrixKadEventsService
from services.kad import KadService

class OrchestratorService:

    def __init__(
            self,
            session: ClientSession,

    ):
        self.session = session
        self.contact_service: BitrixContactService = BitrixContactService(session)
        self.bitrix_kad_service: BitrixKadService = BitrixKadService(session)
        self.kad_service: KadService = KadService(session)
        self.bitrix_kad_events_service = BitrixKadEventsService(session)

    async def process_clients(self, count: int):
        """Процесс поиска информации о клиентах на федресурсе"""
        clients = await self.contact_service.get_contacts()

        for client in clients[:count]:
            await self.process_single_client(client)

    async def process_single_client(self, client):
        kad_info_client = await self.get_kad_info_for_client(client) # получаем ЗАКЭШИРОВАН ЛИ ОН И ДАННЫЕ КЭША, ЛИБО search_person
        # todo create deal_kad_to bitrix with kad_info_client

        case_info = kad_info_client.get("CaseInfo", {})
        participants = kad_info_client.get("Participants", {})
        case_instances = kad_info_client.get("CaseInstances", {})

        possible_sides = {
            "Plaintiffs": "Истец",
            "Respondents": "Ответчик",
            "Thirds": "Третье лицо",
            "Others": "Иной"
        }
        participants_normalize = []

        for k, v in participants.items():
            for participant in v:
                participants_normalize.append(
                    f"{possible_sides[k]}: Name: {participant.get('Name')} INN: {participant.get('INN')} "
                    f"ID: {participant.get('Id')} Address: {participant.get('Address')} "
                    f"BirthDate: {participant.get('BirthDate')}"
                )

        courts = []
        judges = []
        events = []

        for deal in case_instances:
            courts.append(deal.get("Court", {}).get("Name"))
            for judge in deal.get("Judges", []):
                judges.append(judge.get("Name"))

            for event in deal.get("InstanceEvents", []):
                data_event = {
                    "title": f'{case_info.get("CaseNumber")} {event.get("EventTypeName")}',
                    self.bitrix_kad_events_service.fields.opportunity: event.get("ClaimSum", ""),
                    self.bitrix_kad_events_service.fields.element_id: event.get("EventTypeId", ""),
                    self.bitrix_kad_events_service.fields.court_date: event.get("AdditionalInfo", ""),
                    self.bitrix_kad_events_service.fields.description: event.get("ContentTypes", ""),
                    self.bitrix_kad_events_service.fields.link_file: event.get("File", ""),
                    self.bitrix_kad_events_service.fields.comment: event.get("Comment", ""),
                    self.bitrix_kad_events_service.fields.date: event.get("Date", ""),
                    self.bitrix_kad_events_service.fields.date_publish_event: event.get("PublishDate", ""),
                    self.bitrix_kad_events_service.fields.declarers: event.get("Declarers", ""),
                    self.bitrix_kad_events_service.fields.inn_declarers: event.get("DeclarerInn", ""),
                }
                event = await self.bitrix_kad_events_service.create_one(data_event)
                # print(event)
                print(data_event)
                # events.append(str(data_event))
                break


        card_deal = {
            "title": case_info.get("CaseNumber"),
            self.bitrix_kad_service.fields.court: list(set(courts)), # он у каждого дела свой, может не совпадать в теории
            self.bitrix_kad_service.fields.status: case_info.get("State"), # либо "finish": "false", // Законченное дело true / false
            self.bitrix_kad_service.fields.participants: participants_normalize,#[f"{participant.}" for participant in participants], #
            self.bitrix_kad_service.fields.link_deal: f"https://kad.arbitr.ru/Card/{case_info.get('CaseId')}",
            # self.bitrix_kad_service.fields.events: events,
        }

        return await self.bitrix_kad_service.create_one(
            card_deal,
        )

    async def get_kad_info_for_client(self, client):
        search_results = await self.kad_service.search_case(client.get("UF_CRM_FEDRESURS_IP"))

        if len(search_results) > 1:
            print("найдено более 2 дел")

        kad_info_client = None

        for search_result in search_results:
            case_id = search_result.get("caseId")
            kad_info_client = await self.kad_service.get_case_info(case_id)

        return kad_info_client

