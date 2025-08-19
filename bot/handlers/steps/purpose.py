from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Purpose, Step
from bot.services.works.payload import (
    set_campagin_purpose_button_payload,
    set_channel_button_payload,
    set_text_payload,
)
from bot.services.works.post_content import post_to_works
from bot.services.works.written_message import TARGET


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
        await post_to_works(payload=set_channel_button_payload(), id=user_id)
        upsert_session(user_id=user_id, step=Step.TASK_SELECTION.value, context=context)
        return

    if text in Purpose._value2member_map_:
        context = session["context"]
        context[Step.PURPOSE.value] = text
        upsert_session(user_id=user_id, step=Step.PURPOSE.value, context=context)
        await post_to_works(payload=set_text_payload(TARGET), id=user_id)
    else:
        await post_to_works(
            payload=set_campagin_purpose_button_payload(
                "잘못된 입력입니다. 다시 시도해주세요."
            ),
            id=user_id,
        )
