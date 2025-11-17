# Portfolio Metrics Framework

This document defines the standardized framework for measuring quality, cost, and safety across all weekly deliverables.

## Overview

Each deliverable is evaluated across three dimensions with equal weight:
- **Quality Metrics (33%)**: Technical excellence and user value
- **Cost Metrics (33%)**: Operational efficiency and sustainability  
- **Safety Metrics (34%)**: Security, privacy, and responsible AI

## 📊 Quality Metrics

### 1. Code Quality (25% of Quality Score)

#### Metrics
- **Test Coverage**: Percentage of code covered by tests
  - Target: ≥80%
  - Measurement: Using coverage.py or equivalent
  
- **Code Complexity**: Cyclomatic complexity per function
  - Target: ≤10 per function
  - Measurement: Using radon or pylint

- **Documentation**: Docstring coverage
  - Target: ≥90% of public functions
  - Measurement: Custom script or interrogate

#### Scoring
- 100%: Exceeds all targets
- 75%: Meets all targets
- 50%: Meets 2/3 targets
- 25%: Meets 1/3 targets
- 0%: Meets no targets

### 2. Functional Quality (25% of Quality Score)

#### Metrics
- **Response Accuracy**: Correctness of LLM outputs
  - Target: ≥90% on test set
  - Measurement: Human evaluation or automated scoring
  
- **Task Success Rate**: Successful completion of intended tasks
  - Target: ≥95%
  - Measurement: End-to-end test pass rate

- **Consistency**: Same input produces similar outputs
  - Target: ≥85% similarity score
  - Measurement: Multiple runs with cosine similarity

#### Scoring
- 100%: Exceeds all targets by ≥5%
- 75%: Meets all targets
- 50%: Within 5% of targets
- 25%: Within 10% of targets
- 0%: Below 10% of targets

### 3. Performance (25% of Quality Score)

#### Metrics
- **Response Latency**: Time to first token/completion
  - Target: p50 <1s, p95 <2s, p99 <5s
  - Measurement: Instrumentation with timing
  
- **Throughput**: Requests per second
  - Target: Depends on use case, document baseline
  - Measurement: Load testing results

- **Availability**: Uptime and error rate
  - Target: >99% success rate
  - Measurement: Error monitoring

#### Scoring
- 100%: Exceeds all targets
- 75%: Meets all targets
- 50%: Meets 2/3 targets
- 25%: Meets 1/3 targets
- 0%: Meets no targets

### 4. User Experience (25% of Quality Score)

#### Metrics
- **Clarity**: Output is understandable and well-formatted
  - Target: ≥4/5 in user testing
  - Measurement: User surveys or expert review
  
- **Relevance**: Responses address the user's need
  - Target: ≥90% relevance score
  - Measurement: User feedback or automated relevance scoring

- **Error Messages**: Helpful error handling
  - Target: All errors have actionable messages
  - Measurement: Code review checklist

#### Scoring
- 100%: Exceptional UX, delightful to use
- 75%: Good UX, meets expectations
- 50%: Acceptable UX, some rough edges
- 25%: Poor UX, frustrating to use
- 0%: Unusable

## 💰 Cost Metrics

### 1. API Costs (40% of Cost Score)

#### Metrics
- **Cost per Request**: Average API cost per user request
  - Target: Document and minimize
  - Measurement: Token counting × pricing
  
- **Cost per User**: Daily/monthly cost per active user
  - Target: <$0.10 per user per day (adjust by use case)
  - Measurement: Total costs / active users

- **Cost Efficiency**: Cost vs. quality tradeoff
  - Target: Maximize quality/cost ratio
  - Measurement: Quality score / cost

#### Tracking
```python
# Example tracking
{
  "request_id": "req_123",
  "timestamp": "2024-01-01T00:00:00Z",
  "model": "gpt-4",
  "input_tokens": 150,
  "output_tokens": 300,
  "cost_usd": 0.0135,
  "latency_ms": 1200
}
```

#### Scoring
- 100%: Exceptional cost efficiency (<50% of budget)
- 75%: Good cost efficiency (50-75% of budget)
- 50%: On budget (75-100% of budget)
- 25%: Over budget (100-125% of budget)
- 0%: Significantly over budget (>125%)

### 2. Resource Utilization (30% of Cost Score)

