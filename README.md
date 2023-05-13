# PHSX815_Project4

## Photon Counting Experiment Simulation with Detector Efficiency Estimation

### This repository contains several programs:

- `ExperimentData.py` [Python]
- `MeasAnalysis.py` [Python]
- `Random.py` [Python]

### You will see several TestData files, these are the instructions on how to read them:

Both files that begin with `ExpData` are the experimental data files generated and analyzed in this project. See PDF writeup for more information. One dataset has a detector efficiency (DE) of 50% and the other is set at 90%. Both datasets were generated to have 1000 measurements for every 10,000 experiments.  
    
Of course, using the `ExperimentData.py` [Python], you can generate any data set you'd like based off of the parameters you'd like! The world is your oyster!

### Requirements

The Python code in this repository requires the use of several packages which can be 
easily installed from the command line using `HomeBrew` or `pip install` commands. 

In order to compile the program `ExperimentData.py`, these external 
packages are required:
- `numpy`
- `from scipy.stats import poisson`

In order to compile the programs `MeasAnalysis.py`, these external 
packages are required:
- `math`
- `numpy`
- `matplotlib.pyplot as plt`
- `scipy.stats` import `poisson`
- `from scipy.optimize import minimize`
- `from scipy.special import gammaln`
- `from tabulate import tabulate`
- `from prettytable import PrettyTable`

### Usage

The python file `ExperimentData.py` which simulates the experiment can be run from the command
line by typing:

	<> python3 ExperimentData.py -laserpower [Watts] -detect_eff [decimal] -Tmeas [seconds] -seed [seed] -Nmeas [number of measurements] -Nexp [number of experiments] -output ["filename"]

This script will either print the result to the command line or save to a file if given a filename from the command line. See earlier section to understand the datasets present in the repository already. 

With a dataset on hand from the previous script, the next python file to run is `GoalDataAnalysis.py`  which can be run from the commandline by typing:

	<> python3 MeasAnalysis.py -input ["filename"]

This script will conduct our analysis of estimating the rate parameter that is most probable based on the dataset using various methods. It will output one figure with all the plots it generated as well as a table of all the calculated parameters in the command prompt or terminal. 

### Plots within the Repository

You will notice several plots within the Plots & Data Folder within the Repository. There are three types of images in this folder. First we have DataPlots, DataTables, and Composites. The Data Plots are the histograms and other plots that output from running the analysis on different data files. The DataTables are the resulting stats for each analysis run. Lastly, the composite images show multiple data tables at once to compare different experiments of varying the number of measurments, number of experiments, and limits of lambda. Beyond that, the numbers in the file can be read in a similar fashion to the instructions given above on how to read Test Data files. 

### Other Notes

- All of the Python programs can be called from the command line with the `-h` or `--help` flag, which will print the options

- The files and `Random.py` are called within the scripts and should be downloaded or cloned to run properly


    
    
