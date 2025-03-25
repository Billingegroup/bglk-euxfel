import diffpy.morph.morph_api as morph
import xarray as xr
from pathlib import Path
import numpy as np
import matplotlib.cm as cm
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt
import matplotlib

from euxfel.functions import build_delay_dict, find_nearest


matplotlib.use('TkAgg')

run_number = 204
sample_name = 'Bismuth'
target_id = 5
q_min = 4.2
q_max = 4.4
q_min_morph = None
q_max_morph = None
scale = 1.01
stretch = 0.01
smear = 0.005
baselineslope = None
qdamp = None
t0 = -751 # -749.8 for earlier days
points_away_t0_plot_on_off = -6
# rel_path_from_here_to_data = '.'
rel_path_from_here_to_data = '../../doc/example'

def plot_function(delays, time_away_t0):
    fig, (ax0,ax1,ax2,ax3,ax4) = plt.subplots(5,1,figsize=(8, 14))
    keys = [key for key in delays.keys()]
    delay_times_l1 = [delay[4] for delay in delays.values()]
    delay_times_off = [delay[5] for delay in delays.values()]
    delay_times_on = [delay[6] for delay in delays.values()]
    delay_times_l2 = [delay[7] for delay in delays.values()]
    #cmap = cm.get_cmap('viridis', len(keys))
    cmap = matplotlib.colormaps['viridis']
    colors = [cmap(i) for i in np.linspace(0, 1, len(keys))]
    key_to_color_idx = {key: i for i, key in enumerate(keys)}
    #cmap = matplotlib.colormaps.get_cmap('viridis', len(keys))
    #key_to_color_idx = {key: i for i, key in enumerate(keys)}
    for key, delay in delays.items():
        if key == time_away_t0:
            on_plot = delay[1]
            off_plot = delay[2]
        color = colors[key_to_color_idx[key]]
        ax0.plot(delay[0],delay[1],label=key,color=color)
        ax2.plot(delay[0],delay[3],label=key,color=color)
        if q_min is not None:
            ax2.axvline(x=q_min,color='red')
        if q_max is not None:
            ax2.axvline(x=q_max,color='red')
    ax1.plot(delay[0],on_plot,label='on',color='black')
    ax1.plot(delay[0],off_plot,label='off',color='orange')
    ax3.plot(keys,delay_times_off,marker='o', linestyle='-',label='off')
    ax3.plot(keys,delay_times_on,marker='o', linestyle='-',label='on')
    ax4.plot(keys,np.sqrt(delay_times_l2),marker='o', linestyle='-',label='diff')
    ax0.set_xlabel('Q [1/A]')
    ax0.set_ylabel('Pump On Intensity [a.u.]')
    ax1.set_xlabel('Q [1/A]')
    ax1.set_ylabel('Pump Off Intensity [a.u.]')
    ax2.set_xlabel('Q [1/A]')
    ax2.set_ylabel('On-Off Intensity [a.u.]')
    ax3.set_xlabel('Time delay (ps)')
    ax3.set_ylabel('Sum intensities')
    ax4.set_xlabel('Time delay (ps)')
    ax4.set_ylabel('RMS')
    ax3.legend()
    ax0.set_title(f'sample = {sample_name}, run = {run_number}, qmin = {q_min}, qmax = {q_max}')
    ax1.set_title(f'I(q) On vs Off, time_delay ={time_away_t0}, run = {run_number}')
    ax2.set_title(f'I(q) On - I(q) Off run = {run_number}')
    ax4.set_title(f'Figure of Merit run = {run_number}, q_min = {q_min}, q_max = {q_max}')
    plt.tight_layout()
    plt.show()


def main():
    cwd = Path().cwd()
    rel_path_to_data = Path(rel_path_from_here_to_data)
    input_path = cwd / rel_path_to_data / 'input_data'
    str_run_number = str(run_number).zfill(4)
    on_data_path = input_path/f'run{str_run_number}_delay_intensity_on.npy'
    off_data_path = input_path/f'run{str_run_number}_delay_intensity_off.npy'
    q_path = input_path/f'run{str_run_number}_q_values.npy'
    delay_positions_path = input_path/f'run{str_run_number}_delay_positions.npy'

    on = np.load(on_data_path)
    off = np.load(off_data_path)
    q = np.load(q_path)
    delay = np.load(delay_positions_path)
    delay = t0-delay
    target_key = delay[target_id]
    morph_cfg = morph.morph_default_config(scale=scale,stretch=stretch,smear=smear,baselineslope=baselineslope,qdamp=qdamp)

    raw_delays = {}
    for i, step in enumerate(delay):
        raw_delays = build_delay_dict(
            raw_delays,
            step,
            q,
            on[i],
            off[i],
            q_min,
            q_max
        )


    morph_delays = {}
    target = raw_delays[target_key]
    for delay_t, data in raw_delays.items():
        morphed = morph.morph(data[0], data[1], data[0], target[1], rmin=q_min_morph, rmax=q_max_morph, **morph_cfg) #on
        _, on_morph, _, _ = morphed['morph_chain'].xyallout
        morphed = morph.morph(data[0], data[2], data[0], target[1], rmin=q_min_morph, rmax=q_max_morph, **morph_cfg) #off
        _, off_morph, _, _ = morphed['morph_chain'].xyallout
        morph_delays = build_delay_dict(
            morph_delays,
            delay_t,
            data[0],
            on_morph,
            off_morph,
            q_min,
            q_max
        )
    if points_away_t0_plot_on_off is not None:
        t0_index = find_nearest(delay,0)
        time_away_t0_index_plot = t0_index + points_away_t0_plot_on_off
        time_away_t0 = delay[time_away_t0_index_plot]

    #plot_function(raw_delays)
    plot_function(morph_delays, time_away_t0)

if __name__ == '__main__':
    main()