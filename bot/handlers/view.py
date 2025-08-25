from bot.services.db.dml import get_logs
from bot.services.works.payload import (
    set_copy_result_payload,
    set_restart_button_payload,
    set_text_payload,
)
from bot.services.works.post_content import post_to_works


async def handle_view_event(user_id: str) -> None:
    """start step,
    카피 생성하기, 카피 다듬기 선택지, 저장한 카피 보기를 송신
    Session에 step을 START로 설정, context는 빈 딕셔너리로 초기화
    """
    _copies = get_logs(user_id=user_id)
    if len(_copies) == 0:
        await post_to_works(
            payload=set_text_payload("저장하신 카피가 없어요!"), id=user_id
        )
    else:
        await post_to_works(payload=set_copy_result_payload(_copies), id=user_id)
    await post_to_works(payload=set_restart_button_payload(), id=user_id)
