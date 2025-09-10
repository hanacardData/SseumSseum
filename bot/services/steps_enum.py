from enum import Enum

INITIAL_CONTACT: str = "시작하기"
COPIES: str = "copies"
TONE: str = "tone"
STRATEGY: str = "strategy"


class Step(str, Enum):
    START = "start"
    COPY_GENERATION = "copy_generation"
    COPY_FIX = "copy_fix"
    ### Generation steps
    CHANNEL = "channel"
    PURPOSE = "purpose"
    TARGET = "target"
    DESCRIPTION = "description"
    END = "end"

    ### FIX Steps
    FIX_TARGET = "fix_target"


class TaskSelection(str, Enum):
    COPY_GENERATE = "카피 만들기"
    COPY_FIX = "카피 다듬기"
    COPY_VIEW = "이전 카피 보기"
    FAQ = "FAQ"


class Channel(str, Enum):
    LMS = "LMS"
    RCS_LMS = "RCS (LMS)"
    RCS_SMS = "RCS (SMS)"
    TALK = "알림톡"
    PUSH_PAY = "PUSH (하나페이)"
    PUSH_MONEY = "PUSH (하나머니)"
    PREV = "작업 선택 단계로 돌아가기"


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


WRONG_ANSWERS: set[str] = {INITIAL_CONTACT} | {
    m.value for enum in (TaskSelection, Channel, Purpose) for m in enum
}


class CopyFixTarget(str, Enum):
    SAVED = "저장된 카피 선택하기"
    NEW = "직접 입력하기"
    PREV = "작업 선택 단계로 돌아가기"
