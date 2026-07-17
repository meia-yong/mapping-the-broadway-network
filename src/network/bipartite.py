import networkx as nx
import pandas as pd


def build_bipartite_graph(
    cast: pd.DataFrame
) -> nx.Graph:
    """
    Build performer-production bipartite graph.
    """

    B = nx.Graph()

    cast = cast.copy()

    cast["production_node"] = (
        "P_" + cast["production_id"].astype(str)
    )

    cast["performer_node"] = (
        "A_" + cast["performer_id"].astype(str)
    )

    performers = cast["performer_node"].unique()

    productions = cast["production_node"].unique()

    B.add_nodes_from(
        performers,
        bipartite="performer"
    )

    B.add_nodes_from(
        productions,
        bipartite="production"
    )

    B.add_edges_from(
        cast[
            [
                "performer_node",
                "production_node"
            ]
        ]
        .itertuples(
            index=False,
            name=None
        )
    )

    return B

from networkx.algorithms import bipartite

def project_performer_network(
    B: nx.Graph
) -> nx.Graph:
    """
    Project bipartite graph onto performers.

    Edge weights represent number of shared productions.
    """

    performer_nodes = {
        node
        for node, data in B.nodes(data=True)
        if data["bipartite"] == "performer"
    }

    return bipartite.weighted_projected_graph(
        B,
        performer_nodes
    )

def add_performer_attributes(
    G: nx.Graph,
    cast: pd.DataFrame,
) -> nx.Graph:
    """
    Attach performer metadata from the cast table
    to performer nodes.

    Currently adds:

    - performer_name

    Returns
    -------
    networkx.Graph
        Graph with updated node attributes.
    """

    performer_info = (
        cast[
            ["performer_id", "performer_name"]
        ]
        .drop_duplicates("performer_id")
        .set_index("performer_id")
    )

    attributes = performer_info.to_dict("index")

    nx.set_node_attributes(
        G,
        attributes
    )

    return G