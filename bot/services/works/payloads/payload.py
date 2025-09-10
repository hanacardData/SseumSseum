from bot.handlers.generation_steps.messages import (
    CHANNEL_GUIDE,
    PURPOSE_GUIDE,
    RESTART_GUIDE,
)
from bot.services.steps_enum import Channel, Purpose, TaskSelection


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


def set_channel_button_payload() -> dict[str, dict]:
    return {
        "content": {
            "type": "button_template",
            "contentText": CHANNEL_GUIDE,
            "actions": [
                {"type": "message", "label": channel.value} for channel in Channel
            ],
        }
    }


def set_campagin_purpose_button_payload() -> dict[str, dict]:
    return {
        "content": {
            "type": "button_template",
            "contentText": PURPOSE_GUIDE,
            "actions": [
                {"type": "message", "label": purpose.value} for purpose in Purpose
            ],
        }
    }


def set_restart_button_payload() -> dict[str, dict]:
    return {
        "content": {
            "type": "button_template",
            "contentText": RESTART_GUIDE,
            "actions": [
                {
                    "type": "message",
                    "text": "시작하기",
                    "label": "새로 시작하기",
                },
            ],
        }
    }
