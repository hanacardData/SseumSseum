import random

from bot.logger import logger
from bot.services.copywriter.get_copy import suggest_copy, suggest_tone_strategy
from bot.services.copywriter.get_summary import summarise_context
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import COPIES, SUMMARY, Step
from bot.services.works.payload import set_copy_result_payload, set_text_payload
from bot.services.works.post_content import post_to_works

_GREETING_TEXTS = [
    "멋진",
    "화려한",
    "창의적인",
    "독창적인",
    "매력적인",
    "흥미로운",
    "눈에 띄는",
    "기발한",
    "인상적인",
    "특별한",
]


async def generate_copy(user_id: str, context: dict) -> None:
    """생성하는 코어 로직"""
    ## 카피 생성 시작
    await post_to_works(
        payload=set_text_payload(
            f"{random.choice(_GREETING_TEXTS)} 카피 작성을 고민하고 있어요!"
        ),
        id=user_id,
    )
    ## 캠페인 요약 생성
    summary = await summarise_context(context)
    if summary:
        await post_to_works(
            payload=set_text_payload(f"'{summary}'를 위해 작성을 준비하시는군요!"),
            id=user_id,
        )
    else:
        await post_to_works(
            payload=set_text_payload("어려운 주제로 문구를 작성하시네요..!"),
            id=user_id,
        )
        summary = ""
    context[SUMMARY] = summary

    ## 톤과 전략 생성
    tone_strategy = await suggest_tone_strategy(context)
    await post_to_works(
        payload=set_text_payload(tone_strategy.tone_thoughts), id=user_id
    )
    await post_to_works(
        payload=set_text_payload(tone_strategy.strategy_thoughts), id=user_id
    )

    ## 카피 생성
    suggest_copy_dict = await suggest_copy(
        task_info=context,
        tone=tone_strategy.tone,
        strategy=tone_strategy.strategy,
    )
    if not suggest_copy_dict:
        await post_to_works(
            payload=set_text_payload(
                "카피 생성에 실패했어요. 다시 시도해주세요."
                + "오류가 반복된다면 데이터 사업부에 문의해주세요."
            ),
            id=user_id,
        )
        return

    ## 카피 결과 전송
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
    context[COPIES] = suggest_copy_dict["phrases"]
    upsert_session(user_id=user_id, step=Step.END.value, context=context)
    return
