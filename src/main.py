from services.orchestrator import OrchestratorService
from asyncio import run
from utils.session_manager import SessionManager
from aiohttp import ClientSession



async def main(cnt):
    session: ClientSession = await SessionManager.get_session()
    try:
        orchestrator = OrchestratorService(session)
        await orchestrator.process_clients(cnt)
    finally:
        await SessionManager.close_session()

if __name__ == "__main__":
    count = int(input("Сколько персон обработать: "))
    run(main(int(count)))
