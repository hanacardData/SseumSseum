from bot.handlers.steps.start import handle_start_event
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Step
from bot.services.works.payload import set_text_payload
from bot.services.works.post_content import post_to_works


async def handle_description_input_event(
    user_id: str, session: dict, text: str
) -> None:
    """캠페인 설명 입력 이벤트, step=="purpose" 인 경우 실행
    text는 캠페인 설명
    선택한 캠페인 설명에 따라 Session에 step="description"로 설정
    이후 다시 start step으로 돌아가게 함
    """
    context = session["context"]
    context[Step.DESCRIPTION.value] = text
    upsert_session(user_id=user_id, step=Step.DESCRIPTION.value, context=context)
    await post_to_works(payload=set_text_payload(str(context)), id=user_id)
    # FIXME: 생성하기 로직
    await handle_start_event(user_id=user_id)  # loop 처리
