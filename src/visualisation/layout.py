import igraph as ig
import pandas as pd


def layout_to_dataframe(
    graph: ig.Graph,
    layout: ig.Layout,
) -> pd.DataFrame:
    """
    Convert igraph layout coordinates into a dataframe.

    Returns
    -------
    pandas.DataFrame
        Node IDs with x/y coordinates.
    """

    coords = pd.DataFrame(
        layout.coords,
        columns=["x", "y"]
    )

    coords.insert(
        0,
        "id",
        graph.vs["id"]
    )

    return coords


def add_normalised_coordinates(
    nodes: pd.DataFrame,
    coordinates,
) -> pd.DataFrame:
    """
    Add normalised x/y coordinates scaled to [0,1].
    """

    nodes = nodes.copy()

    coords = pd.DataFrame(
        coordinates,
        columns=["x", "y"]
    )

    nodes = pd.concat(
        [
            nodes.reset_index(drop=True),
            coords
        ],
        axis=1
    )

    for column in ["x", "y"]:
        minimum = nodes[column].min()
        maximum = nodes[column].max()
        range_ = maximum - minimum

        if range_ == 0:
            nodes[column] = 0
        else:
            nodes[column] = (
                nodes[column] - minimum
            ) / range_

    return nodes