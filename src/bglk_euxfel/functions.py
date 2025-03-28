from pathlib import Path

import numpy as np


def build_paths(args, metadata):
    """Return paths to all the data files for laser on and off.

    Parameters
    ----------
    args : argparse.Namespace
      The inputs from the command line
    metadata : dict
      The metadata dictionary

    Returns
    -------
    paths : dict of pathlib.Path objects
      The paths to all the data files for laser on and off, the q-value
      arrays and the time-delay values. i.e keys {
        'on_data_path':
        'off_data_path':
        'q_path':
        'delay_positions_path':
    }
    """
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
        "on_data_path": on_data_path,
        "off_data_path": off_data_path,
        "q_path": q_path,
        "delay_positions_path": delay_positions_path,
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


def modulate_q(q, a3, a2, a1, a0):
    return a3*q**3 + a2*q**2 + a1*q + a0


def intensity_residuals(params, q_xfel, q_synchrotron, fq_synchrotron, iq_xfel):
    a3, a2, a1, a0 = params
    q_corrected = modulate_q(q_xfel, a3, a2, a1, a0)
    fq_interp = np.interp(q_corrected, q_synchrotron, fq_synchrotron)
    iq_norm = iq_xfel / np.max(iq_xfel)
    fq_norm = fq_interp / (np.max(fq_interp)*q_corrected)
    return np.sum((iq_norm - fq_norm) ** 2)

def optimize_q(q_xfel, q_synchrotron, fq_synchrotron, iq_xfel, bounds):
    result = differential_evolution(
        intensity_residuals,
        bounds,
        args=(q_xfel, q_synchrotron, fq_synchrotron, iq_xfel)
    )
    return result.x


def perform_polynomial_fit(q_corrected, iq_xfel, q_synchrotron, fq_synchrotron,
                           q_min_range, q_max_range, degree_a, degree_b):
    qmin_idx = np.abs(q_corrected - q_min_range).argmin()
    qmax_idx = np.abs(q_corrected - q_max_range).argmin()
    q_fit = q_corrected[qmin_idx:qmax_idx]
    iq_fit = iq_xfel[qmin_idx:qmax_idx]
    fq_interp = np.interp(q_fit, q_synchrotron, fq_synchrotron)
    X_a = np.vstack([iq_fit * (q_fit ** i) for i in range(degree_a + 1)]).T
    X_b = np.vstack([q_fit ** i for i in range(degree_b + 1)]).T
    X = np.hstack([X_a, X_b])
    coeffs, residuals, rank, s = np.linalg.lstsq(X, fq_interp, rcond=None)
    a_coeffs = coeffs[:degree_a + 1]
    b_coeffs = coeffs[degree_a + 1:]

    def a_poly(q_val):
        return sum(a_coeffs[i] * (q_val ** i) for i in range(degree_a + 1))

    def b_poly(q_val):
        return sum(b_coeffs[i] * (q_val ** i) for i in range(degree_b + 1))

    fitted_fq = np.array([a_poly(q_val) * I_val + b_poly(q_val) for q_val, I_val in zip(q_fit, iq_fit)])

    return q_fit, fitted_fq, a_coeffs, b_coeffs