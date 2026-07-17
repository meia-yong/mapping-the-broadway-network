import networkx as nx


def largest_connected_component(
    G: nx.Graph,
) -> nx.Graph:
    """
    Return the largest connected component
    of an undirected graph.
    """

    largest = max(
        nx.connected_components(G),
        key=len
    )

    return G.subgraph(largest).copy()