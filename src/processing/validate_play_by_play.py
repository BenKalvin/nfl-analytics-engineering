
import polars as pl


def validate_play_by_play(df: pl.DataFrame) -> None:
    """Raise an error if essential play-by-play data quality rules fail."""

    if df.is_empty():
        raise ValueError("Play-by-play dataset is empty.")

    required_columns = {"game_id", "play_id"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if df["game_id"].null_count() > 0:
        raise ValueError("Some rows have missing game IDs.")

    if df["play_id"].null_count() > 0:
        raise ValueError("Some rows have missing play IDs.")

    duplicate_plays = (
        df.select(
            pl.struct(["game_id", "play_id"])
            .is_duplicated()
            .sum()
        ).item()
    )

    if duplicate_plays > 0:
        raise ValueError(
            f"Found {duplicate_plays} duplicate game/play combinations."
        )
