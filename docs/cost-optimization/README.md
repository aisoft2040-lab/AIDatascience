# LLM Cost Optimization Guide

Comprehensive strategies for minimizing costs while maintaining quality in LLM applications.

## 💰 Understanding LLM Costs

### Cost Components

1. **API Costs** (Usually 80-95% of total)
   - Input tokens (prompts)
   - Output tokens (completions)
   - Model tier (GPT-4 vs GPT-3.5 vs Claude, etc.)

2. **Infrastructure Costs** (5-15%)
   - Compute for application logic
   - Vector database storage and queries
   - Caching infrastructure
   - Network/bandwidth

3. **Development Costs** (Often overlooked)
   - Engineering time
   - Experimentation and testing
   - Monitoring and maintenance

### Typical Pricing (as of 2024)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Use Case |
|-------|----------------------|------------------------|----------|
| GPT-4 Turbo | $10 | $30 | Complex reasoning, high quality |
| GPT-3.5 Turbo | $0.50 | $1.50 | General purpose, fast |
| Claude 3 Opus | $15 | $75 | Complex tasks, long context |
| Claude 3 Sonnet | $3 | $15 | Balanced performance |
| Claude 3 Haiku | $0.25 | $1.25 | Fast, simple tasks |

**Note**: Prices change frequently. Always check current pricing.

## 🎯 Cost Optimization Strategies

### 1. Model Selection & Cascading

**Strategy**: Use the cheapest model that meets quality requirements

#### Model Cascading Pattern

```python
class ModelCascade:
    def __init__(self):
        self.models = [
            {'name': 'gpt-3.5-turbo', 'cost_per_token': 0.0000005, 'threshold': 0.8},
            {'name': 'gpt-4-turbo', 'cost_per_token': 0.00001, 'threshold': 0.95},
            {'name': 'gpt-4', 'cost_per_token': 0.00003, 'threshold': 1.0}
        ]
    
    def process(self, query, min_quality=0.9):
        """Try cheaper models first, escalate if needed"""
        for model in self.models:
            response = self.call_model(model['name'], query)
            quality = self.evaluate_quality(response)
            
            # If quality is good enough, return
            if quality >= min_quality:
                return response, model['cost_per_token']
            
            # If this was the last model, return anyway
            if model == self.models[-1]:
                return response, model['cost_per_token']
        
    def call_model(self, model_name, query):
        # Implementation
        pass
    
    def evaluate_quality(self, response):
        # Quick quality check (e.g., length, coherence)
        pass
```

#### Task-Based Model Selection

```python
MODEL_SELECTION = {
    'simple_qa': 'gpt-3.5-turbo',          # Fast, cheap
    'complex_reasoning': 'gpt-4-turbo',     # Higher quality
    'summarization': 'claude-3-haiku',      # Cost-effective
    'long_context': 'claude-3-sonnet',      # Best value for long docs
    'code_generation': 'gpt-4',             # Accuracy matters
}

def select_model(task_type):
    return MODEL_SELECTION.get(task_type, 'gpt-3.5-turbo')
```

### 2. Prompt Optimization

**Strategy**: Minimize tokens while maintaining effectiveness

#### Token Reduction Techniques

```python
def optimize_prompt(verbose_prompt):
    """Reduce tokens without losing meaning"""
    optimizations = [
        # Remove verbose instructions
        ('Please provide a detailed answer', 'Answer:'),
        ('I would like you to', ''),
        
        # Use abbreviations where clear
        ('for example', 'e.g.'),
        ('that is', 'i.e.'),
        
        # Remove redundancy
        ('very very', 'very'),
        
        # Use bullet points instead of paragraphs
        # Use shorter variable names in examples
    ]
    
    optimized = verbose_prompt
    for old, new in optimizations:
        optimized = optimized.replace(old, new)
    
    return optimized

# Example
original = """
Please provide a detailed and comprehensive answer to the following question.
I would like you to think carefully about your response and make sure it is
accurate and helpful. For example, if the question is about history, please
include relevant dates and context.

Question: What is the capital of France?
"""

optimized = """
Answer accurately with context if needed.

Q: What is the capital of France?
"""

# Savings: ~60 tokens → ~15 tokens (75% reduction)
```

