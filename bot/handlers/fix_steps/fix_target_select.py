from bot.handlers.messages import WRONG_INPUT
from bot.handlers.start import handle_start_event
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import CopyFixTarget, Step
from bot.services.works.payloads.payload import (
    set_copy_fix_target_payload,
    set_text_payload,
)
from bot.services.works.post_content import post_to_works


async def handle_fix_target_selection_event(
    user_id: str, session: dict, text: str
) -> None:
    """다듬기 타겟 선택 이벤트, step=="카피 다듬기" 인 경우 실행
    text는  중 하나
    선택한 채널에 따라 Session에 step="channel"로 설정
    """
    if text == CopyFixTarget.PREV.value:
        await handle_start_event(user_id)
        return

    if text in CopyFixTarget.NEW.value:
        context = session["context"]
        context[Step.FIX_TARGET.value] = text
        upsert_session(user_id=user_id, step=Step.FIX_TARGET.value, context=context)
        # 리액션
        await post_to_works(
            payload=set_text_payload(text),
            id=user_id,
        )
        # 다음 액션
        await post_to_works(
            payload=set_text_payload(text),
            id=user_id,
        )
        await handle_start_event(user_id)
    else:
        await post_to_works(
            payload=set_text_payload(WRONG_INPUT),
            id=user_id,
        )
        await post_to_works(
            payload=set_copy_fix_target_payload(),
            id=user_id,
        )
