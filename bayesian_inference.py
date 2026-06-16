#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: bayesian_inference.py
Author: Noah Nielsen
Created: 2024-06-01
Description: Bayesian inference module for updating beliefs about response category 
probabilities based on observed data.
"""


import numpy as np
from scipy.stats import dirichlet

from actors import *

class BayesianInference:

    def __init__(self, question:Question, prior_alpha=np.ones(7)*1.0):

        self.question = question
        self.prior_alpha = prior_alpha
        self.prior_dist = dirichlet(self.prior_alpha)
        self.posterior_dist = None
        self.posterior_alpha = None
        
    
    def bayesian_inference(self):

        # update the distribution with the counts    
        self.posterior_alpha = self.prior_alpha + self.question.counts.values
        self.posterior_dist = dirichlet(self.posterior_alpha)
        return self.posterior_dist

    def mode(self):

        if isinstance(self.posterior_alpha, type(None)):
            return
        else:

            if np.any(self.posterior_alpha <= 1):
                raise ValueError("All alpha components must be > 1 to have a unique interior mode.")
            return (self.posterior_alpha - 1) / (np.sum(self.posterior_alpha) - len(self.posterior_alpha))
    
    def maximum_a_posteriori(self):
        return self.mode()
    
    def expected_value(self):
        return self.posterior_dist.mean()
    
    def variance(self):
        return self.posterior_dist.var()
    
    def covariance_matrix(self):
        return self.posterior_dist.cov()

    def credible_interval(self, confidence=0.95):
        """
        find where the cumulative distribution function (CDF) of 
        the posterior distribution equals the lower and upper tail probabilities
        """


        # alpha = np.array(alpha)
        alpha_total = np.sum(self.posterior_alpha)
        
        # Extract Beta parameters for the specific category
        lower_bound = []
        upper_bound = []
        for category_index in range(len(self.posterior_alpha)):
            a_param = self.posterior_alpha[category_index]
            b_param = alpha_total - a_param
            
            # Calculate tail probabilities
            alpha_tail = (1 - confidence) / 2
            
            # Compute bounds using the Beta distribution
            lower_bound.append(beta.ppf(alpha_tail, a_param, b_param))
            upper_bound.append(beta.ppf(1 - alpha_tail, a_param, b_param))
        lower_bound = np.array(lower_bound)
        upper_bound = np.array(upper_bound)
        return lower_bound, upper_bound