#### Few-Shot Example Optimization

```python
# Instead of many examples
few_shot_verbose = """
Example 1: Input: "I love this!" Output: Positive
Example 2: Input: "This is terrible" Output: Negative  
Example 3: Input: "It's okay I guess" Output: Neutral
Example 4: Input: "Best product ever!" Output: Positive
Example 5: Input: "Waste of money" Output: Negative
"""

# Use minimal examples
few_shot_optimized = """
Examples:
"I love this!" → Positive
"This is terrible" → Negative
"It's okay" → Neutral
"""

# Or use table format
few_shot_table = """
Input | Output
"I love this!" | Positive
"Terrible" | Negative
"""
```

### 3. Caching Strategies

**Strategy**: Avoid recomputing identical or similar requests

#### Exact Match Caching

```python
import hashlib
from functools import lru_cache
import redis

class LLMCache:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379)
        self.ttl = 86400  # 24 hours
    
    def get_cache_key(self, prompt, model):
        """Create deterministic cache key"""
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, prompt, model):
        """Get cached response if exists"""
        key = self.get_cache_key(prompt, model)
        cached = self.redis_client.get(key)
        if cached:
            return cached.decode()
        return None
    
    def set(self, prompt, model, response):
        """Cache response"""
        key = self.get_cache_key(prompt, model)
        self.redis_client.setex(key, self.ttl, response)
    
    def get_or_generate(self, prompt, model):
        """Get from cache or generate"""
        cached = self.get(prompt, model)
        if cached:
            return cached, True  # From cache
        
        response = call_llm(prompt, model)
        self.set(prompt, model, response)
        return response, False  # Fresh generation

# Usage
cache = LLMCache()
response, from_cache = cache.get_or_generate(prompt, 'gpt-4')
if from_cache:
    print("Saved money by using cache!")
```

#### Semantic Caching

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticCache:
    def __init__(self, similarity_threshold=0.95):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache = []  # List of (embedding, prompt, response)
        self.threshold = similarity_threshold
    
    def find_similar(self, prompt):
        """Find cached response for similar prompt"""
        if not self.cache:
            return None
        
        prompt_embedding = self.model.encode(prompt)
        
        for cached_embedding, cached_prompt, cached_response in self.cache:
            similarity = np.dot(prompt_embedding, cached_embedding)
            similarity /= (np.linalg.norm(prompt_embedding) * 
                          np.linalg.norm(cached_embedding))
            
            if similarity >= self.threshold:
                return cached_response
        
        return None
    
    def add(self, prompt, response):
        """Add to cache"""
        embedding = self.model.encode(prompt)
        self.cache.append((embedding, prompt, response))
        
        # Limit cache size
        if len(self.cache) > 1000:
            self.cache.pop(0)

# Example usage
semantic_cache = SemanticCache()

# First request
response1 = call_llm("What is the capital of France?")
semantic_cache.add("What is the capital of France?", response1)

# Similar request - hits cache!
response2 = semantic_cache.find_similar("What's France's capital city?")
if response2:
    print("Cache hit! Saved an API call")
```

### 4. Output Length Control

**Strategy**: Limit output tokens to what's needed

```python
def call_llm_with_budget(prompt, max_tokens=100):
    """Strict token budget"""
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,  # Hard limit on output
        temperature=0.7
    )

# Progressive token allocation
def adaptive_token_budget(task_complexity):
    """Allocate tokens based on task"""
    budgets = {
        'simple': 50,      # Yes/No, short answers
        'medium': 200,     # Paragraph
        'complex': 500,    # Detailed explanation
        'unlimited': 2000  # When quality matters most
    }
    return budgets.get(task_complexity, 200)
```

### 5. Batch Processing

**Strategy**: Process multiple requests together to reduce overhead

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def batch_process(prompts, batch_size=10):
    """Process prompts in batches"""
    results = []
    
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i + batch_size]
        
        # Process batch concurrently
        tasks = [
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": p}]
            )
            for p in batch
        ]
        
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
    
    return results

# Usage
prompts = ["Question 1", "Question 2", ...]
results = asyncio.run(batch_process(prompts))

# Cost savings: Reduced network overhead, better rate limit utilization
```

