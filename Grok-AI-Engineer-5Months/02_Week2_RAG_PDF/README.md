# Week 2 – RAG PDF: Evaluation Harness

This folder includes minimal evaluation utilities for retrieval experiments.

## Metrics
- `precision_recall_f1(tp, fp, fn) -> (p, r, f1)`
- `recall_at_k(ground_truth: set[str], ranked: list[str], k=5) -> float`
- `batch_recall_at_k(list[set[str]], list[list[str]], k=5) -> float`

## Quick Demo (Notebook)
Open `notebooks/eval_demo.ipynb` and run the cells to compute recall@k on toy examples.

## Minimal Usage (Python)
```python
from eval.metrics import precision_recall_f1, recall_at_k
p, r, f1 = precision_recall_f1(tp=8, fp=2, fn=1)
rec = recall_at_k({"d1","d3"}, ["d1","d2","d4","d3"], k=3)
```

## Notes
- Ground truth is the set of relevant document IDs per query.
- Ranked list is the returned order of document IDs (best first).
- Extend with JSON validity, latency, and token cost logging during Week 2.
