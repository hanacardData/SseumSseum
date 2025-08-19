from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Step
from bot.services.works.payload import set_text_payload
from bot.services.works.post_content import post_to_works
from bot.services.works.written_message import DESCRIPTION


async def handle_target_input_event(user_id: str, session: dict, text: str) -> None:
    """캠페인 타겟 입력 이벤트, step=="purpose" 인 경우 실행
    text는 캠페인 타겟
    """
    context = session["context"]
    context[Step.TARGET.value] = text
    upsert_session(user_id=user_id, step=Step.TARGET.value, context=context)
    await post_to_works(payload=set_text_payload(DESCRIPTION), id=user_id)
