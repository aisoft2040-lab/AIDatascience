# LLM Observability & Monitoring Guide

Comprehensive guide to monitoring, debugging, and maintaining LLM applications in production.

## 🎯 Why Observability Matters

Observability enables you to:
- **Detect issues** before users complain
- **Debug problems** in production
- **Optimize performance** based on real data
- **Track costs** and resource usage
- **Ensure quality** over time
- **Meet SLAs** with confidence

## 📊 Key Observability Pillars

### 1. Logging
**What happened and when?**

Structured logs with context about every LLM interaction.

### 2. Metrics
**How is the system performing?**

Quantitative measurements tracked over time.

### 3. Traces
**What is the request flow?**

End-to-end visibility of request lifecycle.

### 4. Alerts
**What needs attention?**

Proactive notifications for issues.

## 🔍 What to Monitor

### Request-Level Metrics

```python
@dataclass
class LLMRequestLog:
    # Identification
    request_id: str
    timestamp: datetime
    user_id: Optional[str]
    
    # Request details
    model: str
    prompt: str
    prompt_tokens: int
    
    # Response details
    response: str
    completion_tokens: int
    total_tokens: int
    
    # Performance
    latency_ms: float
    time_to_first_token_ms: Optional[float]
    
    # Cost
    cost_usd: float
    
    # Quality
    quality_score: Optional[float]
    safety_flags: List[str]
    
    # Context
    cache_hit: bool
    error: Optional[str]
    metadata: Dict[str, Any]
```

### System-Level Metrics

```python
METRICS_TO_TRACK = {
    # Performance
    'request_latency_seconds': 'Histogram of request duration',
    'time_to_first_token_seconds': 'Streaming response start time',
    'requests_per_second': 'Throughput',
    
    # Quality
    'response_quality_score': 'Average quality rating',
    'error_rate': 'Percentage of failed requests',
    'safety_flag_rate': 'Percentage flagged by moderation',
    
    # Cost
    'cost_per_request_usd': 'Average cost',
    'tokens_per_request': 'Average token usage',
    'daily_cost_usd': 'Running daily total',
    
    # Cache
    'cache_hit_rate': 'Percentage from cache',
    'cache_size_bytes': 'Current cache size',
    
    # System
    'active_requests': 'Concurrent requests',
    'queue_depth': 'Pending requests',
    'api_rate_limit_remaining': 'Remaining quota',
}
```

## 🛠️ Implementation Guide

### 1. Structured Logging

```python
import logging
import json
from datetime import datetime
from contextvars import ContextVar

# Context variable for request ID
request_id_var: ContextVar[str] = ContextVar('request_id', default='')

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # JSON formatter
        handler = logging.StreamHandler()
        handler.setFormatter(self.JsonFormatter())
        self.logger.addHandler(handler)
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'message': record.getMessage(),
                'request_id': request_id_var.get(),
                'module': record.module,
                'function': record.funcName,
            }
            
            # Add extra fields
            if hasattr(record, 'extra'):
                log_data.update(record.extra)
            
            return json.dumps(log_data)
    
    def log_llm_request(self, request_data):
        """Log LLM request with full context"""
        self.logger.info('LLM request', extra={
            'event_type': 'llm_request',
            'model': request_data.model,
            'prompt_tokens': request_data.prompt_tokens,
            'user_id': request_data.user_id,
        })
    
    def log_llm_response(self, response_data):
        """Log LLM response with metrics"""
        self.logger.info('LLM response', extra={
            'event_type': 'llm_response',
            'model': response_data.model,
            'completion_tokens': response_data.completion_tokens,
            'latency_ms': response_data.latency_ms,
            'cost_usd': response_data.cost_usd,
            'cache_hit': response_data.cache_hit,
        })

# Usage
logger = StructuredLogger('llm_service')
logger.log_llm_request(request)
```

### 2. Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge, Summary
import time

# Define metrics
llm_requests_total = Counter(
    'llm_requests_total',
    'Total LLM API requests',
    ['model', 'status']
)

