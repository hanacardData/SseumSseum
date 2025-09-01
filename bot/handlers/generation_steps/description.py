from bot.handlers.generation_steps.core import generate_copy
from bot.services.steps_enum import WRONG_ANSWERS, Step
from bot.services.works.payload import set_restart_button_payload, set_text_payload
from bot.services.works.post_content import post_to_works

_WRONG_DESCRIPTION = (
    "'{text}' 입력은 이해할 수 없어요. 캠페인 설명을 다시 입력해주세요."
)


async def handle_description_input_event(
    user_id: str, session: dict, text: str
) -> None:
    """캠페인 설명 입력 이벤트, step=="purpose" 인 경우 실행
    text는 캠페인 설명
    선택한 캠페인 설명에 따라 Session에 step="description"로 설정
    이후 다시 start step으로 돌아가게 함
    """
    if text in WRONG_ANSWERS:
        await post_to_works(
            payload=set_text_payload(_WRONG_DESCRIPTION.format(text=text)), id=user_id
        )
        return
    context = session["context"]
    context[Step.DESCRIPTION.value] = text
    await generate_copy(user_id=user_id, context=context)
    await post_to_works(payload=set_restart_button_payload(), id=user_id)
