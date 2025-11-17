# Job Note (2025-11-17) – Week1 Day1 중간 상태

## 1. 완료된 사항
- Git 초기화 및 원격(`origin`) 연결 + 첫 push.
- 개발/학습 로드맵 확장: Week0 요약 박스, Functional Spec(블로그 커리큘럼 목적 포함), 영어 지원 문서(`docs/glossary.md`, `docs/phrases.md`).
- 에이전트 지침 파일: `.github/copilot-instructions.md`.
- PR 템플릿: `templates/PR_TEMPLATE.md`.
- `chat_1.md` 를 `docs/` 로 이동.
- Week1 스캐폴드: FastAPI 앱(`/health`, `/echo`), 기본 테스트 2개, `Dockerfile`, `.env.example`, `requirements.in`.
- Week2 평가 하네스: `eval/metrics.py` (precision/recall/f1, recall@k, batch 함수), `notebooks/eval_demo.ipynb`.
- Day1 강의 노트 생성: `day1/lecture_notes.md`.

## 2. 미완료 (Day1 목표 대비)
- CSV → JSON 유틸 `src/utils/csv_to_json.py`.
- 테스트 `tests/test_csv_to_json.py`.
- `/echo` 입력 검증(허용 문자/길이) 적용.
- 로깅 초기화(`logging.basicConfig`).
- `.env` 실제 파일 생성 및 `APP_VERSION` 적용 확인.
- 추가 테스트로 총 ≥3개 확보.

## 3. 다음 세션 재시작 체크리스트
1. 가상환경 활성화
   ```cmd
   .\.venv\Scripts\activate
   ```
2. 패키지 재설치(필요시)
   ```cmd
   uv pip install -r requirements.txt
   ```
3. 기존 테스트 실행
   ```cmd
   pytest -q
   ```
4. 남은 구현 순서
   - A) `src/utils/csv_to_json.py`
   - B) `tests/test_csv_to_json.py`
   - C) `/echo` 입력 검증 함수 + 400 에러 처리
   - D) 로깅 설정 추가
   - E) `.env` 생성 후 `/health` 버전 반영
   - F) 커밋 & 푸시

## 4. 코드 스니펫 (참고)
CSV 유틸:
```python
import csv
from typing import List, Dict

def csv_to_json(path: str) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
```

테스트:
```python
from src.utils.csv_to_json import csv_to_json
import tempfile

def test_csv_to_json_basic():
    data = "name,age\nAlice,30\nBob,25\n"
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as tmp:
        tmp.write(data)
        tmp.flush()
        rows = csv_to_json(tmp.name)
    assert rows == [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
```

입력 검증:
```python
ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,?!-_()")
MAX_LEN = 500

def is_safe(text: str) -> bool:
    return len(text) <= MAX_LEN and all(c in ALLOWED_CHARS for c in text)
```

적용 예:
```python
from fastapi import HTTPException

@app.post("/echo")
def echo(payload: EchoIn):
    if not is_safe(payload.message):
        raise HTTPException(status_code=400, detail="invalid characters or length")
    return {"message": payload.message}
```

로깅:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("week1")
logger.info("startup complete")
```

## 5. 커밋 & 푸시 명령 (예시)
```cmd
git add src/utils/csv_to_json.py tests/test_csv_to_json.py Grok-AI-Engineer-5Months/01_Week1_FastAPI_Chatbot/src/main.py .env jobnote.md
git commit -m "feat(week1/day1): add csv util, input validation, logging"
git push origin main
```

## 6. 주의 사항
- 가상환경 비활성 상태에서 설치 금지.
- 허용 문자 세트 필요시 확장(국문 입력 고려 등).
- 빈 CSV 처리 테스트 추가 권장.

## 7. Day2 예고
- Ollama 설치 & 로컬 모델 pull.
- Fallback 구현 (timeout/exception → Groq).
- latency 측정(`time.perf_counter`).
- 토큰 비용 추정 함수 골격.

## 8. Week2 준비 메모
- PDF → 청크 → 임베딩 → in-memory ranking 뒤 recall@k 측정 연계.
- 평가 리포트 초안 템플릿 만들기.

## 9. 빠른 실행 명령
```cmd
\.venv\Scripts\activate
pytest -q
python -m uvicorn src.main:app --reload --port 8000
curl http://localhost:8000/health
curl -X POST http://localhost:8000/echo -H "Content-Type: application/json" -d "{\"message\":\"hello\"}"
```

## 10. 결정 대기 질문
- 입력 검증에 한글 허용 여부?
- CSV 숫자 자동 캐스팅 필요?
- GitHub Actions 도입 시점 (Week1 즉시 vs Week2)?

---
다음 세션에서 상단 체크리스트 A)부터 진행.