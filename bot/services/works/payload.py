from bot.services.steps_enum import Channel, Purpose, TaskSelection
from bot.services.works.written_message import CHANNEL, PURPOSE


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


def set_channel_button_payload(content_text: str = CHANNEL) -> dict[str, dict]:
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


def set_campagin_purpose_button_payload(content_text: str = PURPOSE) -> dict[str, dict]:
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