#### Metrics
- **Compute Costs**: Server/serverless execution costs
  - Target: Document baseline
  - Measurement: Cloud provider billing
  
- **Storage Costs**: Database, vector store, cache costs
  - Target: Document baseline
  - Measurement: Cloud provider billing

- **Network Costs**: Data transfer costs
  - Target: Minimize through caching
  - Measurement: Cloud provider billing

#### Scoring
- 100%: Highly optimized resource usage
- 75%: Efficient resource usage
- 50%: Acceptable resource usage
- 25%: Inefficient resource usage
- 0%: Wasteful resource usage

### 3. Cost Optimization (30% of Cost Score)

#### Evaluated Strategies
- **Caching**: Semantic or exact match caching
  - Metric: Cache hit rate
  - Target: ≥30% for repeat queries
  
- **Model Selection**: Using appropriate model for task
  - Metric: % requests using cheapest suitable model
  - Target: ≥80%

- **Prompt Optimization**: Minimizing tokens while maintaining quality
  - Metric: Average tokens per request
  - Target: Reduce by ≥20% from baseline

- **Batching**: Combining requests efficiently
  - Metric: % requests batched where possible
  - Target: ≥50%

#### Scoring
- 100%: Implemented ≥4 strategies effectively
- 75%: Implemented 3 strategies effectively
- 50%: Implemented 2 strategies effectively
- 25%: Implemented 1 strategy effectively
- 0%: No optimization strategies

## 🔒 Safety Metrics

### 1. Security (30% of Safety Score)

#### Metrics
- **Input Validation**: All inputs validated and sanitized
  - Target: 100% coverage
  - Measurement: Code review + security tests
  
- **Authentication/Authorization**: Proper access controls
  - Target: All endpoints protected
  - Measurement: Security audit

- **Secrets Management**: No hardcoded secrets
  - Target: 0 secrets in code
  - Measurement: Secret scanning tools

- **Vulnerability Scan**: No high/critical vulnerabilities
  - Target: 0 high/critical issues
  - Measurement: SAST/DAST tools

#### Scoring
- 100%: No security issues found
- 75%: Minor issues, not exploitable
- 50%: Medium issues, mitigations in place
- 25%: High issues, need immediate fix
- 0%: Critical issues, system unsafe

### 2. Privacy (30% of Safety Score)

#### Metrics
- **PII Detection**: Identifying and handling sensitive data
  - Target: ≥95% PII detected
  - Measurement: Test with known PII
  
- **Data Minimization**: Only collecting necessary data
  - Target: Document and justify all data collected
  - Measurement: Privacy review

- **Data Retention**: Appropriate data lifecycle
  - Target: Clear retention policies
  - Measurement: Policy documentation

- **Compliance**: Meeting regulatory requirements
  - Target: GDPR/CCPA/relevant compliance
  - Measurement: Compliance checklist

#### Scoring
- 100%: Exemplary privacy practices
- 75%: Good privacy practices, compliant
- 50%: Acceptable, minor gaps
- 25%: Significant privacy concerns
- 0%: Non-compliant, major issues

### 3. Content Safety (20% of Safety Score)

#### Metrics
- **Input Filtering**: Blocking harmful inputs
  - Target: ≥98% harmful inputs blocked
  - Measurement: Red team testing
  
- **Output Filtering**: Moderating generated content
  - Target: ≥95% harmful outputs blocked
  - Measurement: Automated + manual review

- **Prompt Injection Defense**: Resisting manipulation
  - Target: ≥90% injection attempts blocked
  - Measurement: Adversarial testing

#### Scoring
- 100%: Excellent content safety
- 75%: Good content safety
- 50%: Acceptable, some gaps
- 25%: Insufficient protections
- 0%: No content safety measures

### 4. Operational Safety (20% of Safety Score)

#### Metrics
- **Error Handling**: Graceful degradation
  - Target: No unhandled exceptions
  - Measurement: Error monitoring
  
- **Rate Limiting**: Preventing abuse
  - Target: Rate limits on all endpoints
  - Measurement: Configuration review

- **Monitoring**: Detecting anomalies
  - Target: Alerts for all critical issues
  - Measurement: Monitoring setup review

- **Rollback Capability**: Can revert changes
  - Target: <5 min rollback time
  - Measurement: Deployment testing

