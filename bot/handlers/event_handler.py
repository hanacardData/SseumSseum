from fastapi.responses import JSONResponse

from bot.handlers.bot_status import BotStatus
from bot.services.db.dml import get_session, upsert_session
from bot.services.openai_client import get_openai_response
from bot.services.steps_enum import Channel, Purpose, Start, Step
from bot.services.works.payload import (
    set_campagin_purpose_button_payload,
    set_channel_button_payload,
    set_initial_image_carousel_payload,
    set_text_payload,
)
from bot.services.works.post_content import post_to_works
from bot.services.works.written_message import DESCRIPTION, TARGET

_VALID_OPTIONS = set(item.value for item in Channel) | set(
    item.value for item in Purpose
)


async def initial_contact(user_id: str) -> None:
    upsert_session(user_id=user_id, step=Step.START.value, context={})
    await post_to_works(
        payload=set_text_payload("어떤 문구가 고민이신가요? 씀씀이와 함께 써봐요!"),
        id=user_id,
    )
    await post_to_works(payload=set_initial_image_carousel_payload(), id=user_id)


async def process_event(data: dict) -> JSONResponse:
    event_type: str = data.get("type")
    source: dict = data.get("source", {})
    user_id: str = source.get("userId")

    if event_type != "message":
        return JSONResponse(status_code=200, content={"status": BotStatus.IGNORED})

    content = data.get("content", {})
    text: str = content.get("text", "")
    user_info = get_session(user_id)

    if text.startswith("시작하기") or bool(user_info is None):
        await initial_contact(user_id=user_id)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
    elif user_info["step"] == Step.START.value and text == Start.COPY_GENERATE.value:
        upsert_session(
            user_id=user_id,
            step=Step.GENERATE.value,
            context={},
        )
        await post_to_works(
            payload=set_text_payload(
                "좋아요! 씀씀이와 함께 카피를 만들어볼까요? 4단계만 거치면 바로 완성돼요!"
            ),
            id=user_id,
        )
        await post_to_works(payload=set_channel_button_payload(), id=user_id)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
    elif (
        user_info["step"] == Step.GENERATE.value and text in Channel._value2member_map_
    ):
        context = user_info["context"]
        context[Step.CHANNEL.value] = text
        upsert_session(user_id=user_id, step=Step.CHANNEL.value, context=context)
        await post_to_works(payload=set_campagin_purpose_button_payload(), id=user_id)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
    elif user_info["step"] == Step.CHANNEL.value and text in Purpose._value2member_map_:
        context = user_info["context"]
        context[Step.PURPOSE.value] = text
        upsert_session(user_id=user_id, step=Step.PURPOSE.value, context=context)
        await post_to_works(payload=set_text_payload(TARGET), id=user_id)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
    elif user_info["step"] == Step.PURPOSE.value and text not in _VALID_OPTIONS:
        context = user_info["context"]
        context[Step.TARGET.value] = text
        upsert_session(user_id=user_id, step=Step.TARGET.value, context=context)
        await post_to_works(payload=set_text_payload(DESCRIPTION), id=user_id)
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})
    elif user_info["step"] == Step.TARGET.value and text not in _VALID_OPTIONS:
        context = user_info["context"]
        context[Step.DESCRIPTION.value] = text
        upsert_session(user_id=user_id, step=Step.DESCRIPTION.value, context=context)
        await post_to_works(payload=set_text_payload(str(context)), id=user_id)
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
