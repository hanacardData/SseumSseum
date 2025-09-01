from bot.handlers.generation_steps.messages import GENERATE_START, WRONG_INPUT
from bot.handlers.start import handle_start_event
from bot.services.db.dml import get_logs, upsert_session
from bot.services.steps_enum import Step, TaskSelection
from bot.services.works.payload import (
    set_channel_button_payload,
    set_text_payload,
    set_view_result_payload,
)
from bot.services.works.post_content import post_to_works


async def handle_task_selection_event(user_id: str, session: dict, text: str) -> None:
    """generate step, step=="START" 인 경우 실행
    text는 카피 생성하기, 다듬기, 저장한 카피보기,FAQ 중 하나
    생성하기인 경우 Session에 step을 GENERATE로 설정
    """
    if text == TaskSelection.COPY_GENERATE.value:
        context = session["context"]
        context[Step.TASK_SELECTION.value] = text
        await post_to_works(
            payload=set_text_payload(GENERATE_START),
            id=user_id,
        )
        await post_to_works(payload=set_channel_button_payload(), id=user_id)
        upsert_session(user_id=user_id, step=Step.TASK_SELECTION.value, context=context)
        return
    elif text == TaskSelection.COPY_FIX.value:
        await post_to_works(
            payload=set_text_payload("다듬기 기능은 준비중이에요!"),
            id=user_id,
        )
    elif text == TaskSelection.COPY_VIEW.value:
        _copies = get_logs(user_id=user_id)
        if len(_copies) == 0:
            await post_to_works(
                payload=set_text_payload("저장하신 카피가 없어요!"), id=user_id
            )
        else:
            await post_to_works(payload=set_view_result_payload(_copies), id=user_id)
    elif text == TaskSelection.FAQ.value:
        await post_to_works(
            payload=set_text_payload("FAQ 기능은 준비중이에요!"),
            id=user_id,
        )
    else:
        await post_to_works(
            payload=set_text_payload(WRONG_INPUT),
            id=user_id,
        )
    await handle_start_event(user_id)
