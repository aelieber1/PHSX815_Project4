"""
Photodetection Experiment Data Simulation

Purpose: 

Author: @aelieber1
Date: May 8, 2023
University of Kansas, PHSX 815 Computational Physics

Code Adapted from these sources: 
    - @crogan PHSX815 Github Week 1 & 2
    - Documentation for Numpy Poisson Random Sampling
    - Photodetection Source
"""
# importpackages
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import poisson
import sys

# import our Random class from Random.py file - contains Poisson method
sys.path.append(".") 
from Random import Random

if __name__ == "__main__":
    
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-seed number]" % sys.argv[0])
        print (" -seed               seed value")
        print (" -laserpower         power of laser being used (Watts)")
        print (" -detect_eff         efficiency of detector [0,1]")
        print (" -Tmeas              measurement time (seconds)")
        print (" -Nmeas              number of measurements")
        print (" -Nexp               number of experiments")
        print (" -output [filename]  filename to save data output to") 
        sys.exit(1)

    # default seed
    seed = 5555

    # default laser power (Watts)
    laserpower = 0.1
    
    # Detector efficiency [0,1]
    detect_eff = 0.9
    
    # Measurement time (seconds)
    Tmeas = 0.00001

    # default number of measurements which corresponds to games since we take one measurement a game
    Nmeas = 1

    # default number of experiments, number of times we observe set number of games e.g. seasons. 
    #(Ex. if Nmeas=10 and Nexp=5, then we will observe 10 games, 5 times over, observing 50 games total)
    Nexp = 1

    # output file defaults
    doOutputFile = False

    # read the user-provided seed from the command line (if there)
    if '-seed' in sys.argv:
        p = sys.argv.index('-seed')
        seed = sys.argv[p+1]
    if '-laserpower' in sys.argv:
        p = sys.argv.index('-laserpower')
        laserpower = sys.argv[p+1]
    if '-detect_eff' in sys.argv:
        p = sys.argv.index('-detect_eff')
        detect_eff = sys.argv[p+1]
    if '-Tmeas' in sys.argv:
        p = sys.argv.index('-Tmeas')
        Tmeas = sys.argv[p+1]
    if '-Nmeas' in sys.argv:
        p = sys.argv.index('-Nmeas')
        Nt = int(sys.argv[p+1])
        if Nt > 0:
            Nmeas = Nt
    if '-Nexp' in sys.argv:
        p = sys.argv.index('-Nexp')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            Nexp = Ne
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True

    # class instance of our Random class using seed - It will call for the data to be sampled from a poisson distribution
    random = Random(seed)
    
    # mean number of photons (a.k.a the rate (lambda)) - calculate expected number of photons based on laser power and detection efficiency
    mean_photons = (float(laserpower) * float(detect_eff) * float(Tmeas)) / (6.626e-34 * 3e8)
    
    # sample data and either output in the command window (else) or output in a text file as named in the command line after -output
    if doOutputFile:
        outfile = open(OutputFileName, 'w')
        outfile.write(str(mean_photons)+" \n")
        for e in range(0,Nexp):
            for t in range(0,Nmeas):
                outfile.write(str(random.Poisson(mean_photons))+" ")
            outfile.write(" \n")
        outfile.close()
    else:
        print("Mean Number of Photons: ", mean_photons)
        for e in range(0,Nexp):
            for t in range(0,Nmeas):
                print(random.Poisson(mean_photons), end=' ')
            print(" ")