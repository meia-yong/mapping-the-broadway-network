"""
Generate performer-level metadata from cast, production, and network data.

Inputs:
    data/processed/production_cast.csv
    data/processed/production_metadata_checkpoint.csv
    data/processed/performer_edges_clean.csv

Output:
    visualisation/public/data/performer_metadata.csv
"""

from pathlib import Path

import pandas as pd


CAST_PATH = Path(
    "data/processed/production_cast.csv"
)

PRODUCTION_PATH = Path(
    "data/processed/production_metadata_checkpoint.csv"
)

EDGES_PATH = Path(
    "data/processed/performer_edges_clean.csv"
)

OUTPUT_PATH = Path(
    "visualisation/public/data/performer_metadata.csv"
)


def build_performer_metadata(
    cast_df,
    production_df,
    edges_df
):
    """
    Create performer-level summary statistics.
    """

    # Add production dates to each cast appearance
    cast_with_dates = cast_df.merge(
        production_df[
            [
                "production_id",
                "opening_date"
            ]
        ],
        on="production_id",
        how="left"
    )

    # Extract year from opening date
    cast_with_dates["year"] = (
        pd.to_datetime(
            cast_with_dates["opening_date"],
            errors="coerce"
        )
        .dt.year
    )

    # Aggregate performer statistics
    metadata = (
        cast_with_dates
        .groupby(
            [
                "performer_id",
                "performer_name"
            ]
        )
        .agg(
            first_year=(
                "year",
                "min"
            ),
            last_year=(
                "year",
                "max"
            ),
            production_count=(
                "production_id",
                "nunique"
            )
        )
        .reset_index()
    )

    # Count unique collaborators from edge list
    collaborator_counts = (
        pd.concat(
            [
                edges_df["source"],
                edges_df["target"]
            ]
        )
        .value_counts()
        .rename("collaborator_count")
        .reset_index()
    )

    collaborator_counts.columns = [
        "performer_id",
        "collaborator_count"
    ]

    # Add collaborator counts
    metadata = metadata.merge(
        collaborator_counts,
        on="performer_id",
        how="left"
    )

    # Clean missing values and data types
    metadata["collaborator_count"] = (
        metadata["collaborator_count"]
        .fillna(0)
        .astype(int)
    )

    metadata["first_year"] = (
        metadata["first_year"]
        .apply(
            lambda x: int(x) if pd.notna(x) else ""
        )
    )

    metadata["last_year"] = (
        metadata["last_year"]
        .apply(
            lambda x: int(x) if pd.notna(x) else ""
        )
    )

    return metadata


def main():

    print("Loading data...")

    cast = pd.read_csv(
        CAST_PATH
    )

    productions = pd.read_csv(
        PRODUCTION_PATH
    )

    edges = pd.read_csv(
        EDGES_PATH
    )

    # Ensure performer IDs use consistent format

    cast["performer_id"] = (
        cast["performer_id"]
        .astype(str)
    )

    edges["source"] = (
        edges["source"]
        .str.replace(
            "A_",
            "",
            regex=False
        )
    )

    edges["target"] = (
        edges["target"]
        .str.replace(
            "A_",
            "",
            regex=False
        )
    )

    print(
        f"Cast records: {len(cast):,}"
    )

    print(
        f"Productions: {len(productions):,}"
    )

    print(
        f"Edges: {len(edges):,}"
    )

    metadata = build_performer_metadata(
        cast,
        productions,
        edges
    )

    print(
        f"Performers: {len(metadata):,}"
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    metadata.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"Saved: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()