import asyncio
from services.kad import KadService
from services.csv_service import CsvService
from utils.session_manager import SessionManager
from config import settings

def normalize_results(results):
    if results is None:
        return []

    if isinstance(results, dict):
        return [results]

    if isinstance(results, str):
        return [{"value": results}]

    if isinstance(results, list):
        return [
            r if isinstance(r, dict) else {"value": r}
            for r in results
        ]

    return [{"value": str(results)}]

async def main(
    num_deal: str
):
    try:
        session = await SessionManager.get_session()
        service = KadService(
            session
        )
        csv_service = CsvService()
        cases = await service.search_case(num_deal)
        csv_service.save_results(num_deal, "search", cases.get("Result"))

        for case in cases.get("Result"):
            case_info = await service.get_case_info(case.get("caseId"))
            results = normalize_results(case_info.get("Result"))
            csv_service.save_results(num_deal, "info", results)


    finally:
        await SessionManager.close_session()


if __name__ == '__main__':
    deal = input("Enter number of deal: ")
    asyncio.run(main(deal))
