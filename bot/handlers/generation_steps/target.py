from bot.handlers.generation_steps.messages import (
    DESCRIPTION_GUIDE,
    REACTION_TO_TARGET,
    TARGET_GUIDE,
    WRONG_INPUT,
)
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import WRONG_ANSWERS, Step
from bot.services.works.payload import set_text_payload
from bot.services.works.post_content import post_to_works


async def handle_target_input_event(user_id: str, session: dict, text: str) -> None:
    """캠페인 타겟 입력 이벤트, step=="purpose" 인 경우 실행
    text는 캠페인 타겟
    """
    if text in WRONG_ANSWERS:
        await post_to_works(payload=set_text_payload(WRONG_INPUT), id=user_id)
        await post_to_works(payload=set_text_payload(TARGET_GUIDE), id=user_id)
        return
    await post_to_works(payload=set_text_payload(REACTION_TO_TARGET), id=user_id)
    context = session["context"]
    context[Step.TARGET.value] = text
    upsert_session(user_id=user_id, step=Step.TARGET.value, context=context)
    await post_to_works(payload=set_text_payload(DESCRIPTION_GUIDE), id=user_id)
