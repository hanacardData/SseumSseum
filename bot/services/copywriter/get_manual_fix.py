from bot.logger import logger
from bot.services.copywriter.change_str_to_json import parse_json
from bot.services.copywriter.prompt.manual_fix import REVIEW_PROMPT
from bot.services.openai_client import get_openai_response


async def manual_fix(copy: str) -> dict:
    """copy 를 imc 가이드라인에 따라 수정합니다."""
    try:
        result = await get_openai_response(
            prompt=REVIEW_PROMPT,
            input=copy,
        )
        parsed = parse_json(result)
        if not parsed:
            logger.error("Failed to parse imc review OpenAI response.")
            parsed = parse_json(copy)
            if not parsed:
                logger.error("Failed to parse copy OpenAI response in suggest_copy.")
                raise Exception("Parsing error in OpenAI response.")

        parsed["title"] = parsed["title"].strip('"{}').strip()
        parsed["content"] = parsed["title"].strip('"{}').strip()
        return parsed
    except Exception as e:
        logger.error(f"Error in refine copy: {e}")
        return
