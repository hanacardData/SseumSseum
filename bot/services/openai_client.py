from logger import logger
from openai import APIConnectionError, AsyncOpenAI
from retry import retry

from bot.config.settings import settings

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
