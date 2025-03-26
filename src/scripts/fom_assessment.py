import diffpy.morph.morph_api as morph
import xarray as xr
from pathlib import Path
import numpy as np
import matplotlib

from euxfel.functions import build_delay_dict, find_nearest
from euxfel.parsers import get_args, preprocessing_args
from euxfel.plotters import assessment_plotter

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


def main():
    # args = (
    #     gooey_parser()
    #     if len(sys.argv) == 1 or "--gui" in sys.argv
    #     else get_args()
    # )
    args = get_args()
    metadata = preprocessing_args(args)
    print(metadata)

    cwd = Path().cwd()
    run_number = args.run_number
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
    if args.q_min_assess is None:
        args.q_min_assess = min(q)
    if args.q_max_assess is None:
        args.q_max_assess = max(q)
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
    assessment_plotter(morph_delays, args)

if __name__ == '__main__':
    main()