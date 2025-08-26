import random

from pydantic import BaseModel, Field, field_validator
from retry import retry

from bot.logger import logger
from bot.services.copywriter.prompt.copytone import COPY_TONE_MAPPER
from bot.services.copywriter.prompt.message import MESSAGE_PROPMT
from bot.services.copywriter.prompt.strategy import COPY_STRATEGY_MAPPER
from bot.services.copywriter.prompt.tone_strategy_selection import (
    TONE_STRATEGY_SELECTION_PROMPT,
)
from bot.services.copywriter.refine_copy import parse_json
from bot.services.openai_client import get_openai_response
from bot.services.steps_enum import Step


class SuggestedToneStrategy(BaseModel):
    tone: str
    strategy: str
    tone_reasoning: str = Field(default="")
    tone_thoughts: str = Field(default="")
    strategy_reasoning: str = Field(default="")
    strategy_thoughts: str = Field(default="")

    @field_validator("tone")
    def validate_tone(cls, v, values):
        if v not in COPY_TONE_MAPPER:
            v = random.choice(list(COPY_TONE_MAPPER.keys()))
            values["tone_reasoning"] = f"손님이 공감할 수 있도록 {v} 톤을 사용했어요."
            values["tone_thoughts"] = f"음.. {v} 느낌을 전달하려면..."
        return v

    @field_validator("strategy")
    def validate_strategy(cls, v, values):
        if v not in COPY_STRATEGY_MAPPER:
            v = random.choice(list(COPY_STRATEGY_MAPPER.keys()))
            values["strategy_reasoning"] = (
                f"손님들의 반응을 이끌어낼수 있도록 {v} 포인트를 사용했어요."
            )
            values["strategy_thoughts"] = f"{v} 포인트를 사용한다면..."
        return v


async def suggest_tone_strategy(task_info: dict) -> SuggestedToneStrategy:
    """입력 텍스트에 어울리는 톤과 전략을 SuggestedToneStrategy 객체로 반환합니다."""
    tone_candidates = list(COPY_TONE_MAPPER.keys())
    strategy_candidates = list(COPY_STRATEGY_MAPPER.keys())
    prompt = TONE_STRATEGY_SELECTION_PROMPT.format(
        tone_candidates=", ".join(tone_candidates),
        strategy_candidates=", ".join(strategy_candidates),
        task_info=str(task_info),
    )
    try:
        result = await get_openai_response(
            prompt="You are a helpful marketer.",
            input=prompt,
        )
        parsed = parse_json(result)
        if not parsed:
            logger.error("Failed to parse OpenAI response.")
            raise Exception("Parsing error in OpenAI response.")
        return SuggestedToneStrategy(**parsed)
    except Exception as e:
        logger.error(f"Error in suggest tone and strategy: {e}")
        return SuggestedToneStrategy(
            tone=random.choice(tone_candidates),
            strategy=random.choice(strategy_candidates),
        )


@retry(tries=3, delay=1, backoff=2, exceptions=Exception)
async def suggest_copy(task_info: dict, tone: str, strategy: str) -> str | None:
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
        return await get_openai_response(
            prompt="You are a helpful marketer.",
            input=prompt,
        )
    except Exception as e:
        logger.error(f"Error in suggest_copy: {e}")
        return
