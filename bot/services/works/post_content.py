import httpx
from retry import retry

from bot.logger import logger
from bot.services.works.access_token import set_headers

CHANNEL_POST_URL = (
    "https://www.worksapis.com/v1.0/bots/10608672/channels/{channel_id}/messages"
)
USER_POST_URL = "https://www.worksapis.com/v1.0/bots/10608672/users/{user_id}/messages"


@retry(tries=3, delay=1, backoff=2, exceptions=(httpx.RequestError, httpx.HTTPError))
async def post_to_works(
    payload: dict[str, dict[str, str | list[dict[str, str]]]],
    id: str,
    is_channel: bool = False,
) -> None:
    url = (
        CHANNEL_POST_URL.format(channel_id=id)
        if is_channel
        else USER_POST_URL.format(user_id=id)
    )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=set_headers(), json=payload)
            response.raise_for_status()
            return
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.error(f"Error to post payload to works: {e}")
            raise
