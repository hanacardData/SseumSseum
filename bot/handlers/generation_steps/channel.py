from bot.handlers.start import handle_start_event
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Channel, Step
from bot.services.works.payload import (
    set_campagin_purpose_button_payload,
    set_channel_button_payload,
)
from bot.services.works.post_content import post_to_works

_PURPOSE = """{channel} 채널로 캠페인을 진행할 계획이시군요!
두번째로는 캠페인의 목적을 선택해주세요."""
_WRONG_CHANNEL = "'{text}' 입력은 이해할 수 없어요. 채널을 다시 입력해주세요."


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
        await post_to_works(
            payload=set_campagin_purpose_button_payload(
                content_text=_PURPOSE.format(channel=text)
            ),
            id=user_id,
        )
        return
    else:
        await post_to_works(
            payload=set_channel_button_payload(
                content_text=_WRONG_CHANNEL.format(text=text)
            ),
            id=user_id,
        )
