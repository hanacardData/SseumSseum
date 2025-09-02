from bot.handlers.generation_steps.messages import (
    BACK_TO_CHANNEL,
    REACTION_TO_PURPOSE,
    TARGET_GUIDE,
    WRONG_INPUT,
)
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Purpose, Step
from bot.services.works.payload import (
    set_campagin_purpose_button_payload,
    set_channel_button_payload,
    set_text_payload,
)
from bot.services.works.post_content import post_to_works


async def handle_purpose_selection_event(
    user_id: str, session: dict, text: str
) -> None:
    """캠페인 목적 선택 이벤트, step=="channel" 인 경우 실행
    text는 캠페인 목적 선택지 중 하나
    선택한 캠페인 목적에 따라 Session에 step="purpose"로 설정
    """
    if text == Purpose.PREV.value:
        context = session["context"]
        context.pop(Step.CHANNEL.value, None)
        await post_to_works(payload=set_text_payload(BACK_TO_CHANNEL), id=user_id)
        await post_to_works(payload=set_channel_button_payload(), id=user_id)
        upsert_session(user_id=user_id, step=Step.TASK_SELECTION.value, context=context)
        return

    if text in Purpose._value2member_map_:
        context = session["context"]
        context[Step.PURPOSE.value] = text
        upsert_session(user_id=user_id, step=Step.PURPOSE.value, context=context)
        await post_to_works(
            payload=set_text_payload(REACTION_TO_PURPOSE.format(purpose=text)),
            id=user_id,
        )
        await post_to_works(
            payload=set_text_payload(TARGET_GUIDE),
            id=user_id,
        )
        return

    await post_to_works(
        payload=set_campagin_purpose_button_payload(content_text=WRONG_INPUT),
        id=user_id,
    )
