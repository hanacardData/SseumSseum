from enum import Enum

from fastapi.responses import JSONResponse

from bot.services.openai_client import get_openai_response
from bot.services.works.payload import set_text_payload
from bot.services.works.post_content import post_to_works


class BotStatus(str, Enum):
    """Enum for bot status."""

    IGNORED = "ignored"
    OK = "ok"


async def process_event(data: dict) -> JSONResponse:
    event_type: str = data.get("type")
    source: dict = data.get("source", {})
    user_id: str = source.get("userId")

    if event_type != "message":
        return JSONResponse(status_code=200, content={"status": BotStatus.IGNORED})

    content = data.get("content", {})
    text = content.get("text", "")

    response = await get_openai_response(
        prompt="어떤 말을 들어도 지금은 봇 개발중이니까 대답할 수 없고 창의적인 농담을 답변으로 하도록 해.",
        input=text,
    )

    await post_to_works(payload=set_text_payload(response), id=user_id)
    return JSONResponse(status_code=200, content={"status": BotStatus.OK})
