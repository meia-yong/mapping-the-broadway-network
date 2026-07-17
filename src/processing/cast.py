import pandas as pd


DEFAULT_PLACEHOLDER_PERFORMER_IDS = [
    "A_60670",   # George Spelvin
    "A_105617",  # Dummy Spelvin
]


def clean_cast(cast: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate performer-production relationships.

    A performer should appear only once per production.
    """

    return (
        cast
        .drop_duplicates(
            subset=["production_id", "performer_id"]
        )
        .reset_index(drop=True)
    )


def remove_placeholder_performers(
    cast: pd.DataFrame,
    placeholder_ids: list[str] | None = None,
) -> pd.DataFrame:
    """
    Remove known placeholder performer identities.

    Parameters
    ----------
    cast
        Production-performer table.
    placeholder_ids
        Performer IDs to exclude. If None, uses the
        project's default placeholder list.

    Returns
    -------
    pandas.DataFrame
        Cast table without placeholder performers.
    """

    if placeholder_ids is None:
        placeholder_ids = DEFAULT_PLACEHOLDER_PERFORMER_IDS

    return (
        cast[
            ~cast["performer_id"].isin(placeholder_ids)
        ]
        .copy()
        .reset_index(drop=True)
    )