### 6. Streaming for Perceived Performance

**Strategy**: Start showing results immediately, reduce timeout waste

```python
from openai import OpenAI
client = OpenAI()

def stream_response(prompt):
    """Stream tokens as they arrive"""
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            token = chunk.choices[0].delta.content
            full_response += token
            print(token, end="", flush=True)
    
    return full_response

# Benefits:
# - Better UX (users see progress)
# - Can stop generation early if satisfied
# - Reduces wasted tokens on incomplete requests
```

### 7. Context Window Management

**Strategy**: Optimize what goes into the prompt

#### Efficient RAG Context

```python
def optimize_rag_context(query, documents, max_tokens=2000):
    """Select most relevant content within token budget"""
    
    # 1. Rank documents by relevance
    ranked_docs = rank_by_relevance(query, documents)
    
    # 2. Extract key passages from top documents
    context_parts = []
    token_count = 0
    
    for doc in ranked_docs:
        # Get most relevant passage from document
        passage = extract_relevant_passage(query, doc, max_length=200)
        passage_tokens = count_tokens(passage)
        
        if token_count + passage_tokens <= max_tokens:
            context_parts.append(passage)
            token_count += passage_tokens
        else:
            break
    
    return "\n\n".join(context_parts)

# More expensive: Including full documents
# More cost-effective: Extracting only relevant passages
```

#### Conversation History Pruning

```python
def prune_conversation_history(messages, max_tokens=4000):
    """Keep conversation within token budget"""
    
    # Always keep system message and last user message
    system_msg = messages[0]
    last_user_msg = messages[-1]
    history = messages[1:-1]
    
    # Calculate tokens for essential messages
    essential_tokens = count_tokens(system_msg) + count_tokens(last_user_msg)
    available_tokens = max_tokens - essential_tokens
    
    # Include recent history up to token limit
    pruned_history = []
    token_count = 0
    
    for msg in reversed(history):
        msg_tokens = count_tokens(msg)
        if token_count + msg_tokens <= available_tokens:
            pruned_history.insert(0, msg)
            token_count += msg_tokens
        else:
            break
    
    return [system_msg] + pruned_history + [last_user_msg]
```

### 8. Quality-Cost Tradeoff Analysis

```python
class CostQualityOptimizer:
    def __init__(self):
        self.models = [
            {'name': 'gpt-3.5-turbo', 'cost': 0.0000005, 'quality': 0.75},
            {'name': 'gpt-4-turbo', 'cost': 0.00001, 'quality': 0.90},
            {'name': 'gpt-4', 'cost': 0.00003, 'quality': 0.95},
        ]
    
    def optimal_model(self, min_quality=0.8, max_cost=0.00002):
        """Find best model for constraints"""
        
        # Filter by constraints
        candidates = [
            m for m in self.models
            if m['quality'] >= min_quality and m['cost'] <= max_cost
        ]
        
        if not candidates:
            return None
        
        # Maximize quality/cost ratio among candidates
        return max(candidates, key=lambda m: m['quality'] / m['cost'])
    
    def cost_to_reach_quality(self, target_quality, num_requests):
        """Calculate cost to achieve quality target"""
        model = min(
            [m for m in self.models if m['quality'] >= target_quality],
            key=lambda m: m['cost']
        )
        
        avg_tokens = 1000  # Estimate
        return model['cost'] * avg_tokens * num_requests
```

## 📊 Cost Monitoring & Tracking

### Request-Level Tracking

