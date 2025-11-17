from typing import Iterable, Sequence, Set, List, Tuple


def precision_recall_f1(tp: int, fp: int, fn: int) -> Tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def retrieval_at_k(ground_truth: Set[str], ranked: Sequence[str], k: int = 5) -> Tuple[int, int]:
    """
    Returns (hits, k) where hits is number of relevant items in top-k.
    ground_truth: set of relevant doc ids
    ranked: full ranking of doc ids (best first)
    """
    topk = ranked[:k]
    hits = sum(1 for x in topk if x in ground_truth)
    return hits, k


def recall_at_k(ground_truth: Set[str], ranked: Sequence[str], k: int = 5) -> float:
    if not ground_truth:
        return 0.0
    hits, kk = retrieval_at_k(ground_truth, ranked, k)
    return hits / len(ground_truth)


def batch_recall_at_k(ground_truth_list: List[Set[str]], ranked_lists: List[Sequence[str]], k: int = 5) -> float:
    assert len(ground_truth_list) == len(ranked_lists)
    recalls = [recall_at_k(gt, r, k) for gt, r in zip(ground_truth_list, ranked_lists)]
    return sum(recalls) / len(recalls) if recalls else 0.0