#### Scoring
- 100%: Excellent operational safety
- 75%: Good operational practices
- 50%: Acceptable practices
- 25%: Gaps in operational safety
- 0%: Unsafe operations

## 📈 Overall Scoring

### Calculation

```
Overall Score = (Quality Score × 0.33) + (Cost Score × 0.33) + (Safety Score × 0.34)

Where each category score is:
Category Score = Σ(Subcategory Score × Weight) / Σ(Weights)
```

### Rating Scale

- **90-100%**: Excellent - Exceeds expectations
- **75-89%**: Good - Meets all key criteria
- **60-74%**: Satisfactory - Acceptable with minor issues
- **40-59%**: Needs Improvement - Significant gaps
- **<40%**: Unsatisfactory - Major issues

### Minimum Requirements

To be considered complete, a deliverable must achieve:
- **≥60% in each category** (Quality, Cost, Safety)
- **≥70% overall score**

## 📋 Measurement Templates

### Quality Metrics Template

```markdown
## Quality Metrics Report - Week [X]

### Code Quality
- Test Coverage: [X]% (Target: ≥80%)
- Cyclomatic Complexity: [X] avg (Target: ≤10)
- Documentation: [X]% (Target: ≥90%)
- **Score**: [X]/100

### Functional Quality
- Response Accuracy: [X]% (Target: ≥90%)
- Task Success Rate: [X]% (Target: ≥95%)
- Consistency: [X]% (Target: ≥85%)
- **Score**: [X]/100

### Performance
- Latency p50/p95/p99: [X]ms/[X]ms/[X]ms
- Throughput: [X] req/s
- Availability: [X]% (Target: >99%)
- **Score**: [X]/100

### User Experience
- Clarity: [X]/5
- Relevance: [X]%
- Error Messages: [Good/Needs Work]
- **Score**: [X]/100

**Overall Quality Score**: [X]/100
```

### Cost Metrics Template

```markdown
## Cost Metrics Report - Week [X]

### API Costs
- Cost per Request: $[X]
- Cost per User per Day: $[X]
- Total API Costs: $[X]
- **Score**: [X]/100

### Resource Utilization
- Compute: $[X]
- Storage: $[X]
- Network: $[X]
- Total Infrastructure: $[X]
- **Score**: [X]/100

### Cost Optimization
- Caching Hit Rate: [X]%
- Appropriate Model Usage: [X]%
- Tokens per Request: [X] (baseline: [Y])
- Batching Rate: [X]%
- **Score**: [X]/100

**Overall Cost Score**: [X]/100
**Total Cost**: $[X]
```

### Safety Metrics Template

```markdown
## Safety Metrics Report - Week [X]

### Security
- Input Validation: [Pass/Fail]
- Auth/Authz: [Pass/Fail]
- Secrets Management: [Pass/Fail]
- Vulnerabilities: [X] high, [X] medium, [X] low
- **Score**: [X]/100

### Privacy
- PII Detection Rate: [X]%
- Data Minimization: [Documented/Not Documented]
- Retention Policies: [Defined/Not Defined]
- Compliance: [Compliant/Issues Found]
- **Score**: [X]/100

### Content Safety
- Input Filtering: [X]% blocked
- Output Filtering: [X]% blocked
- Prompt Injection Defense: [X]% blocked
- **Score**: [X]/100

### Operational Safety
- Error Handling: [Pass/Fail]
- Rate Limiting: [Configured/Not Configured]
- Monitoring: [Full/Partial/None]
- Rollback Time: [X] min
- **Score**: [X]/100

**Overall Safety Score**: [X]/100
```

## 🔄 Continuous Improvement

### Weekly Review Process

1. **Collect Metrics**: Gather all measurements
2. **Calculate Scores**: Apply scoring rubrics
3. **Identify Gaps**: Find areas below target
4. **Plan Improvements**: Prioritize fixes for next week
5. **Document Learnings**: Record insights

### Portfolio-Wide Trends

Track metrics across weeks to identify:
- Improving areas
- Persistent challenges
- Best practices to replicate
- Skills to develop further

---

**Related Resources**:
- [Weekly Deliverable Template](README.md)
- [Evaluation Guidelines](../../docs/evaluation/README.md)
- [Best Practices](../../docs/README.md)
