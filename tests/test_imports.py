from src.scraping.cast import extract_opening_cast
from src.network.bipartite import build_bipartite_graph
from src.analysis.metrics import build_metrics_table


def test_imports():
    assert extract_opening_cast is not None
    assert build_bipartite_graph is not None
    assert build_metrics_table is not None