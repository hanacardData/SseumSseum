import random

from pydantic import BaseModel
from retry import retry

from bot.logger import logger
from bot.services.copywriter.change_str_to_json import parse_json
from bot.services.copywriter.prompt.copytone import COPY_TONE_MAPPER
from bot.services.copywriter.prompt.message import MESSAGE_PROPMT
from bot.services.copywriter.prompt.strategy import COPY_STRATEGY_MAPPER
from bot.services.copywriter.prompt.tone_strategy_selection import (
    TONE_STRATEGY_SELECTION_PROMPT,
)
from bot.services.openai_client import (
    get_openai_completion_response,
    get_openai_response,
)
from bot.services.steps_enum import Channel, Purpose, Step


class SuggestedToneStrategy(BaseModel):
    tone: str
    strategy: str
    tone_reasoning: str
    strategy_reasoning: str


async def suggest_tone_strategy(context: dict) -> SuggestedToneStrategy:
    """입력 텍스트에 어울리는 톤과 전략을 SuggestedToneStrategy 객체로 반환합니다."""
    tone_candidates = list(COPY_TONE_MAPPER.keys())
    strategy_candidates = list(COPY_STRATEGY_MAPPER.keys())
    prompt = TONE_STRATEGY_SELECTION_PROMPT.format(
        tone_candidates=", ".join(tone_candidates),
        strategy_candidates=", ".join(strategy_candidates),
        context=str(context),
    )
    try:
        result = await get_openai_response(
            prompt="You are a helpful marketer.",
            input=prompt,
        )
        parsed = parse_json(result)
        if not parsed:
            logger.error("Failed to parse OpenAI response in suggest_tone_strategy.")
            raise Exception("Parsing error in OpenAI response.")
        if (
            parsed["tone"] not in tone_candidates
            or parsed["strategy"] not in strategy_candidates
        ):
            logger.error(
                f"Invalid tone or strategy: tone={parsed.get('tone')}, strategy={parsed.get('strategy')}, "
                f"expected tone={tone_candidates}, expected strategy={strategy_candidates}"
            )
            raise ValueError("Invalid tone or strategy provided.")
        return SuggestedToneStrategy(**parsed)
    except Exception as e:
        logger.error(f"Error in suggest tone and strategy: {e}")
        random_tone = random.choice(tone_candidates)
        random_strategy = random.choice(strategy_candidates)
        return SuggestedToneStrategy(
            tone=random_tone,
            strategy=random_strategy,
            tone_reasoning=f"음.. {random_tone} 느낌을 전달하려면...",
            strategy_reasoning=f"{random_strategy} 포인트를 사용한다면...",
        )


CHANNEL_TITLE_BYTE_MAPPER: dict[str, int] = {
    Channel.LMS.value: 24,
    Channel.RCS_LMS.value: 44,
    Channel.RCS_SMS.value: 24,
    Channel.TALK.value: 70,
    Channel.PUSH_PAY.value: 22,
    Channel.PUSH_MONEY.value: 23,
}

CHANNEL_CONTENT_BYTE_MAPPER: dict[str, int] = {
    Channel.LMS.value: 1158,
    Channel.RCS_LMS.value: 1866,
    Channel.RCS_SMS.value: 92,
    Channel.TALK.value: 1866,
    Channel.PUSH_PAY.value: 1211,
    Channel.PUSH_MONEY.value: 640,
}


@retry(tries=3, delay=1, backoff=2, exceptions=Exception)
async def suggest_copy(context: dict, tone: str, strategy: str) -> str | None:
    """입력 텍스트에 어울리는 카피를 생성합니다."""
    copy_tone_prompt = COPY_TONE_MAPPER[tone]
    copy_strategy_prompt = COPY_STRATEGY_MAPPER[strategy]
    content_len_penalty: int = (
        -506 if context[Step.PURPOSE.value] == Purpose.CARD_ISSUE.value else 0
    )
    prompt = MESSAGE_PROPMT.format(
        campaign_purpose=context[Step.PURPOSE.value],
        campaign_description=context[Step.DESCRIPTION.value],
        target_customer=context[Step.TARGET.value],
        copy_tone=copy_tone_prompt,
        copy_strategy=copy_strategy_prompt,
        num_title_byte=CHANNEL_TITLE_BYTE_MAPPER[context[Step.CHANNEL.value]]
        + content_len_penalty,
        num_content_byte=CHANNEL_CONTENT_BYTE_MAPPER[context[Step.CHANNEL.value]]
        + content_len_penalty,
    )

    try:
        return await get_openai_completion_response(
            prompt="You are a helpful marketer.",
            input=prompt,
        )
    except Exception as e:
        logger.error(f"Error in suggest_copy: {e}")
        return
