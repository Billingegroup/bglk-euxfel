# euxfel-mar25

Code from the EuXFEL experiment, March 2025

Scripts are in `src/scripts`
Functions are in a package in `src/functions`

## Installation

We assume that you have miniconda or conda installed

One time setup:

1. clone the repository or download and unzip the code.
2. move to the top level folder of the repository.  It will be called `euxfel-mar25` and contain the `pyproject.toml` file
3. create a python 3.11 conda environment that you will work in, e.g.,
   `conda create -n euxfel-mar25 python=3.11`
4. activate the environment
   `conda activate euxfel-mar25`
5. install all the dependencies
   `conda install --file requirements/conda.txt`
   `pip install `
6. install diffpy.morph
   `pip install -r requirements/pip.txt`
7. if you will be uploading any code edits and making PRs to the repository install and do some more things
   `conda install pre-commit` then type
   `pre-commit install`
8. copy any ipynbs you might want to run to folder where you want to work
8. Download the folder with the data from the EuXFEL cluster and copy it to a folder named 'input_data'.  This folder must reside in the same folder as the ipynb.

Downloading the data from Maxwell cluster:

1. log in to [Jupyter Hub](https://max-jhub.desy.de) on the Maxwell cluster using your DESY credentials and one time authentication factor. See this [link](https://it.desy.de/services/mfa/external_people/index_eng.html) for instructions
2. choose suitable partition on Maxwell from the upper drop-down menu and spawn your job. You will automatically have a folder named GPFS
3. navigate to gpfs/exfel/exp/\<beamline>/\<cycle>/\<proposal_number>/usr/\<code_name>, for example gpfs/exfel/exp/FXE/202501/p008015/usr/data_for_morph. Here you will find a ipynb file \<file_name.ipynb> and a folder \<folder_name>, for example get_data_for_morphing.ipynb and folder name save_raw_integrated_Data. The folder is where all the azimuthal integrated 2D detector images, geometry and mask corrected, will be saved for each run. This includes the raw scattering intensities for each delay scan, sorted between laser on and laser off, scattering vector q, and delay scan motor positions
4. open the ipynb
5. edit any parameters in the second cell, such as the proposal number, the max_run which (the prograis the 

To run the code:
1. log in to your computer and start a terminal
2. activate the conda environment `conda activate euxfel-mar25`
3. move to the directory with the ipynb in it that you want to work on
4. start jupyter `jupyter lab`
5. open the ipynb
6. edit any user-settable parameters in the second cell, such as the run number you want to work on, the q-range you want to use for the normalization and the q-range you want to compute the figure of merit over.
7. run the notebook.  The safest way to do it is using the double-chevron that restarts the kernel and runs all the cels
8. Good luck!