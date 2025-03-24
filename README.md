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
7. if you will be uploading any code edits and making push requests to the repository install and do some more things
   `conda install pre-commit` then type
   `pre-commit install`
8. Make the `eurfel-mar25` environment to be available as a kernel in jupyter.  Type `python -m ipykernel install --user --name=euxfel-mar25`

Testing your installation by running the example in this repo

1. look for the `example` directory in the `doc` directory.  You should see a folder called `input_data`
2. make a copy of the `figure_of_merit_assessment.ipynb` and paste it into the `example` directory.
3. in your terminal move to that same directory, e.g., `cd doc/example`
4. with your `euxfel-mar25` environment activated type `jupyter notebook &`
5. Jupyter should open in your browser
6. navigate to the `figure_of_merit_assessment.ipynb` and double-click on it to open it
7. make sure that the kernel selected is `euxfel-mar25` by selecting it in the dropdown menu
8. adjust the user-defined entries the second cell appropriately and run the notebook.  You can do this by running each cell separately, but better is 
9. it should run and give plots that look nice without crashing
10. after doing this, you can safely delete that ipynb

Downloading the data from Maxwell cluster to do a full analysis:

1. log in to [Jupyter Hub](https://max-jhub.desy.de) on the Maxwell cluster using your DESY credentials and one time authentication factor. See this [link](https://it.desy.de/services/mfa/external_people/index_eng.html) for instructions
2. choose suitable partition on Maxwell from the upper drop-down menu and spawn your job. You will automatically have a folder named GPFS
3. navigate to `gpfs/exfel/exp/\<beamline>/\<cycle>/\<proposal_number>/usr/\<code_name>`, for example `gpfs/exfel/exp/FXE/202501/p008015/usr/data_for_morph`. Here you will find a ipynb file \<file_name.ipynb> and a folder \<folder_name>, for example `get_data_for_morphing.ipynb` and folder name 'save_raw_integrated_Data'. The folder is where all the azimuthal integrated 2D detector images, geometry and mask corrected, will be saved for each run. This includes the raw scattering intensities for each delay scan, sorted between laser on and laser off, scattering vector q, and delay scan motor positions
4. open the ipynb
5. edit the parameters in the second cell, see example below
```
proposal = 8015     # number of the proposal
max_run = 190       # the code will try and process all scans from any numbered zero up to max_run
overwrite = False   # set to true if you want to reanalyze previously analyzed data, otherwise set to False for faster response
```
6. run the notebook
8. Download the folder with the data from the EuXFEL cluster and copy it to a folder named 'input_data'.  This folder must reside in the same folder as the ipynb for the morphing `figure_of_merit_assessment.ipynb`

Morphing the data and figure of merit:
1. To run the code:
2. log in to your computer and start a terminal
3. activate the conda environment `conda activate euxfel-mar25`
4. move to the directory with the ipynb in it that you want to work on
5. start jupyter `jupyter lab`
6. open the ipynb
7. edit any user-settable parameters in the second cell, such as the run number you want to work on, the q-range you want to use for the normalization and the q-range you want to compute the figure of merit over.
8. run the notebook.  The safest way to do it is using the double-chevron that restarts the kernel and runs all the cels
9. Good luck!