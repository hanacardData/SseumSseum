import json
import re


def parse_json(response_text: str) -> dict:
    """
    OpenAI 응답에서 JSON을 안전하게 추출하고 파싱합니다.
    ```
    json
    { ... }
    ```
    이런 코드블록도 처리 가능.
    """
    # ```json ... ``` 또는 ``` ... ``` 제거
    cleaned = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", response_text, flags=re.DOTALL)

    # 앞뒤 공백 제거
    cleaned = cleaned.strip()

    # JSON 파싱
    return json.loads(cleaned)
