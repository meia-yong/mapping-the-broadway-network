import pandas as pd
import networkx as nx


def calculate_degree_metrics(G: nx.Graph) -> pd.DataFrame:
    """
    Calculate degree and weighted degree metrics.
    """

    degree = pd.DataFrame(
        G.degree(),
        columns=["performer_id", "degree"]
    )

    weighted_degree = pd.DataFrame(
        G.degree(weight="weight"),
        columns=["performer_id", "weighted_degree"]
    )

    return degree.merge(
        weighted_degree,
        on="performer_id"
    )


def calculate_pagerank(
    G: nx.Graph,
    weighted: bool = False,
) -> pd.DataFrame:
    """
    Calculate PageRank centrality.
    """

    scores = nx.pagerank(
        G,
        weight="weight" if weighted else None
    )

    column = (
        "pagerank_weighted"
        if weighted
        else "pagerank"
    )

    return pd.DataFrame(
        scores.items(),
        columns=["performer_id", column]
    )


def calculate_eigenvector_centrality(
    G: nx.Graph,
) -> pd.DataFrame:
    """
    Calculate eigenvector centrality.

    The graph should be connected.
    """

    scores = nx.eigenvector_centrality(
        G,
        max_iter=500
    )

    return pd.DataFrame(
        scores.items(),
        columns=[
            "performer_id",
            "eigenvector_centrality"
        ]
    )


def calculate_betweenness(
    G: nx.Graph,
    k: int = 500,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Estimate betweenness centrality.
    """

    scores = nx.betweenness_centrality(
        G,
        k=k,
        seed=seed
    )

    return pd.DataFrame(
        scores.items(),
        columns=[
            "performer_id",
            "betweenness"
        ]
    )


def add_collaboration_metrics(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add collaboration intensity metrics.
    """

    df = df.copy()

    df["collaboration_intensity"] = (
        df["weighted_degree"]
        .div(df["degree"])
        .fillna(0)
    )

    df["repeat_collaboration_surplus"] = (
        df["weighted_degree"]
        -
        df["degree"]
    )

    df["repeat_collaboration_ratio"] = (
        df["repeat_collaboration_surplus"]
        .div(df["degree"])
        .fillna(0)
    )

    return df


def build_metrics_table(
    G: nx.Graph,
) -> pd.DataFrame:
    """
    Build complete performer network metrics table.
    """

    metrics = calculate_degree_metrics(G)

    for table in [
        calculate_pagerank(G),
        calculate_pagerank(G, weighted=True),
        calculate_eigenvector_centrality(G),
        calculate_betweenness(G),
    ]:
        metrics = metrics.merge(
            table,
            on="performer_id"
        )

    return add_collaboration_metrics(metrics)