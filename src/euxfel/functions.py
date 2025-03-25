import numpy as np

def build_delay_dict(delays,delay_time,q,on,off,q_min=None,q_max=None):
    diff = on-off
    if q_min is not None:
        qmin_idx = find_nearest(q,q_min)
    else:
        qmin_idx = 0
    if q_max is not None:
        qmax_idx = find_nearest(q,q_max)
    else:
        qmax_idx = -1
    l1_diff = np.sum(np.abs(diff[qmin_idx:qmax_idx]))
    l2_diff = np.sum(diff[qmin_idx:qmax_idx]**2)
    i_sum_off = np.sum(off[qmin_idx:qmax_idx])
    i_sum_on = np.sum(on[qmin_idx:qmax_idx])
    delays.update({delay_time : [
        q,
        on,
        off,
        diff,
        l1_diff,
        i_sum_off,
        i_sum_on,
        l2_diff
    ]})
    return delays


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

