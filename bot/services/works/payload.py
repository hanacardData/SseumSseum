from bot.services.steps_enum import Channel, Purpose, Start


def set_text_payload(message: str) -> dict[str, dict[str, str]]:
    return {"content": {"type": "text", "text": message}}


def set_initial_image_carousel_payload() -> dict[str, dict]:
    return {
        "content": {
            "type": "image_carousel",
            "columns": [
                {
                    "originalContentUrl": "https://static.worksmobile.net/static/wm/botprofile/Bot_General_640.png",
                    "action": {
                        "type": "message",
                        "label": Start.COPY_GENERATE.value,
                        "text": Start.COPY_GENERATE.value,
                    },
                },
                {
                    "originalContentUrl": "https://static.worksmobile.net/static/wm/botprofile/Bot_General_640.png",
                    "action": {
                        "type": "message",
                        "label": Start.COPY_FIX.value,
                        "text": Start.COPY_FIX.value,
                    },
                },
            ],
        }
    }


def set_channel_button_payload():
    return {
        "content": {
            "type": "button_template",
            "contentText": "첫번째로, 카피를 담을 채널을 선택해주세요!",
            "actions": [
                {
                    "type": "message",
                    "label": Channel.PUSH,
                },
                {
                    "type": "message",
                    "label": Channel.LMS,
                },
                {
                    "type": "message",
                    "label": Channel.SMS,
                },
                {
                    "type": "message",
                    "label": Channel.TALK,
                },
            ],
        }
    }


def set_campagin_purpose_button_payload():
    return {
        "content": {
            "type": "button_template",
            "contentText": "두번째로, 캠페인 목적을 선택해주세요!",
            "actions": [
                {
                    "type": "message",
                    "label": Purpose.CARD_ISSUE,
                },
                {
                    "type": "message",
                    "label": Purpose.CARD_USE,
                },
                {
                    "type": "message",
                    "label": Purpose.CARD_RENEWAL,
                },
                {
                    "type": "message",
                    "label": Purpose.APP_SIGNUP,
                },
                {
                    "type": "message",
                    "label": Purpose.APP_USE,
                },
                {
                    "type": "message",
                    "label": Purpose.APP_FEATURE_USE,
                },
                {
                    "type": "message",
                    "label": Purpose.EVENT_JOIN,
                },
                {
                    "type": "message",
                    "label": Purpose.SURVEY,
                },
                {
                    "type": "message",
                    "label": Purpose.PRODUCT_RECOMMEND,
                },
            ],
        }
    }
