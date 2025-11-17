# LLM Evaluation Framework

Comprehensive guide to evaluating Large Language Model applications in production.

## 🎯 Why Evaluation Matters

Evaluation is critical for:
- **Quality assurance**: Ensuring outputs meet requirements
- **Regression detection**: Catching degradation from changes
- **Cost optimization**: Balancing quality vs. cost tradeoffs
- **Continuous improvement**: Measuring progress over time
- **Stakeholder confidence**: Demonstrating value and reliability

## 📊 Evaluation Framework Overview

### Evaluation Levels

1. **Unit Evaluation**: Individual components (prompts, retrievers)
2. **Integration Evaluation**: Combined components working together
3. **End-to-End Evaluation**: Complete user workflows
4. **Production Evaluation**: Real user interactions

### Evaluation Types

1. **Offline Evaluation**: Batch evaluation on test sets
2. **Online Evaluation**: Real-time evaluation in production
3. **Human Evaluation**: Manual review by humans
4. **Automated Evaluation**: Programmatic scoring

## 🔍 Key Evaluation Dimensions

### 1. Accuracy & Correctness

**Definition**: Does the output contain correct information?

#### Metrics
- **Factual Accuracy**: Percentage of factually correct statements
- **Answer Correctness**: For Q&A tasks, is the answer right?
- **Classification Accuracy**: For categorization tasks

#### Measurement Methods

**Ground Truth Comparison**
```python
def evaluate_accuracy(prediction, ground_truth):
    """Compare prediction against known correct answer"""
    return prediction.lower().strip() == ground_truth.lower().strip()
```

**LLM-as-a-Judge**
```python
def llm_judge_accuracy(question, answer, context):
    """Use GPT-4 to judge if answer is accurate given context"""
    prompt = f"""
    Question: {question}
    Context: {context}
    Answer: {answer}
    
    Is this answer factually correct? Rate 0-10.
    Provide brief reasoning.
    """
    # Call GPT-4 and parse response
    return score, reasoning
```

**Best Practices**
- Use multiple judges for important decisions
- Calibrate LLM judges against human ratings
- Include edge cases in test set
- Regular human spot-checks

### 2. Relevance

**Definition**: Does the output address the user's query or need?

#### Metrics
- **Relevance Score**: 0-1 scale of how relevant the output is
- **Answer Relevancy**: Specifically for Q&A systems
- **Context Relevance**: For RAG, are retrieved docs relevant?

#### Measurement Methods

**Semantic Similarity**
```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_relevance(query, response):
    """Calculate semantic similarity between query and response"""
    query_embedding = model.encode(query)
    response_embedding = model.encode(response)
    
    similarity = np.dot(query_embedding, response_embedding)
    similarity /= (np.linalg.norm(query_embedding) * np.linalg.norm(response_embedding))
    
    return similarity
```

**RAGAS Metrics**
```python
from ragas import evaluate
from ragas.metrics import answer_relevancy, context_relevancy

# Evaluate RAG system
results = evaluate(
    dataset,
    metrics=[answer_relevancy, context_relevancy]
)
```

### 3. Coherence & Quality

**Definition**: Is the output well-structured, grammatically correct, and easy to understand?

#### Metrics
- **Coherence Score**: Logical flow and consistency
- **Fluency Score**: Grammar and readability
- **Formatting Quality**: Proper structure and formatting

#### Measurement Methods

**Automated Quality Assessment**
```python
def evaluate_coherence(text):
    """Assess coherence using various signals"""
    checks = {
        'length': len(text.split()) > 10,  # Not too short
        'sentences': text.count('.') > 0,   # Has sentences
        'structure': '\n' in text,          # Has paragraphs
        'grammar': check_grammar(text),     # Basic grammar
    }
    return sum(checks.values()) / len(checks)
```

**LLM-based Assessment**
```python
def llm_judge_quality(text):
    """Use LLM to assess quality"""
    prompt = f"""
    Rate the following text on:
    1. Coherence (logical flow)
    2. Grammar and fluency
    3. Formatting and structure
    
    Text: {text}
    
    Provide scores 0-10 for each aspect.
    """
    # Parse and return scores
```

### 4. Completeness

**Definition**: Does the output fully address all aspects of the query?

#### Metrics
- **Coverage Score**: Percentage of query aspects addressed
- **Completeness Rating**: Subjective 0-10 rating

#### Measurement Methods

**Aspect-based Evaluation**
```python
def evaluate_completeness(query, response, required_aspects):
    """Check if response covers all required aspects"""
    covered = []
    for aspect in required_aspects:
        if is_aspect_covered(response, aspect):
            covered.append(aspect)
    return len(covered) / len(required_aspects)
```

