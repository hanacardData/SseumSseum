from bot.handlers.steps.start import handle_start_event
from bot.logger import logger
from bot.services.copywriter.get_copy import suggest_copy, suggest_tone_strategy
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Step
from bot.services.works.payload import set_copy_result_payload, set_text_payload
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
    await post_to_works(
        payload=set_text_payload("멋진 카피 작성을 고민하고 있어요!"), id=user_id
    )
    # await post_to_works(payload=set_text_payload(str(context)), id=user_id) # 디버깅용
    tone_strategy = await suggest_tone_strategy(context)
    await post_to_works(
        payload=set_text_payload(tone_strategy.tone_thoughts), id=user_id
    )
    await post_to_works(
        payload=set_text_payload(tone_strategy.strategy_thoughts), id=user_id
    )
    suggest_copy_dict = await suggest_copy(
        task_info=context,
        tone=tone_strategy.tone,
        strategy=tone_strategy.strategy,
    )
    if not suggest_copy_dict:
        await post_to_works(
            payload=set_text_payload(
                "카피 생성에 실패했어요. 다시 시도해주세요."
                + "만약 오류가 반복된다면 데이터 사업부에 문의해주세요."
            ),
            id=user_id,
        )
        await handle_start_event(user_id=user_id)
        return

    try:
        await post_to_works(
            payload=set_copy_result_payload(suggest_copy_dict),
            id=user_id,
        )
    except Exception as e:
        logger.error(f"Error posting copy result: {e}")
        logger.error(f"{set_copy_result_payload(suggest_copy_dict)}")
        await post_to_works(
            payload=set_text_payload(str(suggest_copy_dict["phrases"])),
            id=user_id,
        )
        await handle_start_event(user_id=user_id)
        return
    await handle_start_event(user_id=user_id)
