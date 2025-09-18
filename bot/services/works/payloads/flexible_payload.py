import re

from bot.services.steps_enum import Channel

_IDX_MAP = {0: "하나", 1: "둘", 2: "셋", 3: "넷", 4: "다섯"}

_CHANNEL_TITLE_HEADER: dict[str, str] = {
    Channel.LMS.value: "(광고)[하나카드]",
    Channel.RCS_LMS.value: "(광고)[하나카드]",
    Channel.RCS_SMS.value: "(광고)[하나카드]",
    Channel.TALK.value: "[하나카드]",
    Channel.PUSH_PAY.value: "(광고)[하나카드](1800-1111)",
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


def set_copy_result_payload(phrases: dict, channel: str) -> dict:
    carousel_payload = {"type": "carousel", "contents": []}
    for idx, (key, phrase) in enumerate(phrases.items()):
        _title = set_title_header(phrase["title"], channel)
        _content = set_content_footer(phrase["content"], channel)
        _copy_text = "\n".join([_title, _content])
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"씀씀이 아이디어 {_IDX_MAP[idx]}!",
                        "size": "sm",
                        "color": "#ffffff",
                        "weight": "bold",
                        "align": "center",
                    }
                ],
                "backgroundColor": "#008e71",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": _title,
                        "wrap": True,
                        "size": "sm",
                        "align": "start",
                        "color": "#333333",
                        "weight": "bold",
                    },
                    {
                        "type": "text",
                        "text": _content,
                        "wrap": True,
                        "size": "sm",
                        "align": "start",
                        "color": "#333333",
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm",
                        "backgroundColor": "#ffffff",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "[이 아이디어의 매력 포인트]",
                                        "size": "sm",
                                        "color": "#333333",
                                        "align": "center",
                                        "weight": "bold",
                                    },
                                    {
                                        "type": "text",
                                        "text": f"- 글자 수 {len(_copy_text)} 자 ({len(_copy_text.encode())} Byte)",
                                        "size": "sm",
                                        "color": "#333333",
                                        "align": "start",
                                        "wrap": True,
                                    },
                                    {
                                        "type": "text",
                                        "text": f"- {phrase['reasoning']}",
                                        "size": "sm",
                                        "color": "#333333",
                                        "align": "start",
                                        "wrap": True,
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "기억해두기",
                        "action": {
                            "type": "postback",
                            "data": key,
                        },
                        "size": "sm",
                        "align": "center",
                        "style": "normal",
                        "color": "#157efb",
                    },
                    {
                        "type": "text",
                        "text": "복사하기",
                        "action": {"type": "copy", "copyText": _copy_text},
                        "size": "sm",
                        "align": "center",
                        "style": "normal",
                        "color": "#157efb",
                    },
                ],
            },
        }
        carousel_payload["contents"].append(bubble)

    last_bubble = {
        "type": "bubble",
        "size": "kilo",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "이제 어떻게 해볼까요?",
                    "size": "sm",
                    "color": "#ffffff",
                    "weight": "bold",
                    "align": "center",
                }
            ],
            "backgroundColor": "#008e71",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "아이디어가 괜찮으셨다면,\n[기억해두기]를 눌러주세요!",
                    "wrap": True,
                    "size": "sm",
                    "align": "start",
                    "color": "#333333",
                },
                {
                    "type": "text",
                    "text": "\n더 다듬고 싶다면,\n[기억해두기] → [새로 시작하기]\n→ [카피 다듬기]로 도와드려요!",
                    "wrap": True,
                    "size": "sm",
                    "align": "start",
                    "color": "#333333",
                },
                {
                    "type": "text",
                    "text": "\n새로운 작업을 원하시면,\n[새로 시작하기]를 눌러주세요!",
                    "wrap": True,
                    "size": "sm",
                    "align": "start",
                    "color": "#333333",
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "새로 시작하기",
                        "text": "시작하기",
                    },
                    "style": "primary",
                    "color": "#0e8366",
                },
            ],
        },
    }
    carousel_payload["contents"].append(last_bubble)
    return {
        "content": {
            "type": "flex",
            "altText": "카피 생성 결과",
            "contents": carousel_payload,
        }
    }