### 5. Safety & Bias

**Definition**: Is the output safe, unbiased, and appropriate?

#### Metrics
- **Safety Score**: No harmful content
- **Bias Score**: Fairness across demographics
- **Appropriateness**: Context-appropriate responses

#### Measurement Methods

**Content Moderation**
```python
from openai import OpenAI
client = OpenAI()

def check_safety(text):
    """Use OpenAI moderation API"""
    response = client.moderations.create(input=text)
    result = response.results[0]
    
    return {
        'safe': not result.flagged,
        'categories': result.categories,
        'scores': result.category_scores
    }
```

**Bias Detection**
```python
def evaluate_bias(prompt_template, test_demographics):
    """Test for demographic bias"""
    results = {}
    for demographic in test_demographics:
        response = generate(prompt_template.format(demographic=demographic))
        results[demographic] = analyze_sentiment(response)
    
    # Check if results vary significantly by demographic
    return calculate_bias_score(results)
```

### 6. Latency & Performance

**Definition**: How fast and reliably does the system respond?

#### Metrics
- **Response Time**: p50, p95, p99 latencies
- **Time to First Token**: For streaming responses
- **Throughput**: Requests per second
- **Availability**: Uptime percentage

#### Measurement

```python
import time
from statistics import median, quantiles

def measure_latency(num_requests=100):
    """Measure response time distribution"""
    latencies = []
    
    for _ in range(num_requests):
        start = time.time()
        response = make_llm_call()
        latency = time.time() - start
        latencies.append(latency)
    
    latencies.sort()
    return {
        'p50': median(latencies),
        'p95': quantiles(latencies, n=20)[18],  # 95th percentile
        'p99': quantiles(latencies, n=100)[98],
        'mean': sum(latencies) / len(latencies)
    }
```

### 7. Cost Efficiency

**Definition**: What is the cost-to-quality ratio?

#### Metrics
- **Cost per Request**: Average cost
- **Cost per Correct Answer**: Cost / accuracy
- **Quality-Adjusted Cost**: Cost weighted by quality

#### Measurement

```python
def evaluate_cost_efficiency(test_set):
    """Calculate cost-quality tradeoff"""
    total_cost = 0
    quality_scores = []
    
    for item in test_set:
        response, cost = make_llm_call_with_cost(item['query'])
        quality = evaluate_quality(item['query'], response, item['ground_truth'])
        
        total_cost += cost
        quality_scores.append(quality)
    
    avg_quality = sum(quality_scores) / len(quality_scores)
    avg_cost = total_cost / len(test_set)
    
    return {
        'avg_cost': avg_cost,
        'avg_quality': avg_quality,
        'efficiency': avg_quality / avg_cost  # Quality per dollar
    }
```

## 🧪 Building Evaluation Datasets

### Dataset Requirements

1. **Diverse**: Cover various scenarios and edge cases
2. **Representative**: Match production distribution
3. **Balanced**: Include positive and negative examples
4. **Labeled**: Ground truth for supervised evaluation
5. **Maintained**: Updated as system evolves

### Creating Test Sets

```python
# Example test set structure
test_set = [
    {
        'id': 'test_001',
        'query': 'What is the capital of France?',
        'ground_truth': 'Paris',
        'category': 'factual',
        'difficulty': 'easy',
        'context': None  # For RAG systems, include relevant docs
    },
    {
        'id': 'test_002',
        'query': 'Explain quantum computing to a 10-year-old',
        'ground_truth': None,  # No single correct answer
        'category': 'explanation',
        'difficulty': 'medium',
        'evaluation_criteria': [
            'uses simple language',
            'includes analogy',
            'age-appropriate'
        ]
    }
]
```

### Synthetic Data Generation

```python
def generate_test_cases(num_cases=100):
    """Use LLM to generate diverse test cases"""
    prompt = """
    Generate {num} diverse question-answer pairs for testing a Q&A system.
    Include various topics, difficulties, and question types.
    
    Format:
    Q: [question]
    A: [answer]
    Category: [factual/opinion/explanation/etc]
    Difficulty: [easy/medium/hard]
    """
    
    # Parse LLM output into test cases
    return test_cases
```

## 📈 Evaluation Pipelines

### Automated Evaluation Pipeline

