TONE_STRATEGY_SELECTION_PROMPT: str = """
아래와 같은 정보를 기반으로, 가장 적합한 톤과 전략을 선택하세요.

정보:
{context}

tone과 strategy는 반드시 아래 목록 중 하나만 출력해야 합니다.

출력 가능한 톤: {tone_candidates}

출력 가능한 전략: {strategy_candidates}

톤과 전략을 선택하면서 생각한 의견을 담은 메시지(예를 들면, "손님이 공감할 수 있도록 ....하게", "음.. ...한 느낌을 전달하려면" 등)는 존댓말로 작성해야 합니다.
톤과 전략, 선택의 이유를 담은 메시지는 각각의 필드에 작성해야 합니다.

### 결과 형식:
아래와 같은 형식으로, 다른 텍스트를 제외한 JSON만 출력하십시오.
tone, strategy, tone_reasoning, strategy_reasoning 외에는 다른 설명이나 텍스트를 출력하지 마십시오.

{{
    "tone": "{{ 선택된 톤 }}",
    "strategy": "{{ 선택된 전략 }}",
    "tone_reasoning": "{{ 톤 선택 과정의 이유}}",
    "strategy_reasoning": "{{ 전략 선택 과정의 이유 }}"
}}
"""
