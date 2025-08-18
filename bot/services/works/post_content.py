import httpx
from retry import retry

from bot.logger import logger
from bot.services.works.access_token import set_headers
from bot.services.works.variables import CHANNEL_POST_URL, USER_POST_URL


@retry(tries=3, delay=1, backoff=2, exceptions=(httpx.RequestError, httpx.HTTPError))
async def post_to_works(
    payload: dict[str, dict[str, str | list[dict[str, str]]]],
    id: str,
    is_channel: bool = False,
) -> None:
    if is_channel:
        url = CHANNEL_POST_URL.format(channel_id=id)
    else:
        url = USER_POST_URL.format(user_id=id)

    headers = set_headers()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.error(e)
            raise
