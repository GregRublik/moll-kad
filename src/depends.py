from fastapi import Depends
from aiohttp import ClientSession
from utils.session_manager import SessionManager

def get_http_session(
        http_session: ClientSession = Depends(SessionManager.get_session),
) -> ClientSession:
    return http_session