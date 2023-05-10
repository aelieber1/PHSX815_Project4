"""
Random Class to generate random numbers
An array of probability distributions are listed below, but this code will focus on calling the Poisson distribution method
This method stands out in between pound sign rows

Method for Poisson Distr. adapted from NumPy's numpy.random.Generator.poisson method found here: 
https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.poisson.html#numpy.random.Generator.poisson

Author: original code written by @crogan, adapted for these purposes by @aelieber1 -- added the Poisson method for this project
"""

import math
import numpy as np

class Random:
    """A random number generator class"""

    # initialization method for Random class
    def __init__(self, seed = 5555):
        self.seed = seed
        self.m_v = np.uint64(4101842887655102017)
        self.m_w = np.uint64(1)
        self.m_u = np.uint64(1)
        
        self.m_u = np.uint64(self.seed) ^ self.m_v
        self.int64()
        self.m_v = self.m_u
        self.int64()
        self.m_w = self.m_v
        self.int64()

    # function returns a random 64 bit integer
    def int64(self):
        with np.errstate(over='ignore'):
            self.m_u = np.uint64(self.m_u * np.uint64(2862933555777941757) + np.uint64(7046029254386353087))
        self.m_v ^= self.m_v >> np.uint64(17)
        self.m_v ^= self.m_v << np.uint64(31)
        self.m_v ^= self.m_v >> np.uint64(8)
        self.m_w = np.uint64(np.uint64(4294957665)*(self.m_w & np.uint64(0xffffffff))) + np.uint64((self.m_w >> np.uint64(32)))
        x = np.uint64(self.m_u ^ (self.m_u << np.uint64(21)))
        x ^= x >> np.uint64(35)
        x ^= x << np.uint64(4)
        with np.errstate(over='ignore'):
            return (x + self.m_v)^self.m_w

    # function returns a random floating point number between (0, 1) (uniform)
    def rand(self):
        return 5.42101086242752217E-20 * self.int64()
    
    ###################################################################################################
    """ Poisson Distribution """
    # function retruns a random integer that are drawn samples from the parametrized Poisson distr.

    def Poisson(self, lam):
        x = np.random.poisson(lam,size=None)
        
        return x
        
    ###################################################################################################

    # function returns a random integer (0 or 1) according to a Bernoulli distr.
    def Bernoulli(self, p=0.5):
        if p < 0. or p > 1.:
            return 1
        
        R = self.rand()

        if R < p:
            return 1
        else:
            return 0
        
    # function returns a random double (0 to infty) according to an exponential distribution
    def Exponential(self, beta=1.):
      # make sure beta is consistent with an exponential
      if beta <= 0.:
        beta = 1.

      R = self.rand()

      while R <= 0.:
        R = self.rand()

      X = -math.log(R)/beta

      return X
    
    # Additional distribution from Homework #3
    # First I tried the Categorical distribution as you suggested:
    def dist_categorical(self, thetas, n_samples):
        n_classes = len(thetas)
        
        # sets the categorical boundaries
        thetas_cumsum = np.cumsum(thetas)
        
        # samples a random dataset
        dataset_x = np.random.rand(n_samples)
        
        # uses np.select to categorize the data to transform from data sampled from a uniform distribution to data sampled from a categorical
        lower_than_limits = [dataset_x <= limit for limit in thetas_cumsum]
        class_matrix = [i * np.ones(n_samples) for i in range(n_classes)]
        dataset_w = np.select(condlist=lower_than_limits, choicelist=class_matrix)
        
        return dataset_w