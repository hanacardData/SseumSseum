from enum import Enum

INITIAL_CONTACT: str = "시작하기"
COPIES: str = "copies"
VIEW: str = "기억한 카피 보기"


class Step(str, Enum):
    START = "start"
    TASK_SELECTION = "task_selection"
    CHANNEL = "channel"
    PURPOSE = "purpose"
    TARGET = "target"
    DESCRIPTION = "description"
    END = "end"


class TaskSelection(str, Enum):
    COPY_GENERATE = "카피 생성하기"
    COPY_FIX = "카피 다듬기"
    COPY_VIEW = "기억한 카피 보기"
    FAQ = "FAQ"


class Channel(str, Enum):
    PUSH = "PUSH 메시지"
    LMS = "LMS"
    SMS = "SMS"
    TALK = "알림톡"
    PREV = "생성 단계로 돌아가기"


class Purpose(str, Enum):
    CARD_ISSUE = "카드 발급 유도"
    CARD_USE = "카드 사용 유도"
    CARD_RENEWAL = "카드 갱신 유도"
    APP_SIGNUP = "앱 가입 유도"
    APP_USE = "앱 사용 유도"
    APP_FEATURE_USE = "앱 특정 기능 사용"
    EVENT_JOIN = "이벤트 응모"
    SURVEY = "만족도 조사"
    PRODUCT_RECOMMEND = "특정 상품 권유"
    PREV = "채널 선택 단계로 돌아가기"