llm_request_duration_seconds = Histogram(
    'llm_request_duration_seconds',
    'LLM request duration',
    ['model'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

llm_tokens_total = Counter(
    'llm_tokens_total',
    'Total tokens used',
    ['model', 'type']  # type: prompt or completion
)

llm_cost_usd_total = Counter(
    'llm_cost_usd_total',
    'Total cost in USD',
    ['model']
)

llm_active_requests = Gauge(
    'llm_active_requests',
    'Currently processing requests'
)

class MetricsCollector:
    @staticmethod
    def track_request(model, func):
        """Decorator to track LLM requests"""
        def wrapper(*args, **kwargs):
            llm_active_requests.inc()
            start_time = time.time()
            
            try:
                response = func(*args, **kwargs)
                
                # Record success
                duration = time.time() - start_time
                llm_requests_total.labels(model=model, status='success').inc()
                llm_request_duration_seconds.labels(model=model).observe(duration)
                
                # Record usage
                llm_tokens_total.labels(model=model, type='prompt').inc(
                    response.usage.prompt_tokens
                )
                llm_tokens_total.labels(model=model, type='completion').inc(
                    response.usage.completion_tokens
                )
                
                # Record cost
                cost = calculate_cost(model, response.usage)
                llm_cost_usd_total.labels(model=model).inc(cost)
                
                return response
                
            except Exception as e:
                llm_requests_total.labels(model=model, status='error').inc()
                raise
            finally:
                llm_active_requests.dec()
        
        return wrapper

# Usage
@MetricsCollector.track_request('gpt-4')
def call_gpt4(prompt):
    return openai.ChatCompletion.create(...)
```

### 3. Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Set up tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to observability platform
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

class TracedLLMClient:
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
    
    def call_llm(self, prompt, model='gpt-4'):
        """Make traced LLM call"""
        with self.tracer.start_as_current_span("llm_request") as span:
            # Add span attributes
            span.set_attribute("model", model)
            span.set_attribute("prompt_length", len(prompt))
            
            # Make API call
            try:
                with self.tracer.start_as_current_span("api_call"):
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}]
                    )
                
                # Record response details
                span.set_attribute("completion_tokens", 
                                 response.usage.completion_tokens)
                span.set_attribute("total_tokens", 
                                 response.usage.total_tokens)
                
                return response
                
            except Exception as e:
                span.set_attribute("error", True)
                span.set_attribute("error.message", str(e))
                raise
```

### 4. Alerting Rules

```python
class AlertManager:
    def __init__(self):
        self.thresholds = {
            'error_rate': 0.05,           # 5% error rate
            'latency_p95': 5.0,           # 5 seconds
            'daily_cost': 100.0,          # $100/day
            'safety_flag_rate': 0.01,     # 1% safety flags
        }
        self.alert_channels = ['email', 'slack', 'pagerduty']
    
    def check_error_rate(self, current_rate):
        """Alert if error rate too high"""
        if current_rate > self.thresholds['error_rate']:
            self.send_alert(
                severity='high',
                title='High Error Rate',
                message=f'Error rate {current_rate:.2%} exceeds threshold',
                metric='error_rate',
                current_value=current_rate,
                threshold=self.thresholds['error_rate']
            )
    
    def check_latency(self, p95_latency):
        """Alert if latency too high"""
        if p95_latency > self.thresholds['latency_p95']:
            self.send_alert(
                severity='medium',
                title='High Latency',
                message=f'P95 latency {p95_latency:.2f}s exceeds threshold',
                metric='latency_p95',
                current_value=p95_latency,
                threshold=self.thresholds['latency_p95']
            )
    
    def check_cost(self, daily_cost):
        """Alert if approaching budget"""
        if daily_cost > self.thresholds['daily_cost'] * 0.8:
            severity = 'high' if daily_cost > self.thresholds['daily_cost'] else 'medium'
            self.send_alert(
                severity=severity,
                title='High Daily Cost',
                message=f'Daily cost ${daily_cost:.2f} approaching limit',
                metric='daily_cost',
                current_value=daily_cost,
                threshold=self.thresholds['daily_cost']
            )
    
    def send_alert(self, severity, title, message, metric, current_value, threshold):
        """Send alert through configured channels"""
        alert = {
            'severity': severity,
            'title': title,
            'message': message,
            'metric': metric,
            'current_value': current_value,
            'threshold': threshold,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        for channel in self.alert_channels:
            self._send_to_channel(channel, alert)
```

## 📈 Dashboard Examples

### Key Metrics Dashboard

```yaml
# Example Grafana dashboard config
dashboard:
  title: "LLM Service Monitoring"
  panels:
    - title: "Requests per Second"
      type: graph
      targets:
        - expr: rate(llm_requests_total[5m])
    
    - title: "Latency Percentiles"
      type: graph
      targets:
        - expr: histogram_quantile(0.50, llm_request_duration_seconds)
          legend: "p50"
        - expr: histogram_quantile(0.95, llm_request_duration_seconds)
          legend: "p95"
        - expr: histogram_quantile(0.99, llm_request_duration_seconds)
          legend: "p99"
    
    - title: "Error Rate"
      type: graph
      targets:
        - expr: |
            rate(llm_requests_total{status="error"}[5m]) /
            rate(llm_requests_total[5m])
    
    - title: "Hourly Cost"
      type: graph
      targets:
        - expr: increase(llm_cost_usd_total[1h])
    
    - title: "Cache Hit Rate"
      type: stat
      targets:
        - expr: |
            sum(rate(llm_cache_hits[5m])) /
            sum(rate(llm_requests_total[5m]))
```

### Cost Dashboard

```python
def generate_cost_dashboard(metrics):
    """Generate cost analysis dashboard"""
    return {
        'daily_cost': {
            'current': metrics.get_daily_cost(),
            'budget': 100.0,
            'percentage': metrics.get_daily_cost() / 100.0
        },
        'cost_by_model': metrics.get_cost_by_model(),
        'cost_trend': metrics.get_cost_trend_7days(),
        'top_expensive_requests': metrics.get_top_expensive_requests(10),
        'cost_per_user': metrics.get_cost_per_user(),
        'projected_monthly': metrics.project_monthly_cost()
    }
```

## 🔍 Debugging in Production

### Log Analysis

```python
def analyze_failed_requests(logs, time_window='1h'):
    """Analyze patterns in failed requests"""
    failed = [log for log in logs if log.error is not None]
    
    analysis = {
        'total_failures': len(failed),
        'error_types': count_by_field(failed, 'error'),
        'affected_models': count_by_field(failed, 'model'),
        'affected_users': len(set(log.user_id for log in failed)),
        'common_patterns': extract_patterns(failed),
        'time_distribution': group_by_time(failed, interval='5m')
    }
    
    return analysis
```

### Troubleshooting Guide

```python
class TroubleshootingGuide:
    @staticmethod
    def diagnose_high_latency(metrics):
        """Diagnose causes of high latency"""
        issues = []
        
        # Check API response time
        if metrics.api_latency_p95 > 3.0:
            issues.append("High API latency - may be provider issue")
        
        # Check queue depth
        if metrics.queue_depth > 100:
            issues.append("High queue depth - consider scaling")
        
        # Check cache hit rate
        if metrics.cache_hit_rate < 0.2:
            issues.append("Low cache hit rate - review caching strategy")
        
        # Check model selection
        if metrics.gpt4_percentage > 0.5:
            issues.append("High GPT-4 usage - consider cheaper models")
        
        return {
            'issues': issues,
            'recommendations': generate_recommendations(issues)
        }
    
    @staticmethod
    def diagnose_high_cost(metrics):
        """Diagnose causes of high cost"""
        issues = []
        
        # Check token usage
        if metrics.avg_tokens_per_request > 2000:
            issues.append("High token usage - optimize prompts")
        
        # Check model mix
        expensive_ratio = metrics.expensive_model_ratio
        if expensive_ratio > 0.3:
            issues.append(f"High expensive model usage: {expensive_ratio:.0%}")
        
        # Check cache effectiveness
        if metrics.cache_hit_rate < 0.3:
            issues.append("Caching underutilized")
        
        return {
            'issues': issues,
            'cost_breakdown': metrics.get_cost_breakdown(),
            'savings_opportunities': calculate_savings_opportunities(metrics)
        }
```

## 🛠️ Tools & Platforms

### LLM-Specific Tools

1. **LangSmith** (LangChain)
   - Request tracing
   - Prompt versioning
   - Dataset management

2. **Weights & Biases**
   - Experiment tracking
   - Model evaluation
   - Cost tracking

3. **TruLens**
   - Quality evaluation
   - Feedback functions
   - Dashboard

4. **Helicone**
   - LLM observability
   - Cost tracking
   - Caching

### General Observability Tools

1. **Prometheus + Grafana**
   - Metrics collection and visualization

2. **ELK Stack** (Elasticsearch, Logstash, Kibana)
   - Log aggregation and search

3. **Datadog / New Relic**
   - Full-stack monitoring
   - APM for AI apps

4. **Sentry**
   - Error tracking
   - Performance monitoring

## 📋 Observability Checklist

### Setup Phase
- [ ] Structured logging configured
- [ ] Metrics collection implemented
- [ ] Distributed tracing set up
- [ ] Dashboards created
- [ ] Alerts configured
- [ ] Runbooks documented

### Monitoring Phase
- [ ] Daily dashboard review
- [ ] Weekly cost analysis
- [ ] Monthly trends review
- [ ] Quarterly capacity planning
- [ ] Alert response procedures tested

### Key Metrics to Watch
- [ ] Request latency (p50, p95, p99)
- [ ] Error rate
- [ ] Cost per request
- [ ] Cache hit rate
- [ ] Quality scores
- [ ] Safety flag rate

## 💡 Best Practices

1. **Log Everything** - You can't debug what you can't see
2. **Use Request IDs** - Track requests end-to-end
3. **Set Meaningful Alerts** - Avoid alert fatigue
4. **Monitor Costs Daily** - Catch runaway costs early
5. **Track Quality** - Monitor beyond just errors
6. **Document Runbooks** - Know what to do when alerts fire
7. **Regular Reviews** - Weekly/monthly metric reviews
8. **Test Observability** - Ensure monitoring works

---

**Related Guides**:
- [Evaluation Framework](../evaluation/README.md)
- [Cost Optimization](../cost-optimization/README.md)
- [Governance Framework](../governance/README.md)
