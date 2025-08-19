import random

from bot.logger import logger
from bot.services.copywriter.prompt.copytone import COPY_TONE_MAPPER
from bot.services.copywriter.prompt.message import MESSAGE_PROPMT
from bot.services.copywriter.prompt.strategy import COPY_STRATEGY_MAPPER
from bot.services.copywriter.refine_copy import parse_json
from bot.services.openai_client import get_openai_response
from bot.services.steps_enum import Step

_PROMPT = """
아래와 같은 정보를 기반으로, 가장 적합한 톤과 전략을 선택하세요.

정보:
{task_info}

tone과 strategy는 반드시 아래 목록 중 하나만 출력해야 합니다.

가능한 톤: {tone_candidates}
가능한 전략: {strategy_candidates}

톤과 전략을 선택한 이유를 각각 작성해야 합니다.
또, 이유를 생각하는 과정에서 하는 혼잣말은 따로 작성해야 합니다.


### 결과 형식:
아래와 같은 형식으로만 출력하십시오.
생성된 tone, strategy, tone_reasoning, strategy_reasoning, tone_thoughts, strategy_thoughts 외에는 다른 설명이나 텍스트를 출력하지 마십시오.
반드시 다른 텍스트를 제외한 JSON만 출력하십시오.
반드시 tone, strategy, tone_reasoning, strategy_reasoning, tone_thoughts, strategy_thoughts 만 생성하세요.

{{
    "tone": "{{ 선택된 톤 }}",
    "strategy": "{{ 선택된 전략 }}",
    "tone_reasoning": "{{ 톤 선택 이유 }}",
    "tone_thoughts": "{{ 톤 선택 과정에서의 혼잣말 }}",
    "strategy_reasoning": "{{ 전략 선택 이유 }}",
    "strategy_thoughts": "{{ 전략 선택 과정에서의 혼잣말 }}"
}}
"""


async def suggest_tone_strategy(task_info: dict) -> dict[str, str]:
    """OpenAI 모델을 사용해 입력 텍스트에 어울리는 톤과 전략을 반환합니다."""
    tone_candidates = list(COPY_TONE_MAPPER.keys())
    strategy_candidates = list(COPY_STRATEGY_MAPPER.keys())
    prompt = _PROMPT.format(
        tone_candidates=", ".join(tone_candidates),
        strategy_candidates=", ".join(strategy_candidates),
        task_info=str(task_info),
    )
    try:
        result = await get_openai_response(
            prompt=prompt,
            input=prompt,
        )
        result = parse_json(result)
        print(result)
        if (
            result["tone"] not in tone_candidates
            or "tone_reasoning" not in result
            or "tone_thoughts" not in result
        ):
            result["tone"] = random.choice(tone_candidates)
            result["tone_reasoning"] = (
                f"손님이 공감할 수 있도록 {result['tone']} 톤을 사용했어요."
            )
            result["tone_thoughts"] = f"음.. {result['tone']} 느낌을 전달하려면..."

        if (
            result["strategy"] not in strategy_candidates
            or "strategy_reasoning" not in result
            or "strategy_thoughts" not in result
        ):
            result["strategy"] = random.choice(strategy_candidates)
            result["strategy_reasoning"] = (
                f"손님들의 반응을 이끌어낼수 있도록 {result['strategy']} 포인트를 사용했어요."
            )
            result["strategy_thoughts"] = f"{result['strategy']} 포인트를 사용한다면..."

        return result

    except Exception as e:
        logger.error(f"Error in suggest tone and startegy: {e}")
        tone = random.choice(tone_candidates)
        strategy = random.choice(strategy_candidates)
        return {
            "tone": tone,
            "strategy": strategy,
            "tone_reasoning": f"손님이 공감할 수 있도록 {tone} 톤을 사용했어요.",
            "tone_thoughts": f"음.. {tone} 느낌을 전달하려면...",
            "strategy_reasoning": f"손님들의 반응을 이끌어낼수 있도록 {strategy} 포인트를 사용했어요.",
            "strategy_thoughts": f"{strategy} 포인트를 사용한다면...",
        }


async def suggest_copy(task_info: dict, tone: str, strategy: str) -> str:
    """입력 텍스트에 어울리는 카피를 생성합니다."""
    copy_tone_prompt = COPY_TONE_MAPPER[tone]
    copy_strategy_prompt = COPY_STRATEGY_MAPPER[strategy]

    prompt = MESSAGE_PROPMT.format(
        campaign_purpose=task_info[Step.PURPOSE.value],
        campaign_description=task_info[Step.DESCRIPTION.value],
        target_customer=task_info[Step.TARGET.value],
        copy_tone=copy_tone_prompt,
        copy_strategy=copy_strategy_prompt,
    )

    try:
        result = await get_openai_response(
            prompt="You are a helpful marketer.",
            input=prompt,
        )
        return result
    except Exception as e:
        logger.error(f"Error in suggest_copy: {e}")
        return "카피 생성에 실패했습니다. 다시 시도해주세요."
