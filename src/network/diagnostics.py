import pandas as pd
import networkx as nx


def graph_summary(G: nx.Graph) -> dict:
    """
    Return basic summary statistics for a graph.
    """

    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G),
    }


def degree_table(G: nx.Graph) -> pd.DataFrame:
    """
    Create dataframe of node degrees.
    """

    return (
        pd.DataFrame(
            G.degree(),
            columns=["node", "degree"]
        )
        .sort_values(
            "degree",
            ascending=False
        )
        .reset_index(drop=True)
    )


def component_summary(G: nx.Graph) -> dict:
    """
    Return connected component statistics.
    """

    components = sorted(
        nx.connected_components(G),
        key=len,
        reverse=True,
    )

    return {
        "components": len(components),
        "largest_component": len(components[0]),
        "second_largest_component": (
            len(components[1])
            if len(components) > 1
            else 0
        ),
    }