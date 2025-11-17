from services.http_service import http_clients
from services.log_service import logger
from services.module_load_service import load_ocr_api

ocr_api=None

async def ocr():
    global ocr_api
    if ocr_api is None:
        ocr_api=load_ocr_api()
    pass