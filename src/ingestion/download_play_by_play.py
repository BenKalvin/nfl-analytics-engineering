
from pathlib import Path

import nflreadpy as nfl


# Find the project root, regardless of where the script is run from.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "play_by_play_2023.parquet"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading 2023 NFL play-by-play data...")

    play_by_play = nfl.load_pbp(seasons=[2023])

    print(f"Downloaded {play_by_play.height:,} plays.")

    play_by_play.write_parquet(OUTPUT_FILE)

    print(f"Data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
