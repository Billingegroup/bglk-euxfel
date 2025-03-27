import json
from pathlib import Path

import pytest

from bglk_euxfel.parsers import get_args


@pytest.fixture
def user_filesystem(tmp_path):
    base_dir = Path(tmp_path)
    input_data_dir = base_dir / "input_data"
    input_data_dir.mkdir(parents=True, exist_ok=True)
    home_dir = base_dir / "home_dir"
    home_dir.mkdir(parents=True, exist_ok=True)
    cwd_dir = base_dir / "cwd_dir"
    cwd_dir.mkdir(parents=True, exist_ok=True)

    home_config_data = {"username": "home_username", "email": "home@email.com"}
    with open(home_dir / "diffpyconfig.json", "w") as f:
        json.dump(home_config_data, f)

    yield tmp_path


@pytest.fixture
def default_args():
    args = get_args(
        [
            "204",
            "--q-min-assess",
            "4.2",
            "--q-max-assess",
            "4.4",
            "--sample-name",
            "Bismuth",
            "--normalize-to-target-id",
            "0",
            "--path-to-data",
            "./input_data",
        ]
    )
    yield args
