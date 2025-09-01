from bot.services.db.dml import upsert_session
from bot.services.steps_enum import WRONG_ANSWERS, Step
from bot.services.works.payload import set_text_payload
from bot.services.works.post_content import post_to_works

DESCRIPTION = """마지막으로, 진행할 캠페인을 구체적으로 말씀해주세요.
손님의 참여 방법, 제공 혜택 등 핵심 포인트를 알려주시면, 씀씀이가 카피에 쓱쓱 반영해드릴게요!

예시)
하나대학교 신입생 대상 학생증 겸 체크카드 발급 이벤트를 진행할거야. 3월에 발급하면 아메리카노 2잔 기프티콘을 제공할거야.
"""
_WRONG_TARGET = "'{text}' 입력은 이해할 수 없어요. 캠페인 타겟을 다시 입력해주세요."


async def handle_target_input_event(user_id: str, session: dict, text: str) -> None:
    """캠페인 타겟 입력 이벤트, step=="purpose" 인 경우 실행
    text는 캠페인 타겟
    """
    if text in WRONG_ANSWERS:
        await post_to_works(
            payload=set_text_payload(_WRONG_TARGET.format(text=text)), id=user_id
        )
        return
    context = session["context"]
    context[Step.TARGET.value] = text
    upsert_session(user_id=user_id, step=Step.TARGET.value, context=context)
    await post_to_works(payload=set_text_payload(DESCRIPTION), id=user_id)
