from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from bot.config.settings import settings
from bot.handlers.event_handler import process_event
from bot.logger import logger
from bot.utils.signature import verify_signature

app = FastAPI()


@app.post("/")
async def callback(
    request: Request, x_works_signature: str = Header(None)
) -> JSONResponse:
    raw_body = await request.body()
    raw_text = raw_body.decode()

    if not x_works_signature or not verify_signature(
        raw_text, x_works_signature, settings.bot_secret
    ):
        logger.error("Invalid or missing signature.")
        raise HTTPException(status_code=403, detail="Invalid or missing signature")

    data = await request.json()
    return await process_event(data)