```python
class EvaluationPipeline:
    def __init__(self, test_set, metrics):
        self.test_set = test_set
        self.metrics = metrics
        
    def run(self):
        """Run full evaluation pipeline"""
        results = []
        
        for test_case in self.test_set:
            # Generate response
            response = self.generate_response(test_case['query'])
            
            # Calculate all metrics
            scores = {}
            for metric_name, metric_fn in self.metrics.items():
                scores[metric_name] = metric_fn(
                    test_case['query'],
                    response,
                    test_case.get('ground_truth')
                )
            
            results.append({
                'test_id': test_case['id'],
                'query': test_case['query'],
                'response': response,
                'scores': scores
            })
        
        return self.aggregate_results(results)
    
    def aggregate_results(self, results):
        """Aggregate metrics across test set"""
        aggregated = {}
        for metric_name in self.metrics.keys():
            scores = [r['scores'][metric_name] for r in results]
            aggregated[metric_name] = {
                'mean': sum(scores) / len(scores),
                'min': min(scores),
                'max': max(scores)
            }
        return aggregated
```

### Continuous Evaluation

```python
# Run evaluation on every commit
# .github/workflows/evaluate.yml
name: LLM Evaluation

on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Evaluation
        run: |
          python evaluate.py --test-set data/test_set.json
      - name: Check Thresholds
        run: |
          python check_thresholds.py --results evaluation_results.json
```

## 🎯 Best Practices

### 1. Multiple Evaluation Methods

Don't rely on a single metric:
- Combine automated and human evaluation
- Use multiple automated metrics
- Regular human spot-checks

### 2. Evaluation Frequency

- **Pre-commit**: Quick smoke tests
- **Daily**: Full evaluation suite
- **Weekly**: Human evaluation sample
- **On-demand**: Before major releases

### 3. Threshold Setting

```python
# Example thresholds
THRESHOLDS = {
    'accuracy': 0.85,       # 85% minimum
    'relevance': 0.80,      # 80% minimum
    'safety': 1.0,          # 100% - zero tolerance
    'latency_p95': 2.0,     # 2 seconds max
    'cost_per_request': 0.01 # $0.01 max
}
```

### 4. Regression Testing

```python
def regression_test(current_results, baseline_results):
    """Check if metrics have degraded"""
    regressions = []
    
    for metric, current_score in current_results.items():
        baseline_score = baseline_results.get(metric)
        if baseline_score and current_score < baseline_score * 0.95:  # 5% tolerance
            regressions.append({
                'metric': metric,
                'baseline': baseline_score,
                'current': current_score,
                'change': current_score - baseline_score
            })
    
    return regressions
```

### 5. Versioned Evaluation

```python
# Track evaluation results over time
{
    'version': 'v1.2.3',
    'timestamp': '2024-01-15T10:30:00Z',
    'commit': 'abc123',
    'model': 'gpt-4-turbo',
    'results': {
        'accuracy': 0.89,
        'relevance': 0.92,
        # ... other metrics
    }
}
```

## 🔧 Tools & Frameworks

### Popular Evaluation Tools

1. **RAGAS**: RAG evaluation framework
   - Answer relevancy, faithfulness, context precision
   
2. **TruLens**: Comprehensive LLM app evaluation
   - Custom feedback functions
   - Dashboard for monitoring

3. **PromptFlow**: Microsoft's evaluation framework
   - Visual evaluation pipelines
   - Integrated with Azure

4. **LangSmith**: LangChain's evaluation platform
   - Dataset management
   - Online evaluation

5. **Weights & Biases**: MLOps platform
   - Experiment tracking
   - Evaluation dashboards

### Building Custom Evaluators

```python
from abc import ABC, abstractmethod

class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, query, response, ground_truth=None):
        """Return score 0-1"""
        pass

class AccuracyEvaluator(Evaluator):
    def evaluate(self, query, response, ground_truth):
        if not ground_truth:
            raise ValueError("Ground truth required")
        return 1.0 if response.strip() == ground_truth.strip() else 0.0

class RelevanceEvaluator(Evaluator):
    def __init__(self, model):
        self.model = model
    
    def evaluate(self, query, response, ground_truth=None):
        return calculate_semantic_similarity(query, response, self.model)
```

## 📚 Additional Resources

- [RAGAS Documentation](https://docs.ragas.io/)
- [TruLens Guides](https://www.trulens.org/)
- [OpenAI Evals](https://github.com/openai/evals)
- [Anthropic's Red Teaming](https://www.anthropic.com/red-teaming)

---

**Next Steps**: 
- [Observability Guide](../observability/README.md)
- [Cost Optimization](../cost-optimization/README.md)
- [Governance Framework](../governance/README.md)
