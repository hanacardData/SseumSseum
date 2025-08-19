from bot.handlers.steps.start import handle_start_event
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Channel, Step
from bot.services.works.payload import (
    set_campagin_purpose_button_payload,
    set_channel_button_payload,
)
from bot.services.works.post_content import post_to_works


async def handle_channel_selection_event(
    user_id: str, session: dict, text: str
) -> None:
    """채널 선택 이벤트, step=="task_selection" 인 경우 실행
    text는 채널 선택지 중 하나
    선택한 채널에 따라 Session에 step="channel"로 설정
    """
    if text == Channel.PREV.value:
        await handle_start_event(user_id)
        return

    if text in Channel._value2member_map_:
        context = session["context"]
        context[Step.CHANNEL.value] = text
        upsert_session(user_id=user_id, step=Step.CHANNEL.value, context=context)
        await post_to_works(payload=set_campagin_purpose_button_payload(), id=user_id)
    else:
        await post_to_works(
            payload=set_channel_button_payload(
                "잘못된 입력입니다. 채널을 다시 입력해주세요."
            ),
            id=user_id,
        )
