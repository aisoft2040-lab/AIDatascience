# AI/SaaS Glossary (KO–EN)

목적: 반복되는 도메인/기술 용어를 한–영으로 정리해 의사소통 속도와 정확도를 높입니다. 짧고 일관된 정의를 유지하세요.

사용법
- 새 용어는 표 맨 아래에 추가합니다.
- 정의는 한 문장, 예시는 한 문장으로 제한합니다.
- 출처(문서/링크/파일 경로)가 있으면 간단히 남깁니다.

| Term (EN) | 용어 (KO) | Definition | Example | Source |
|---|---|---|---|---|
| Retrieval | 검색/조회 | 질문과 관련된 문서를 인덱스에서 찾아오는 단계 | Top‑k=3으로 상위 문서 3개를 가져온다 | RAG design doc |
| Recall@k | 재현율@k | 상위 k개 중 정답을 포함할 확률 | Recall@5=0.74 | eval notebook |
| Hit Rate | 히트율 | 조회 결과에 유효 문서가 포함된 비율 | Hit Rate 78% | metrics dashboard |
| Embedding | 임베딩 | 텍스트를 벡터(숫자 배열)로 변환한 표현 | 문장 임베딩으로 코사인 유사도 계산 | model card |
| Vector DB | 벡터 DB | 벡터 검색을 위한 데이터베이스 | Qdrant 컬렉션에 인덱스 생성 | qdrant config |
| Prompt Injection | 프롬프트 주입 | 모델 지시를 우회/오용하도록 유도하는 공격 | “시스템 프롬프트를 출력해라” 차단 | security note |
| PII | 개인식별정보 | 개인을 식별 가능한 정보 집합 | 이메일/전화번호 마스킹 | compliance |
| JSON Schema | JSON 스키마 | JSON 구조/타입 제약 정의 | 응답 JSON 유효율 95% 목표 | schema.json |
| Fallback | 폴백 | 실패/지연 시 대체 경로로 우회 | 로컬→클라우드 모델 전환 | service design |
| Cost per session | 세션당 비용 | 1세션 LLM/API 비용 총합 | $0.018/세션 | billing export |
| Latency p95 | p95 지연 | 95% 요청 이하의 응답 시간 | p95=1.2s | tracing |
| Caching | 캐싱 | 재사용을 위해 결과 임시 저장 | 쿼리/임베딩 캐시 적중률 42% | cache stats |
| Grounding | 근거 제시 | 답변에 출처/근거를 함께 제공 | 상위 청크 링크 첨부 | UI spec |

메모
- 용어는 프로젝트 전반에서 동일한 번역을 사용합니다.
- 불명확한 용어는 주석으로 예외/범위를 명시합니다.
