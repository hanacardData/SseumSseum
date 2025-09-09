import random

from bot.logger import logger
from bot.services.copywriter.get_copy import suggest_copy, suggest_tone_strategy
from bot.services.copywriter.get_imc_review import refine_copy
from bot.services.db.dml import upsert_session
from bot.services.steps_enum import COPIES, STRATEGY, TONE, Step
from bot.services.works.payload import set_copy_result_payload, set_text_payload
from bot.services.works.post_content import post_to_works

_TEXTS_FOR_GREETING = [
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
    "강렬한",
    "압도적인",
    "극적인",
    "대담한",
    "파격적인",
    "확실한",
    "열정적인",
]

_TEXTS_FOR_CHIILING = [
    "즐거운",
    "설레는",
    "따뜻한",
    "행복한",
    "산뜻한",
    "유쾌한",
    "빛나는",
    "까다로운",
    "심화된",
    "전문적인",
    "심도 있는",
    "도전적인",
]


async def failed_message(user_id: str) -> None:
    await post_to_works(
        payload=set_text_payload(
            "카피 생성에 실패했어요. 다시 시도해주세요."
            + "오류가 반복된다면 데이터 사업부에 문의해주세요."
        ),
        id=user_id,
    )


async def generate_copy(user_id: str, context: dict) -> None:
    """생성하는 코어 로직"""
    ## 카피 생성 시작
    await post_to_works(
        payload=set_text_payload(
            f"{random.choice(_TEXTS_FOR_GREETING)} 카피 작성을 시작해볼까요!"
        ),
        id=user_id,
    )
    await post_to_works(
        payload=set_text_payload(
            f"{random.choice(_TEXTS_FOR_CHIILING)} 주제로 문구를 작성하시네요."
        ),
        id=user_id,
    )

    ## 톤과 전략 생성
    tone_strategy = await suggest_tone_strategy(context)
    await post_to_works(
        payload=set_text_payload(tone_strategy.tone_reasoning), id=user_id
    )
    await post_to_works(
        payload=set_text_payload(tone_strategy.strategy_reasoning), id=user_id
    )

    ## 카피 생성
    suggested_copy = await suggest_copy(
        context=context,
        tone=tone_strategy.tone,
        strategy=tone_strategy.strategy,
    )
    if not suggested_copy:
        await failed_message(user_id=user_id)
        return
    await post_to_works(
        payload=set_text_payload(
            "하나카드의 가이드라인에 맞게 문구를 다듬는 중이에요."
        ),
        id=user_id,
    )
    ## 문구 변경
    refined_copies = await refine_copy(suggested_copy)
    if not refined_copies:
        await failed_message(user_id=user_id)
        return

    ## 카피 결과 전송
    try:
        await post_to_works(
            payload=set_copy_result_payload(
                phrases=refined_copies, channel=context[Step.CHANNEL.value]
            ),
            id=user_id,
        )
    except Exception as e:
        logger.error(f"Error posting copy result: {e}")
        logger.error(
            f"{set_copy_result_payload(phrases=refined_copies, channel=context[Step.CHANNEL.value])}"
        )
        await post_to_works(
            payload=set_text_payload(str(refined_copies["phrases"])),
            id=user_id,
        )

    context[TONE] = tone_strategy.tone
    context[STRATEGY] = tone_strategy.strategy
    context[COPIES] = refined_copies
    upsert_session(user_id=user_id, step=Step.END.value, context=context)
    return
