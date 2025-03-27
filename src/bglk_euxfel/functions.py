import numpy as np
from pathlib import Path

def build_paths(args, metadata):
    cwd = Path().cwd()
    rel_path_to_data = Path(args.path_to_data)
    input_path = cwd / rel_path_to_data
    str_run_number = str(args.run_number).zfill(4)
    on_data_path = input_path / f"run{str_run_number}_delay_intensity_on.npy"
    off_data_path = input_path / f"run{str_run_number}_delay_intensity_off.npy"
    q_path = input_path / f"run{str_run_number}_q_values.npy"
    delay_positions_path = (
            input_path / f"run{str_run_number}_delay_positions.npy"
    )
    project_paths = {
        'on_data_path': on_data_path,
        'off_data_path': off_data_path,
        'q_path': q_path,
        'delay_positions_path': delay_positions_path,
    }
    metadata.update({"cwd": cwd})
    return project_paths, metadata


def build_delay_dict(
    delays, delay_time, q, on, off, morphed=None, q_min=None, q_max=None
):
    diff = on - off
    if q_min is not None:
        qmin_idx = find_nearest(q, q_min)
    else:
        qmin_idx = 0
    if q_max is not None:
        qmax_idx = find_nearest(q, q_max)
    else:
        qmax_idx = -1
    l1_diff = np.sum(np.abs(diff[qmin_idx:qmax_idx]))
    l2_diff = np.sum(diff[qmin_idx:qmax_idx] ** 2)
    i_sum_off = np.sum(off[qmin_idx:qmax_idx])
    i_sum_on = np.sum(on[qmin_idx:qmax_idx])
    items_list = [
        q,
        on,
        off,
        diff,
        l1_diff,
        i_sum_off,
        i_sum_on,
        l2_diff,
    ]
    if morphed is not None:
        items_list.extend(
            [morphed.get("morphed_cfg"), morphed.get("rw"), morphed.get("cpp")]
        )
    delays.update({delay_time: items_list})
    return delays


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return int(idx)


def set_limits(args, q):
    if args.q_min_assess is None or args.q_min_assess < min(q):
        args.q_min_assess = min(q)
    if args.q_min_normalize is None or args.q_min_normalize < min(q):
        args.q_min_normalize = min(q)
    if args.q_max_assess is None or args.q_max_assess > max(q):
        args.q_max_assess = max(q)
    if args.q_max_normalize is None or args.q_max_normalize > max(q):
        args.q_max_normalize = max(q)
    return args
