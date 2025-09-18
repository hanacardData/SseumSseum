from bot.services.steps_enum import Purpose

PURPOSE_MAPPER: dict[str, str] = {
    Purpose.CARD_ISSUE.value: "신규 고객에게 신용카드 또는 체크카드를 발급받도록 권장하는 캠페인. 다양한 혜택이나 추가 서비스를 강조해 신규 카드 발급을 장려할 수 있음.",
    Purpose.WELCOME_CARD_USE.value: "신규 가입 고객을 대상으로 환영의 의미로 제공하는 이벤트. 처음 가입한 고객이 카드를 사용하면 일정 혜택을 제공함.",
    Purpose.CARD_USE.value: "고객이 가지고 있는 카드를 더 자주 사용하도록 하는 캠페인. 일정 금액 이상 사용 시 추가 혜택을 제공하는 등의 캠페인이 예시가 됨.",
    Purpose.CARD_RENEWAL.value: "카드의 유효기간이 임박한 고객에게 카드 갱신을 유도하는 캠페인.",
    Purpose.APP_SIGNUP.value: "해당 앱에 가입하지 않은 고객들에게 앱 서비스에 가입하도록 장려하는 캠페인. 가입 혜택이나 특별 이벤트를 통해 유도할 수 있음.",
    Purpose.APP_USE.value: "이미 해당 앱에 가입한 고객을 대상으로 진행. 앱의 특정 기능을 고객이 사용해보도록 유도하는 캠페인. 새로운 이벤트일 수도 있고 루틴하게 진행되는 이벤트일 수도 있음.",
    Purpose.EVENT_JOIN.value: "고객들이 특정 이벤트에 참여하도록 유도하는 캠페인. 이벤트에 참여하고, 직접 응모를 하는 등의 활동이 가능함.",
    Purpose.SURVEY.value: "고객에게 서비스에 대한 만족도를 조사하기 위한 캠페인. 피드백을 받아 서비스 개선에 반영하고, 참여 고객에게 소정의 보상을 제공할 수 있음.",
    Purpose.PRODUCT_RECOMMEND.value: "고객의 관심사나 소비 패턴에 맞는 특정 상품을 추천하거나 권유하는 캠페인.",
}
