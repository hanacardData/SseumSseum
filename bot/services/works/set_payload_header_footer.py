import re

from bot.services.steps_enum import Channel

IDX_MAP = {0: "하나", 1: "둘", 2: "셋", 3: "넷", 4: "다섯"}

_CHANNEL_TITLE_HEADER: dict[str, str] = {
    Channel.LMS.value: "(광고)[하나카드]",
    Channel.RCS_LMS.value: "(광고)[하나카드]",
    Channel.RCS_SMS.value: "(광고)[하나카드]",
    Channel.TALK.value: "[하나카드]",
    Channel.PUSH_PAY.value: "(광고)[하나카드] (1800-1111)",
    Channel.PUSH_MONEY.value: "(광고)[하나카드](1800-1111)",
}

_CHANNEL_CONTENT_FOOTER: dict[str, str] = {
    Channel.LMS.value: """
*************************
※ 유의사항
-
▶

준법심의 S-00-0000 (2025.00.00~2025.00.00)""",
    Channel.RCS_LMS.value: """
*************************
※ 유의사항
-
▶

준법심의 S-00-0000 (2025.00.00~2025.00.00)
무료 수신거부 [080-890-1155]""",
    Channel.RCS_SMS.value: """
준법심의 S-00-0000(2025.00.00~2025.00.00)
무료 수신거부 0808901155""",
    Channel.TALK.value: """
*************************""",
    Channel.PUSH_PAY.value: """
*************************
-
▶
준법심의 S-00-0000 (2025.00.00~2025.00.00)
* 수신거부 : 전체→설정→알림설정→이벤트/마케팅 알림수신→해제""",
    Channel.PUSH_MONEY.value: """
*************************
-
▶
준법심의 S-00-0000 (2025.00.00~2025.00.00)
수신거부 : 우측 상단 [설정] → 혜택/이벤트 → OFF""",
}


def set_title_header(title: str, channel: str) -> str:
    return f"{_CHANNEL_TITLE_HEADER[channel]}{title}"


def set_content_footer(content: str, channel: str) -> str:
    _content = re.sub(r"\s*◆", r"\n◆", content)
    return f"{_content}{_CHANNEL_CONTENT_FOOTER[channel]}"
