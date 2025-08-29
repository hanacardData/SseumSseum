# SseumSseum
네이버웍스 씀씀이

## 실행 명령어
개발환경
```bash
uvicorn bot.main:app --reload --host 0.0.0.0 --port 5000
```

운영환경
```bash
uvicorn bot.main:app --host 0.0.0.0 --port 5000 --workers 4
```