```python
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class CostMetrics:
    request_id: str
    timestamp: float
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_ms: float
    cache_hit: bool
    
class CostTracker:
    def __init__(self):
        self.metrics = []
        self.pricing = {
            'gpt-4': {'input': 0.00003, 'output': 0.00006},
            'gpt-3.5-turbo': {'input': 0.0000005, 'output': 0.0000015},
        }
    
    def track_request(self, request_id, model, response, cache_hit=False):
        """Track cost for a single request"""
        usage = response.usage
        pricing = self.pricing[model]
        
        cost = (
            usage.prompt_tokens * pricing['input'] +
            usage.completion_tokens * pricing['output']
        )
        
        metrics = CostMetrics(
            request_id=request_id,
            timestamp=time.time(),
            model=model,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            cost_usd=cost,
            latency_ms=response.response_ms,
            cache_hit=cache_hit
        )
        
        self.metrics.append(metrics)
        return metrics
    
    def get_daily_cost(self):
        """Calculate cost for today"""
        today_start = time.time() - 86400
        today_metrics = [m for m in self.metrics if m.timestamp > today_start]
        return sum(m.cost_usd for m in today_metrics)
    
    def get_cost_by_model(self):
        """Break down cost by model"""
        by_model = {}
        for m in self.metrics:
            if m.model not in by_model:
                by_model[m.model] = 0
            by_model[m.model] += m.cost_usd
        return by_model
```

### Budget Alerts

```python
class BudgetMonitor:
    def __init__(self, daily_budget=10.0, monthly_budget=300.0):
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget
        self.tracker = CostTracker()
    
    def check_budget(self):
        """Check if approaching budget limits"""
        daily_cost = self.tracker.get_daily_cost()
        monthly_cost = self.tracker.get_monthly_cost()
        
        alerts = []
        
        # Daily budget checks
        if daily_cost > self.daily_budget:
            alerts.append(f"CRITICAL: Exceeded daily budget! ${daily_cost:.2f} > ${self.daily_budget:.2f}")
        elif daily_cost > self.daily_budget * 0.8:
            alerts.append(f"WARNING: 80% of daily budget used: ${daily_cost:.2f}")
        
        # Monthly budget checks
        if monthly_cost > self.monthly_budget:
            alerts.append(f"CRITICAL: Exceeded monthly budget! ${monthly_cost:.2f}")
        elif monthly_cost > self.monthly_budget * 0.8:
            alerts.append(f"WARNING: 80% of monthly budget used: ${monthly_cost:.2f}")
        
        return alerts
    
    def enforce_budget(self, request_cost):
        """Block request if would exceed budget"""
        if self.tracker.get_daily_cost() + request_cost > self.daily_budget:
            raise BudgetExceededError("Would exceed daily budget")
        return True
```

## 🎯 Cost Optimization Checklist

### Before Deployment
- [ ] Profile typical request costs
- [ ] Set up cost tracking
- [ ] Implement caching strategy
- [ ] Optimize prompts for tokens
- [ ] Choose appropriate models per task
- [ ] Set token limits on outputs
- [ ] Configure budget alerts

### During Operation
- [ ] Monitor daily/monthly costs
- [ ] Track cost per user/request
- [ ] Measure cache hit rates
- [ ] Analyze expensive requests
- [ ] A/B test cheaper alternatives
- [ ] Review and optimize regularly

### Optimization Opportunities
- [ ] Can simpler model work?
- [ ] Can we cache more?
- [ ] Are prompts optimized?
- [ ] Can we batch requests?
- [ ] Is output length appropriate?
- [ ] Are we using streaming?
- [ ] Can we use semantic cache?

## 💡 Real-World Examples

### Example 1: Reducing Q&A Costs by 70%

**Before**:
- Using GPT-4 for all questions
- No caching
- Verbose prompts
- Cost: $500/month

**After**:
- GPT-3.5-turbo for simple questions (70% of traffic)
- GPT-4 only for complex questions (30%)
- Semantic caching (40% hit rate)
- Optimized prompts (-30% tokens)
- Cost: $150/month (70% reduction)

### Example 2: RAG System Optimization

**Before**:
- Including 5 full documents in context
- Average 6000 tokens per request
- Cost per request: $0.06

**After**:
- Extract relevant passages only
- Average 1500 tokens per request
- Cost per request: $0.015 (75% reduction)
- Quality score: 0.90 → 0.88 (minor drop, acceptable)

## 📚 Additional Resources

- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [Token Counting Tools](https://platform.openai.com/tokenizer)
- [Cost Optimization Case Studies](https://example.com)

---

**Related Guides**:
- [Evaluation Framework](../evaluation/README.md)
- [Observability Guide](../observability/README.md)
- [Production Best Practices](../README.md)
