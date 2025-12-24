# SseumSseum
네이버웍스 씀씀이
* 하나카드 직원용 서비스로, 캠페인 내용을 입력하면 이에 적합한 카피가 LLM 기반으로 생성되는 봇.
* 행동경제학, 사회심리학을 기반으로 광고 효과가 보장된 카피 전략이 반영될 수 있게 구성. 


## Demo
<div align="left">
  <table>
    <tr>
      <td align="left">
        <video src="https://github.com/user-attachments/assets/62eba505-7156-46a2-9a6a-5bbc8476b560" width="100%"></video>
      </td>
    </tr>
  </table>
</div>

## 실행 명령어
개발환경
```bash
uvicorn bot.main:app --reload --host 0.0.0.0 --port 5000
```

운영환경
```bash
uvicorn bot.main:app --host 0.0.0.0 --port 5000
```
