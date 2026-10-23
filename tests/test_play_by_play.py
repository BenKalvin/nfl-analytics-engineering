
import polars as pl
import pytest

from src.processing.validate_play_by_play import validate_play_by_play


def valid_data():
    return pl.DataFrame(
        {
            "game_id": ["2023_01_BUF_NYJ", "2023_01_BUF_NYJ"],
            "play_id": [1, 2],
        }
    )


def test_valid_data_passes():
    validate_play_by_play(valid_data())


def test_empty_data_fails():
    df = pl.DataFrame(
        schema={"game_id": pl.String, "play_id": pl.Int64}
    )

    with pytest.raises(ValueError, match="empty"):
        validate_play_by_play(df)


def test_missing_game_id_fails():
    df = pl.DataFrame(
        {
            "game_id": ["2023_01_BUF_NYJ", None],
            "play_id": [1, 2],
        }
    )

    with pytest.raises(ValueError, match="missing game IDs"):
        validate_play_by_play(df)


def test_missing_play_id_fails():
    df = pl.DataFrame(
        {
            "game_id": ["2023_01_BUF_NYJ", "2023_01_BUF_NYJ"],
            "play_id": [1, None],
        }
    )

    with pytest.raises(ValueError, match="missing play IDs"):
        validate_play_by_play(df)


def test_duplicate_play_fails():
    df = pl.DataFrame(
        {
            "game_id": ["2023_01_BUF_NYJ", "2023_01_BUF_NYJ"],
            "play_id": [1, 1],
        }
    )

    with pytest.raises(ValueError, match="duplicate"):
        validate_play_by_play(df)


def test_missing_required_column_fails():
    df = pl.DataFrame({"game_id": ["2023_01_BUF_NYJ"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_play_by_play(df)
