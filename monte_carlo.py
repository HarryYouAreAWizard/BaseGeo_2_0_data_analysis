#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: monte_carlo.py
Author: Noah Nielsen
Created: 2024-06-14
Description: This module implements Monte Carlo sampling for converting posterior 
distributions from Bayesian Inference into point estimates and uncertainty quantification. 
It provides methods to calculate expected values, variances, credible intervals, and 
probabilities of differences between groups based on the samples drawn from the posterior distribution.

should be substituted with a library doing Markov Chain Monte Carlo sampling
"""

"is the monto carlo method just yet another method for doing inference?"


import numpy as np
import scipy

class MonteCarloSampler:
    """not a MCMC"""

    def __init__(self, posterior_dist, num_categories=7, num_samples=100000):

        self.posterior_dist = posterior_dist
        self.num_samples = num_samples
        self.samples = self.sample()
        self.response_categories = np.arange(1, num_categories + 1)
        self.expected_values = np.dot(self.samples, self.response_categories)
    
    def sample(self):
        """
        Dicihlet distribution can be sampled directly using its rvs method.
        the samples are normalized, as a property of the Dirichlet distribution
        """
        self.samples = self.posterior_dist.rvs(size=self.num_samples)
        return self.samples
    
    def score_expected_value(self):
        """Calculate the expected value of the expected value from the 
        surveys based on the Monte Carlo samples."""

        return self.expected_values.mean()
    
    def score_variance(self):
        """calculate the variance of the survey scale mean based on 
        the Monte Carlo samples."""
        return self.expected_values.var()
    
    def probability_dist_of_differences(self, other):
        """Calculate the probability distribution of the difference in expected values between self and other.
        
        should be replaced with a MCMC"""

        self.dif_prop_dist = self.expected_values - other.expected_values 
        return self.dif_prop_dist


    def credible_interval_of_differences_percentile(self, other, confidence=0.90):
        """Calculate the credible interval for the difference in expected values between self and other.
        This is done by calculating the distribution of differences and then finding the percentiles corresponding 
        to the confidence level.
        
        confidence=0.90 means we want to find the interval that contains the middle 90% of the distribution of differences, 
        which leaves 5% in each tail
        """

        dif_samples = self.probability_dist_of_differences(other)
        lower_bound = np.percentile(dif_samples, (0.5 - confidence*0.5) * 100)
        upper_bound = np.percentile(dif_samples, (0.5 + confidence*0.5) * 100)
        return lower_bound, upper_bound

    
    def credible_interval_of_differences_gaussian_assumption(self, other, confidence=0.90):
        """Calculate the credible interval for the difference in expected values between self and other,
        assuming that the distribution of differences is approximately Gaussian. This is done by calculating
        the mean and standard deviation of the difference distribution and then using the appropriate z-score 
        for the confidence level.

        confidence=0.90 means we want to find the interval that contains the middle 90% of the 
        distribution of differences, which leaves 5% in each tail"""

        dif_samples = self.probability_dist_of_differences(other)
        mean_diff = dif_samples.mean()
        std_diff = dif_samples.std()
        z_score = scipy.stats.norm.ppf(0.5 + confidence*0.5) # where this gaussian cut off upper 2.5%
        lower_bound = mean_diff - z_score * std_diff # gaussian is symmetric
        upper_bound = mean_diff + z_score * std_diff
        return lower_bound, upper_bound


    def probability_higher_score_than_other(self, other):
        """Calculate the probabiliity that the mean score from self.samples is higher
        than the mean score from other.samples."""
        # count how many samples are greater than 0
        prob = np.mean(self.dif_prop_dist > 0)
        return prob