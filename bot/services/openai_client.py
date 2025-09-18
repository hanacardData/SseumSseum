from openai import APIConnectionError, AsyncOpenAI
from retry import retry

from bot.config.settings import settings
from bot.logger import logger

client = AsyncOpenAI(api_key=settings.openai_api_key)


@retry(tries=3, delay=1, backoff=2, exceptions=APIConnectionError)
async def get_openai_response(
    prompt: str,
    input: str,
) -> str:
    try:
        response = await client.responses.create(
            model="gpt-4o",
            instructions=prompt,
            input=input,
        )
        return response.output_text.strip()
    except APIConnectionError as e:
        logger.error(e)
        raise


@retry(tries=3, delay=1, backoff=2, exceptions=APIConnectionError)
async def get_openai_completion_response(
    prompt: str,
    input: str,
) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input},
            ],
            frequency_penalty=0.4,  # 반복 줄임
            presence_penalty=0.4,  # 새로운 표현 유도
            temperature=1.0,  # 창의성 정도 (0=결정적, 1=창의적)
        )

        return response.choices[0].message.content.strip()
    except APIConnectionError as e:
        logger.error(e)
        raise
