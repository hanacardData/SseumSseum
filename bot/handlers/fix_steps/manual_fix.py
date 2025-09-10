from bot.handlers.start import handle_start_event
from bot.services.copywriter.get_manual_fix import manual_fix
from bot.services.works.payloads.payload import (
    set_text_payload,
)
from bot.services.works.post_content import post_to_works


async def handle_manual_fix_event(user_id: str, session: dict, text: str) -> None:
    """직접 입력된 문구 수정 이벤트, step=="manual_fix" 인 경우 실행"""
    fixed_copy = await manual_fix(text)
    await post_to_works(
        payload=set_text_payload(str(fixed_copy)),
        id=user_id,
    )
    await handle_start_event(user_id=user_id)
