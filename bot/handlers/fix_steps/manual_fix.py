from bot.services.copywriter.get_manual_fix import manual_fix
from bot.services.works.payloads.flexible_payload import set_manual_fix_payload
from bot.services.works.payloads.payload import (
    set_text_payload,
)
from bot.services.works.post_content import post_to_works


async def handle_manual_fix_event(user_id: str, session: dict, text: str) -> None:
    """직접 입력된 문구 수정 이벤트, step=="manual_fix" 인 경우 실행"""
    fixed_copy = await manual_fix(text)
    if isinstance(fixed_copy, dict):
        try:
            await post_to_works(
                payload=set_manual_fix_payload(fixed_copy),
                id=user_id,
            )
        except Exception:
            await post_to_works(
                payload=set_text_payload(str(fixed_copy)),
                id=user_id,
            )
    elif isinstance(fixed_copy, str):
        await post_to_works(
            payload=set_text_payload(fixed_copy),
            id=user_id,
        )
    else:
        await post_to_works(
            payload=set_text_payload("오류가 발생했어요. 다시 시도해주세요."),
            id=user_id,
        )
