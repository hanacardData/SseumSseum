import json

from bot.services.steps_enum import Channel, Purpose, TaskSelection


def set_text_payload(message: str) -> dict[str, dict[str, str]]:
    return {"content": {"type": "text", "text": message}}


def set_task_selection_image_carousel_payload() -> dict[str, dict]:
    return {
        "content": {
            "type": "image_carousel",
            "columns": [
                {
                    "originalContentUrl": "https://static.worksmobile.net/static/wm/botprofile/Bot_General_640.png",
                    "action": {
                        "type": "message",
                        "label": TaskSelection.COPY_GENERATE.value,
                        "text": TaskSelection.COPY_GENERATE.value,
                    },
                },
                {
                    "originalContentUrl": "https://static.worksmobile.net/static/wm/botprofile/Bot_General_640.png",
                    "action": {
                        "type": "message",
                        "label": TaskSelection.COPY_FIX.value,
                        "text": TaskSelection.COPY_FIX.value,
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


def set_copy_result_payload(copy_result: dict):
    carousel_payload = {"type": "carousel", "contents": []}
    phrases = copy_result.get("phrases")
    context = copy_result.get("context")
    for _, phrase in phrases.items():
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": phrase["title"],
                        "wrap": True,
                        "weight": "bold",
                        "size": "sm",
                        "color": "#000000",
                    }
                ],
            },
            "body": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": phrase["content"],
                        "wrap": True,
                        "size": "sm",
                        "color": "#000000",
                    }
                ],
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "저장하기",
                        "action": {
                            "type": "postback",
                            "data": json.dumps(
                                {k: context[k] for k in ["channel", "purpose"]}
                                | phrase,
                                ensure_ascii=False,
                            ),
                        },
                        "size": "sm",
                        "align": "center",
                        "style": "normal",
                        "color": "#157efb",
                    }
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
