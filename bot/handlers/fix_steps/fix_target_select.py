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
    """다듬기 타겟 선택 이벤트, step=="copy_fix" 인 경우 실행"""
    if text == CopyFixTarget.PREV.value:
        await handle_start_event(user_id)
        return

    if text in CopyFixTarget.NEW.value:
        context = session["context"]
        context[Step.FIX_TARGET.value] = text
        upsert_session(user_id=user_id, step=Step.MANUAL_FIX.value, context=context)
        await post_to_works(
            payload=set_text_payload("IMC 가이드라인을 적용할 카피를 입력해주세요!"),
            id=user_id,
        )
    elif text == CopyFixTarget.SAVED.value:
        await post_to_works(
            payload=set_text_payload("아직 개발 중인 기능입니다!"),
            id=user_id,
        )
        await post_to_works(
            payload=set_copy_fix_target_payload(),
            id=user_id,
        )
    else:
        await post_to_works(
            payload=set_text_payload(WRONG_INPUT),
            id=user_id,
        )
        await post_to_works(
            payload=set_copy_fix_target_payload(),
            id=user_id,
        )
