from bot.handlers.generation_steps.messages import CHANNEL_GUIDE, PURPOSE_GUIDE
from bot.services.steps_enum import Channel, Purpose, TaskSelection
from bot.services.works.set_payload_header_footer import (
    IDX_MAP,
    set_content_footer,
    set_title_header,
)


def set_text_payload(message: str) -> dict[str, dict[str, str]]:
    return {"content": {"type": "text", "text": message}}


def set_task_selection_image_carousel_payload() -> dict[str, dict]:
    return {
        "content": {
            "type": "image_carousel",
            "columns": [
                {
                    "originalContentUrl": "https://i.imgur.com/09crFe5.png",
                    "action": {
                        "type": "message",
                        "label": TaskSelection.COPY_GENERATE.value,
                        "text": TaskSelection.COPY_GENERATE.value,
                    },
                },
                {
                    "originalContentUrl": "https://i.imgur.com/QnJNPD9.png",
                    "action": {
                        "type": "message",
                        "label": TaskSelection.COPY_FIX.value,
                        "text": TaskSelection.COPY_FIX.value,
                    },
                },
                {
                    "originalContentUrl": "https://i.imgur.com/3j29wQx.png",
                    "action": {
                        "type": "message",
                        "label": TaskSelection.COPY_VIEW.value,
                        "text": TaskSelection.COPY_VIEW.value,
                    },
                },
                {
                    "originalContentUrl": "https://i.imgur.com/Fb7wlVX.png",
                    "action": {
                        "type": "message",
                        "label": TaskSelection.FAQ.value,
                        "text": TaskSelection.FAQ.value,
                    },
                },
            ],
        }
    }


def set_channel_button_payload(content_text: str = CHANNEL_GUIDE) -> dict[str, dict]:
    return {
        "content": {
            "type": "button_template",
            "contentText": content_text,
            "actions": [
                {"type": "message", "label": channel.value} for channel in Channel
            ],
        }
    }


def set_campagin_purpose_button_payload(
    content_text: str = PURPOSE_GUIDE,
) -> dict[str, dict]:
    return {
        "content": {
            "type": "button_template",
            "contentText": content_text,
            "actions": [
                {"type": "message", "label": purpose.value} for purpose in Purpose
            ],
        }
    }


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
                        "text": f"씀씀이 아이디어 {IDX_MAP[idx]}!",
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
                                        "text": f"- 글자 수 {len(_copy_text)} 자",
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
                        "text": f"저장한 카피 {IDX_MAP[idx]}",
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


def set_restart_button_payload() -> dict[str, dict]:
    return {
        "content": {
            "type": "button_template",
            "contentText": "새로운 작업을 시작하시겠어요? 시작하시려면 아래버튼을 눌러주세요! 저장하지 않은 모든 내용은 사라져요.",
            "actions": [
                {
                    "type": "message",
                    "text": "시작하기",
                    "label": "새로 시작하기",
                },
            ],
        }
    }
