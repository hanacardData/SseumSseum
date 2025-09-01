from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Purpose, Step
from bot.services.works.payload import (
    set_campagin_purpose_button_payload,
    set_channel_button_payload,
    set_text_payload,
)
from bot.services.works.post_content import post_to_works

_BACK = "채널선택으로 다시 돌아왔어요!"
_REACTION_TO_PURPOSE = "{purpose} 목적으로 캠페인을 진행하시는군요!"

_TARGET = """세번째로, 메시지를 받을 손님에 대해 설명해주세요.

예시)
- 하나대학교 신입생
- 다음달 미국 여행을 준비중인 유학생
- 신용카드 없이 체크카드만 쓰는 20대 후반 직장인
"""
_WRONG_PURPOSE = "'{text}' 입력은 이해할 수 없어요. 캠페인 목적을 다시 입력해주세요."


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
        await post_to_works(
            payload=set_channel_button_payload(content_text=_BACK), id=user_id
        )
        upsert_session(user_id=user_id, step=Step.TASK_SELECTION.value, context=context)
        return

    if text in Purpose._value2member_map_:
        context = session["context"]
        context[Step.PURPOSE.value] = text
        upsert_session(user_id=user_id, step=Step.PURPOSE.value, context=context)
        await post_to_works(
            payload=set_text_payload(_REACTION_TO_PURPOSE.format(purpose=text)),
            id=user_id,
        )
        await post_to_works(
            payload=set_text_payload(_TARGET),
            id=user_id,
        )
        return

    await post_to_works(
        payload=set_campagin_purpose_button_payload(
            content_text=_WRONG_PURPOSE.format(text=text)
        ),
        id=user_id,
    )
