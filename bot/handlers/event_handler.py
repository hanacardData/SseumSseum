from fastapi.responses import JSONResponse

from bot.handlers.bot_status import BotStatus
from bot.handlers.generation_steps.channel import handle_channel_selection_event
from bot.handlers.generation_steps.description import handle_description_input_event
from bot.handlers.generation_steps.purpose import handle_purpose_selection_event
from bot.handlers.generation_steps.target import handle_target_input_event
from bot.handlers.generation_steps.task_selection import handle_task_selection_event
from bot.handlers.start import handle_start_event
from bot.handlers.view import handle_view_event
from bot.services.db.dml import get_session, insert_log
from bot.services.steps_enum import COPIES, INITIAL_CONTACT, SUMMARY, VIEW, Step
from bot.services.works.payload import set_text_payload
from bot.services.works.post_content import post_to_works


async def process_event(data: dict) -> JSONResponse:
    event_type: str = data.get("type")
    source: dict = data.get("source", {})
    user_id: str = source.get("userId")
    if event_type not in ["message", "postback"]:
        return JSONResponse(status_code=200, content={"status": BotStatus.IGNORED})

    if event_type == "postback":  # 기억해두기를 눌렀을 때
        session = get_session(user_id)
        if session and session.get("step") == Step.END.value and "context" in session:
            # data["data"]: copy idx -> phrase 1 phrase 2 ...
            save_copy: dict = session["context"][COPIES][data["data"]]
            insert_log(
                user_id=user_id,
                channel=session["context"][Step.CHANNEL.value],
                purpose=session["context"][Step.PURPOSE.value],
                target=session["context"][Step.TARGET.value],
                description=session["context"][Step.DESCRIPTION.value],
                summary=session["context"][SUMMARY],
                title=save_copy["title"],
                content=save_copy["content"],
            )
            await post_to_works(
                payload=set_text_payload(
                    "마음에 드셨다니 기뻐요! 씀씀이가 이 카피를 기억해둘게요!"
                ),
                id=user_id,
            )
            return JSONResponse(status_code=200, content={"status": BotStatus.OK})

    content = data.get("content", {})
    text: str = content.get("text", "")

    session = get_session(user_id)
    step = session.get("step", None)
    if text == INITIAL_CONTACT or not session or not step:
        await handle_start_event(user_id=user_id)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})

    if text == VIEW:
        await handle_view_event(user_id=user_id)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})

    event_handler_map = {
        Step.START.value: handle_task_selection_event,
        Step.TASK_SELECTION.value: handle_channel_selection_event,
        Step.CHANNEL.value: handle_purpose_selection_event,
        Step.PURPOSE.value: handle_target_input_event,
        Step.TARGET.value: handle_description_input_event,
    }
    event_handler = event_handler_map.get(step)

    if event_handler:
        await event_handler(user_id=user_id, session=session, text=text)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
    else:
        await post_to_works(
            payload=set_text_payload(
                "죄송해요, 지금은 봇 개발 중이라 에러가 발생했나봐요. 시작하기 라고 입력해주세요!"
            ),
            id=user_id,
        )
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
