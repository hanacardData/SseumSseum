from bot.services.db.dml import upsert_session
from bot.services.steps_enum import Step
from bot.services.works.payload import (
    set_task_selection_image_carousel_payload,
    set_text_payload,
)
from bot.services.works.post_content import post_to_works

_GREETINGS = "어떤 문구가 고민이신가요? 씀씀이와 함께 써봐요!"


async def handle_start_event(user_id: str) -> None:
    """start step,
    카피 생성하기, 카피 다듬기 선택지를 송신
    Session에 step을 START로 설정, context는 빈 딕셔너리로 초기화
    """
    await post_to_works(
        payload=set_text_payload(_GREETINGS),
        id=user_id,
    )
    await post_to_works(payload=set_task_selection_image_carousel_payload(), id=user_id)
    upsert_session(user_id=user_id, step=Step.START.value, context={})
