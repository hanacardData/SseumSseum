import json

from bot.logger import logger
from bot.services.copywriter.prompt.imc import REVIEW_PROMPT
from bot.services.copywriter.refine_copy import parse_json
from bot.services.openai_client import get_openai_response


async def refine_copy(copy: str | dict) -> dict:
    """copy 를 imc 가이드라인에 따라 반환합니다.
    만약 실패할 경우, imc 가이드라인 반영 전의 text를 사용합니다.
    "phrase 1", "phrase 2", ... 형식의 키를 가지며, 각 키는 "title"과 "content"를 포함하는 딕셔너리를 반환합니다.
    """
    if isinstance(copy, dict):
        copy = json.dumps(copy, ensure_ascii=False)
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
        for key, phrase in parsed.items():
            parsed[key]["title"] = phrase["title"].strip('"{}').strip()
            parsed[key]["content"] = phrase["content"].strip('"{}').strip()
        return parsed
    except Exception as e:
        logger.error(f"Error in refine copy: {e}")
        return
