from fastapi.responses import JSONResponse

from bot.handlers.bot_status import BotStatus
from bot.handlers.steps.channel import handle_channel_selection_event
from bot.handlers.steps.description import handle_description_input_event
from bot.handlers.steps.purpose import handle_purpose_selection_event
from bot.handlers.steps.start import handle_start_event
from bot.handlers.steps.target import handle_target_input_event
from bot.handlers.steps.task_selection import handle_task_selection_event
from bot.services.db.dml import get_session
from bot.services.openai_client import get_openai_response
from bot.services.steps_enum import INITIAL_CONTACT, Step
from bot.services.works.payload import set_text_payload
from bot.services.works.post_content import post_to_works


async def process_event(data: dict) -> JSONResponse:
    event_type: str = data.get("type")
    source: dict = data.get("source", {})
    user_id: str = source.get("userId")

    if event_type != "message":
        return JSONResponse(status_code=200, content={"status": BotStatus.IGNORED})

    content = data.get("content", {})
    text: str = content.get("text", "")
    session = get_session(user_id)
    step = session.get("step", None)
    if text == INITIAL_CONTACT or not session or not step:
        await handle_start_event(user_id=user_id)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})

    event_handler_map = {
        Step.START.value: handle_task_selection_event,
        Step.TASK_SELECTION.value: handle_channel_selection_event,
        Step.CHANNEL.value: handle_purpose_selection_event,
        Step.PURPOSE.value: handle_target_input_event,
        Step.TARGET.value: handle_description_input_event,
    }

    if step == Step.START.value:
        await handle_task_selection_event(user_id=user_id, session=session, text=text)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})

    event_handler = event_handler_map.get(step)
    if event_handler:
        await event_handler(user_id=user_id, session=session, text=text)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
    else:
        response = await get_openai_response(
            prompt="어떤 말을 들어도 지금은 봇 개발중이니까 대답할 수 없고 창의적인 농담을 답변으로 하도록 해.",
            input=text,
        )
        await post_to_works(
            payload=set_text_payload(response),
            id=user_id,
        )
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
