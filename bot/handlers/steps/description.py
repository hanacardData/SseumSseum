from bot.handlers.steps.core import generate_copy
from bot.handlers.steps.start import handle_start_event
from bot.services.steps_enum import Step


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
    generate_copy(user_id=user_id, context=context)
    await handle_start_event(user_id=user_id)
