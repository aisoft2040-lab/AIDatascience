# Meetings & Emails Phrases (실무 스크립트)

목적: 짧고 명확한 영어 문장을 반복 사용해 회의/이메일 생산성을 높입니다.
사용법: 상황별로 골라 붙이고, 숫자/파일 경로/링크만 바꿔 사용하세요.

## Opening / 목적 확인
- "Today I'd like to confirm the goal and the success criteria."
- "My understanding is X. Please correct me if I missed anything."
- "We aim to validate value with a low-cost, safe LLM add-on."

## 요구사항/범위 명확화
- "Could you share two examples of a good outcome and a bad one?"
- "What constraints should we respect? (latency, cost, PII, rollout)"
- "Which users will try the first pilot?"

## 제안/방향성
- "I propose a small PoC: /ask + RAG with top‑k=3 and JSON schema."
- "We can start with local model and fall back to cloud on timeout."
- "Let's add metrics for recall@k, JSON validity, p95 latency, and cost/session."

## 확인/합의
- "Does this plan align with your priorities for this week?"
- "Can we agree on the acceptance criteria and a rollback plan?"
- "I'll share a short summary and next steps after this call."

## 리스크/의존성 제기
- "Main risks: prompt injection, PII exposure, and cost spikes."
- "Mitigation: input filter, PII redaction, caching, and feature flag."
- "Dependencies: access to documents and an evaluation set of 30 Q&A."

## 데이터/문서 요청
- "Please provide 10 sample documents and 30 labeled Q&A by Friday."
- "If possible, a link to any existing guidelines or policies would help."
- "Could we get a small budget token for the pilot?"

## 마무리/다음 단계
- "Action items: I will set up the endpoint and share a dashboard."
- "Let's review metrics in two days and decide on the pilot scope."
- "Thank you—I'll send a summary with links and dates."

## 이메일/PR 한 줄 문구
- "Purpose: Add safe, low-cost LLM retrieval with measurable KPIs."
- "Metrics (before→after): recall@5 58%→74%, p95 2.1s→1.2s, cost −32%."
- "Risks & mitigations are documented; rollback is a single flag flip."
- "Please review acceptance criteria and test results attached."

## 요청/거절·조정
- "Given the constraint, I'd recommend narrowing the scope to A and B."
- "I can deliver X by Friday; Y will require another two days. Is that acceptable?"
- "To keep costs predictable, let's cap tokens and enable caching first."

## 회의 시작/끝 상용구(스크립트)
- "Shall we start? I'll share my screen in a moment."
- "Before we finish, any concerns or blockers from your side?"
- "Thanks all—recording and notes will be shared shortly."

> 목표: 총 30개 이상을 누적하세요. 실제 사용 예시를 추가하면 더 좋습니다.
