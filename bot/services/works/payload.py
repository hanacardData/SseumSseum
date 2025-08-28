import re

from bot.services.steps_enum import Channel, Purpose, TaskSelection

_IDX_MAP = {0: "하나", 1: "둘", 2: "셋", 3: "넷", 4: "다섯"}


def _refine_title(text: str) -> str:
    return f"(광고)[하나카드] {text}"


def _refine_content(text: str) -> str:
    return (
        re.sub(r"\s*◆", r"\n◆", text)
        + "\n◆\n  -\n*************************\n※ 하나카드 고객센터 : 1800-1111\n"
    )


def _set_copy_text(title: str, content: str) -> str:
    return _refine_title(title) + "\n" + _refine_content(content)


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


def set_channel_button_payload(content_text: str) -> dict[str, dict]:
    return {
        "content": {
            "type": "button_template",
            "contentText": content_text,
            "actions": [
                {
                    "type": "message",
                    "label": Channel.PUSH.value,
                },
                {
                    "type": "message",
                    "label": Channel.LMS.value,
                },
                {
                    "type": "message",
                    "label": Channel.SMS.value,
                },
                {
                    "type": "message",
                    "label": Channel.TALK.value,
                },
                {
                    "type": "message",
                    "label": Channel.PREV.value,
                },
            ],
        }
    }


def set_campagin_purpose_button_payload(content_text: str) -> dict[str, dict]:
    return {
        "content": {
            "type": "button_template",
            "contentText": content_text,
            "actions": [
                {
                    "type": "message",
                    "label": Purpose.CARD_ISSUE.value,
                },
                {
                    "type": "message",
                    "label": Purpose.CARD_USE.value,
                },
                {
                    "type": "message",
                    "label": Purpose.CARD_RENEWAL.value,
                },
                {
                    "type": "message",
                    "label": Purpose.APP_SIGNUP.value,
                },
                {
                    "type": "message",
                    "label": Purpose.APP_USE.value,
                },
                {
                    "type": "message",
                    "label": Purpose.APP_FEATURE_USE.value,
                },
                {
                    "type": "message",
                    "label": Purpose.EVENT_JOIN.value,
                },
                {
                    "type": "message",
                    "label": Purpose.SURVEY.value,
                },
                {
                    "type": "message",
                    "label": Purpose.PRODUCT_RECOMMEND.value,
                },
                {
                    "type": "message",
                    "label": Purpose.PREV.value,
                },
            ],
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
                    "label": "다시 시작하기",
                },
            ],
        }
    }


def set_copy_result_payload(phrases: dict):
    carousel_payload = {"type": "carousel", "contents": []}
    for idx, (key, phrase) in enumerate(phrases.items()):
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
                        "text": f"씀씀이 아이디어 {_IDX_MAP[idx]}",
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
                        "text": _refine_title(phrase["title"]),
                        "wrap": True,
                        "size": "sm",
                        "align": "start",
                        "color": "#333333",
                        "weight": "bold",
                    },
                    {
                        "type": "text",
                        "text": _refine_content(phrase["content"]),
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
                                        "text": f"- 글자 수 {len(phrase['title'] + phrase['content'])} 자",
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
                        "action": {
                            "type": "copy",
                            "copyText": _set_copy_text(
                                phrase["title"], phrase["content"]
                            ),
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
                        "text": _refine_title(phrase["title"]),
                        "wrap": True,
                        "size": "sm",
                        "align": "start",
                        "color": "#333333",
                        "weight": "bold",
                    },
                    {
                        "type": "text",
                        "text": _refine_content(phrase["content"]),
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
                            "copyText": _set_copy_text(
                                phrase["title"], phrase["content"]
                            ),
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

    return {
        "content": {
            "type": "flex",
            "altText": "카피 불러오기 결과",
            "contents": carousel_payload,
        }
    }
