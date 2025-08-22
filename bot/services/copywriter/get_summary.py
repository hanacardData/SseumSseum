from bot.logger import logger
from bot.services.openai_client import get_openai_response

_PROMPT = """
아래와 같은 정보를 기반으로, 수행학고자 하는 캠페인의 목적과 타겟을 10글자 이내로 요약해서 전달하세요.
정보:
{task_info}

### 결과 형식:
10글자 이내의 캠페인 목적과 타겟을 요약한 문자열을 출력하십시오.
설명과 이유는 절대로 출력하지 마세요.
"""


async def summarise_context(task_info: dict) -> str | None:
    """OpenAI 모델을 사용해 입력 텍스트에 요약을 반환합니다."""
    prompt = _PROMPT.format(
        task_info=str(task_info),
    )
    try:
        return await get_openai_response(
            prompt="You are a helpful marketer.",
            input=prompt,
        )
    except Exception as e:
        logger.error(f"Error in summarise context: {e}")
        return
