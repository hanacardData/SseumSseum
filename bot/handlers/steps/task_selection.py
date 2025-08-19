from bot.handlers.steps.start import handle_start_event
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Step, TaskSelection
from bot.services.works.payload import (
    set_channel_button_payload,
    set_text_payload,
)
from bot.services.works.post_content import post_to_works
from bot.services.works.written_message import GENERATE


async def handle_task_selection_event(user_id: str, session: dict, text: str) -> None:
    """generate step, step=="START" 인 경우 실행
    text는 카피 생성하기, 다듬기 중 하나
    생성하기인 경우 Session에 step을 GENERATE로 설정
    """
    if text == TaskSelection.COPY_GENERATE.value:
        context = session["context"]
        context[Step.TASK_SELECTION.value] = text
        await post_to_works(
            payload=set_text_payload(GENERATE),
            id=user_id,
        )
        await post_to_works(payload=set_channel_button_payload(), id=user_id)

        upsert_session(user_id=user_id, step=Step.TASK_SELECTION.value, context=context)
    elif text == TaskSelection.COPY_FIX.value:
        await post_to_works(
            payload=set_text_payload("다듬기 기능은 준비중이에요!"),
            id=user_id,
        )
        await handle_start_event(user_id)
    else:
        await post_to_works(
            payload=set_text_payload("잘못된 입력입니다. 다시 시도해주세요."),
            id=user_id,
        )
        await handle_start_event(user_id)
