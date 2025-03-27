import os
from pathlib import Path

from bglk_euxfel.functions import build_paths


# @pytest.mark.parametrize(
#     "runtime_inputs, expected",
#     [  # tests as before but now config file present in cwd and home
#          but orcid
#         #   missing in the cwd config
#         # C1: nothing passed in, expect uname, email from local config, orcid
#               from home_config
#         ({}, {"owner_name": "cwd_ownername", "owner_email": "cwd@email.com",
#               "owner_orcid": "home_orcid"}),
#         # C2: empty strings passed in, expect uname, email, orcid from
#               home_config
#         (
#             {"owner_name": "", "owner_email": "", "owner_orcid": ""},
#             {"owner_name": "cwd_ownername", "owner_email": "cwd@email.com",
#              "owner_orcid": "home_orcid"},
#         ),
#    ],
# )
def test_build_paths(user_filesystem, default_args):
    # runtime_inputs, expected, ):
    cwd = Path(user_filesystem)
    os.chdir(cwd)
    metadata = {"thing": "one"}
    actual_paths, actual_metadata = build_paths(default_args, metadata)
    expected_paths = {
        "on_data_path": cwd / "input_data" / "run0204_delay_intensity_on.npy",
        "off_data_path": cwd
        / "input_data"
        / "run0204_delay_intensity_off.npy",
        "q_path": cwd / "input_data" / "run0204_q_values.npy",
        "delay_positions_path": cwd
        / "input_data"
        / "run0204_delay_positions.npy",
    }
    expected_metadata = {"thing": "one", "cwd": cwd}
    assert actual_paths == expected_paths
    assert actual_metadata == expected_metadata
