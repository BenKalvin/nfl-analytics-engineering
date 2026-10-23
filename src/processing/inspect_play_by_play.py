
from pathlib import Path

import polars as pl


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "play_by_play_2023.parquet"


def main():
    print("Reading NFL play-by-play data...")

    df = pl.read_parquet(DATA_FILE)

    # 1. Basic dataset size
    print("\n--- Dataset Overview ---")
    print(f"Rows: {df.height:,}")
    print(f"Columns: {df.width:,}")

    # 2. Column names and data types
    print("\n--- Schema ---")
    print(df.schema)

    # 3. Check for missing game IDs
    print("\n--- Data Quality Checks ---")
    missing_game_ids = df["game_id"].null_count()
    print(f"Rows with missing game IDs: {missing_game_ids:,}")

    # 4. Check for duplicate game/play combinations
    duplicate_plays = (
        df.select(
            pl.struct(["game_id", "play_id"])
            .is_duplicated()
            .sum()
        ).item()
    )
    print(f"Duplicate game/play combinations: {duplicate_plays:,}")

    # 5. Preview a few records
    print("\n--- Sample Records ---")
    print(df.head(5))


if __name__ == "__main__":
    main()
