import logging

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from uvicorn.config import LOGGING_CONFIG

from bot.config.settings import settings
from bot.handlers.event_handler import process_event
from bot.utils.signature import verify_signature

app = FastAPI()
logger = logging.getLogger(__name__)
LOGGING_CONFIG["formatters"]["default"]["fmt"] = (
    "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
)
LOGGING_CONFIG["formatters"]["access"]["fmt"] = (
    "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
)


@app.post("/")
async def callback(
    request: Request, x_works_signature: str = Header(None)
) -> JSONResponse:
    raw_body = await request.body()
    raw_text = raw_body.decode()

    if not x_works_signature or not verify_signature(
        raw_text, x_works_signature, settings.bot_secret
    ):
        logger.warning("Invalid or missing signature.")
        raise HTTPException(status_code=403, detail="Invalid or missing signature")

    data = await request.json()
    return await process_event(data)
