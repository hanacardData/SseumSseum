TONE_STRATEGY_SELECTION_PROMPT = """
아래와 같은 정보를 기반으로, 가장 적합한 톤과 전략을 선택하세요.

정보:
{task_info}

tone과 strategy는 반드시 아래 목록 중 하나만 출력해야 합니다.

가능한 톤: {tone_candidates}
가능한 전략: {strategy_candidates}

톤과 전략을 선택한 이유를 각각 작성해야 하며, 적절한 톤과 전략을 생각하면서 할 수 있는 메시지
(예를 들면, "손님이 공감할 수 있도록 ...톤을 사용했어요.", "음.. ...한 느낌을 전달하려면")는 따로 작성해야 합니다.
톤과 전략의 이유와 생각 과정 메시지는 존댓말로 각각의 필드에 작성해야 합니다.

### 결과 형식:
아래와 같은 형식으로만 출력하십시오.
생성된 tone, strategy, tone_reasoning, strategy_reasoning, tone_thoughts, strategy_thoughts 외에는 다른 설명이나 텍스트를 출력하지 마십시오.
반드시 다른 텍스트를 제외한 JSON만 출력하십시오.
반드시 tone, strategy, tone_reasoning, strategy_reasoning, tone_thoughts, strategy_thoughts 만 생성하세요.

{{
    "tone": "{{ 선택된 톤 }}",
    "strategy": "{{ 선택된 전략 }}",
    "tone_reasoning": "{{ 톤 선택 이유 }}",
    "tone_thoughts": "{{ 톤 선택 과정에서의 메시지}}",
    "strategy_reasoning": "{{ 전략 선택 이유 }}",
    "strategy_thoughts": "{{ 전략 선택 과정에서의 메시지 }}"
}}
"""
