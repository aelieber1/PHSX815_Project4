"""
Goal Data Analysis Code for Project 3

Purpose: 
    - This code will read in the data generated from a Poisson distribution
    - You'll find several print statements throughout the code below, those are generally used to help troubleshoot while writing code, but they are left in the event you need to also troubleshoot the results you get

Author: @aelieber1
Date: April 6, 2023
Code adapted from these sources: 

"""

# Import Necessary Packages
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
from scipy.optimize import minimize
from scipy.special import gammaln
from tabulate import tabulate
from prettytable import PrettyTable

# main function for our CookieAnalysis Python code
if __name__ == "__main__":
   
    """ Read in data file name from commandline prompt """
    
    # Read in data file as input
    haveInput = False
    if '-input' in sys.argv:
        p = sys.argv.index('-input')
        InputFile = sys.argv[p+1]
        haveInput = True
    
    # Print help message if no input is found
    if '-h' in sys.argv or '--help' in sys.argv or not haveInput:
        print ("Usage: %s [options] [input file]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print (" -input (filename)   first hypothesis data to be analyzed")
        sys.exit(1)
        
    """ Negative log likelihood of Poisson function """ 
    # this function will be minimized later to ascertain what the probable value for 
    # the rate parameter lambda for each experiment 
    
    def loglikelihood(l):
        return (-1 * ((math.log(l) * sum_data) - (Nmeas * l) - factorial_sum))
        
    # Create empty arrays to store estimates of lambda, neg logliklihood, and error 
    param_estimates = []
    neg_logliklihood_estimates = []
    datapoints = []
        
    """ Estimate the Most Probable Lambda Value for the Dataset """
    need_rate = True
    with open(InputFile) as ifile: 
        
        # Read in true rate parameter
        for line in ifile:
            if need_rate:
                need_rate = False
                rate = float(line)
                continue
        print("True Rate is: ", rate)
        
        # Read in Nmeas (number of measurements)
        lineVals = line.split()
        Nmeas = len(lineVals)
        print("Nmeas: ", Nmeas)
        
        # Load data - skipping first row which just has the true rate
        data = np.loadtxt(InputFile, dtype=float, skiprows=1)
        #print(data)
                            
        # loop over each experiment
        Nexp = 0
        
        for i in data: 
            
            # Update counter for Nexp
            Nexp += 1
            
            """ Make calculations to use in minimization routine """
            # easier to troubleshoot this way rather than inputting it all into the 
            # function definition
            exp_data = i
            #print("Exp data: ", exp_data)
            sum_data = sum(exp_data)
            
            factorial_sum = 0
            for k in exp_data:
                f = math.log(math.factorial(int(k)))
                factorial_sum += f
            
            # Add bounds - only values that should be considered to be the rate (lambda) 
            # should be positive zero to positive infinity
            rate_bounds = [(0, math.inf)]
            
            """ Find Minimum of Negative Log Liklihood Function """
            min_result = minimize(loglikelihood, x0=3, bounds=rate_bounds)
            #print(" Minimization Routine Result: \n", min_result)
            
            minimum_estimate = min_result.x[0]
            param_estimates.append(minimum_estimate)
            
            # Add loglikelihood value to list - to plot later on
            neg_logliklihood_estimates.append(loglikelihood(minimum_estimate))
            
            for j in i:
                datapoints.append(j)
            
        Nmeas_total = Nmeas * Nexp   
    
    #print("Rate Estimates for this Dataset: ", param_estimates)
    #print("Neg LL Calculations for this Dataset: ", neg_logliklihood_estimates)
    
    # For the output plot, I'd like it to output at once
    plt.figure(figsize=(8, 4))
    
    # Plot data to visualize distribution
    plt.subplot(2,2,1)
    plt.hist(datapoints, bins=12,
             density=True, histtype='stepfilled', color='bisque', ec='orange', 
             alpha=0.75, label="Dataset with "+str(Nmeas)+" measurements per " 
             + str(Nexp) + " experiments")
    plt.xlabel("Number of Goals Scored")
    plt.title("Distribution of Dataset Drawn from Poisson Distribution \n Based on the True Rate Parameter " + str(rate))
    plt.legend()
    plt.grid(True)
    #plt.show()
    
    """ Plot Distribution of Lambda Parameter (should peak at true value) """
    plt.subplot(2,2,2)
    n, bins, patches = plt.hist(param_estimates, bins='auto' , density=True, histtype='bar',color='lightblue', ec='blue',alpha=0.75)
    plt.xlabel('Estimated Lambda Parameters')
    plt.title('Distribution of Estimated Lambda Parameters for \n' + 
              str(Nexp) + ' experiments and ' + str(Nmeas) + ' measurements')
    plt.axvline(x=rate, color = 'purple', 
                linewidth = 1.5, label = 'True Rate Parameter ' + str(rate))
    plt.legend()
    plt.grid(True)
    #plt.show()
    
    """ Calculate uncertainties from Lambda-Histogram Method """
    # Utilizing the numpy average method - following advice from StackExchange (https://stackoverflow.com/questions/50786699/how-to-calculate-the-standard-deviation-from-a-histogram-python-matplotlib)
    # Estimated mean from histogram
    mids = 0.5 * (bins[1:] + bins[:-1])
    mean = np.average(mids, weights=n)
    #print("Lambda Histogram Estimated Mean: ", mean)
    
    # Estimated variance - weighted average of the squared difference from the mean
    var = np.average((mids - mean)**2, weights=n)
    #print("Lambda Histogram Estimated Variance: ", var)
    
    # Standard deviation
    #print("Lambda Histogram Estimated StDev: ", np.sqrt(var))
    
    """ Calculate uncertainties from LogLikelihood Curve """
    # Plot negative log likelihood of function versus 
    nll = np.zeros_like(param_estimates)
    lambs = np.array(param_estimates)
    data_arr = np.array(datapoints)
    # Calculates the LogLiklihood based on the range of estimated lambdas & 
    for u, lam in enumerate(lambs):
        nll[u] = -np.sum(data_arr*np.log(lam) - lam - gammaln(data_arr+1))
    plt.subplot(2,2,3)
    plt.scatter(param_estimates, nll)
    plt.xlabel('Lambda Rate Parameter')
    plt.ylabel('Negative LogLikelihood of Lambda (NLL)')
    plt.title("Negative LogLikelihood Estimates vs. Estimated Parameters")
    
    
    # Plot Poisson Distribution based off of calculated lambda
    x = data_arr
    y = poisson.pmf(x, mu=mean)
    plt.subplot(2,2,4)
    plt.scatter(x,y, color='red')
    plt.axvline(x=rate, color = 'orange', 
                linewidth = 1.5, label = 'True Rate Parameter ' + str(rate))
    plt.legend()
    plt.title('Poisson Distribution based on True Rate Parameter')
    plt.show()
    
    # Find the minimum of this Neg Max Liklihood curve
    lambda_hat = lambs[np.argmin(nll)]
    #print("Maximum likelihood estimate of lambda from Minimum of LogLikelihood Curve:", lambda_hat)


    """ Analytical Calculate what the estiamted lambda is & variation from average of the datapoints """
    analytical_average = sum(datapoints)/ len(datapoints)
    #print("Analytically derived average: ", analytical_average)
    analystical_stdev = np.sqrt(analytical_average)
    #print("Analytically derived stdev: ", analystical_stdev)
    
    
    """ Output of Calculated Values in Table """
    t = PrettyTable(['Description', 'Value'])
    t.add_row(['True Rate Parameter for Data', rate])
    t.add_row(['Number of Experiments', Nexp])
    t.add_row(['Number of Measurments', Nmeas])
    t.add_row(['----------------------------------- ', '------------------'])                     
    t.add_row(["Lambda Histogram Estimated Mean: ", mean])
    t.add_row(["Lambda Histogram Estimated Variance: ", var])
    t.add_row(["Lambda Histogram Estimated StDev: ", np.sqrt(var)])
    t.add_row(['----------------------------------- ', '------------------'])   
    t.add_row(["Minimum of LogLikelihood Curve \n Estimate of Lambda:", lambda_hat])
    t.add_row(['----------------------------------- ', '------------------'])   
    t.add_row(["Analytically derived Average: ", analytical_average])
    t.add_row(["Analytically derived StDev: ", analystical_stdev])
    print(t)
    

    
                
    