def set_view_result_payload(phrases: list[dict[str, str]]):
    carousel_payload = {"type": "carousel", "contents": []}
    for idx, phrase in enumerate(phrases):
        _title = set_title_header(phrase["title"], phrase["channel"])
        _content = set_content_footer(phrase["content"], phrase["channel"])
        _copy_text = "\n".join([_title, _content])
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"저장한 카피 {_IDX_MAP[idx]}",
                        "size": "sm",
                        "color": "#ffffff",
                        "weight": "bold",
                        "align": "center",
                    }
                ],
                "backgroundColor": "#008e71",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": _title,
                        "wrap": True,
                        "size": "sm",
                        "align": "start",
                        "color": "#333333",
                        "weight": "bold",
                    },
                    {
                        "type": "text",
                        "text": _content,
                        "wrap": True,
                        "size": "sm",
                        "align": "start",
                        "color": "#333333",
                    },
                ],
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "복사하기",
                        "action": {
                            "type": "copy",
                            "copyText": _copy_text,
                        },
                        "size": "sm",
                        "align": "center",
                        "style": "normal",
                        "color": "#157efb",
                    },
                ],
            },
        }
        carousel_payload["contents"].append(bubble)

    last_bubble = {
        "type": "bubble",
        "size": "kilo",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "이제 어떻게 해볼까요?",
                    "size": "sm",
                    "color": "#ffffff",
                    "weight": "bold",
                    "align": "center",
                }
            ],
            "backgroundColor": "#008e71",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "새로운 작업을 원하시면,\n[새로 시작하기]를 눌러주세요!",
                    "wrap": True,
                    "size": "sm",
                    "align": "start",
                    "color": "#333333",
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "새로 시작하기",
                        "text": "시작하기",
                    },
                    "style": "primary",
                    "color": "#0e8366",
                },
            ],
        },
    }
    carousel_payload["contents"].append(last_bubble)

    return {
        "content": {
            "type": "flex",
            "altText": "카피 불러오기 결과",
            "contents": carousel_payload,
        }
    }


def set_manual_fix_payload(phrase: dict[str, str]):
    carousel_payload = {"type": "carousel", "contents": []}
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "수정된 카피",
                    "size": "sm",
                    "color": "#ffffff",
                    "weight": "bold",
                    "align": "center",
                }
            ],
            "backgroundColor": "#008e71",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": phrase["title"],
                    "wrap": True,
                    "size": "sm",
                    "align": "start",
                    "color": "#333333",
                    "weight": "bold",
                },
                {
                    "type": "text",
                    "text": phrase.get("content") or " ",
                    "wrap": True,
                    "size": "sm",
                    "align": "start",
                    "color": "#333333",
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "복사하기",
                    "action": {
                        "type": "copy",
                        "copyText": "\n".join([phrase["title"], phrase["content"]]),
                    },
                    "size": "sm",
                    "align": "center",
                    "style": "normal",
                    "color": "#157efb",
                },
            ],
        },
    }
    carousel_payload["contents"].append(bubble)

    last_bubble = {
        "type": "bubble",
        "size": "kilo",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "이제 어떻게 해볼까요?",
                    "size": "sm",
                    "color": "#ffffff",
                    "weight": "bold",
                    "align": "center",
                }
            ],
            "backgroundColor": "#008e71",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "추가로 수정을 원하시면 채팅창에 입력해주세요!\n새로운 작업을 원하시면,\n[새로 시작하기]를 눌러주세요!",
                    "wrap": True,
                    "size": "sm",
                    "align": "start",
                    "color": "#333333",
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "새로 시작하기",
                        "text": "시작하기",
                    },
                    "style": "primary",
                    "color": "#0e8366",
                },
            ],
        },
    }
    carousel_payload["contents"].append(last_bubble)

    return {
        "content": {
            "type": "flex",
            "altText": "카피 수정하기",
            "contents": carousel_payload,
        }
    }
