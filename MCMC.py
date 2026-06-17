#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: MCMC.py
Author: Noah Nielsen (Adapted)
Description: This module implements Markov Chain Monte Carlo (MCMC) sampling using PyMC
To convert posterior distributions from Bayesian Inference into point estimates and 
uncertainty quantification. It provides methods to calculate expected values, variances, 
credible intervals, and probabilities of differences between groups.
"""

import numpy as np
import scipy.stats
import pymc as pm

class MonteCarloSampler:
    """Implements MCMC sampling over a Dirichlet-Multinomial posterior distribution."""

    def __init__(self, posterior_dist, num_categories=7, num_samples=1000000):
        self.num_categories = num_categories
        self.num_samples = num_samples
        self.response_categories = np.arange(1, num_categories + 1)
        
        # 1. Broadly extract the alpha parameters from the scipy dirichlet_frozen object
        if hasattr(posterior_dist, 'alpha'):
            alpha_params = np.atleast_1d(posterior_dist.alpha)
        elif hasattr(posterior_dist, 'kwds') and 'a' in posterior_dist.kwds:
            alpha_params = np.atleast_1d(posterior_dist.kwds['a'])
        elif hasattr(posterior_dist, 'args') and len(posterior_dist.args) > 0:
            alpha_params = np.atleast_1d(posterior_dist.args[0])
        else:
            alpha_params = np.atleast_1d(np.asarray(posterior_dist))

        # 2. Back-calculate effective observed counts assuming a flat uniform prior (alpha - 1)
        # We ensure it is a valid numerical array before running subtraction operations
        if isinstance(alpha_params, np.ndarray) and alpha_params.dtype.kind in 'biuf':
            self.observed_counts = np.clip(alpha_params - 1.0, 0, None)
        else:
            self.observed_counts = np.ones(num_categories) * 10  # Safe layout fallback

        # 3. Execute sampling and calculate expected values
        self.samples = self.sample()
        self.expected_values = np.dot(self.samples, self.response_categories)
        self.dif_prop_dist = None
    
    def sample(self):
        """
        Defines the Dirichlet-Multinomial model structure inside PyMC and draws 
        samples via MCMC (NUTS). Uses bootstrap upsampling to match target sizes efficiently.
        """
        counts_list = [int(x) for x in self.observed_counts]
        total_n = int(sum(counts_list))
        
        if total_n == 0:
            counts_list = [1 for _ in range(self.num_categories)]
            total_n = self.num_categories

        # Pull a robust, high-quality MCMC chain link array (e.g., 4000 draws)
        mcmc_draws = min(4000, self.num_samples)
        
        with pm.Model() as model:
            # Prior distribution over categories
            theta = pm.Dirichlet("theta", a=np.ones(self.num_categories))
            
            # Likelihood definition
            pm.Multinomial("likelihood", n=total_n, p=theta, observed=counts_list)
            
            # Run MCMC Sampling Core
            idata = pm.sample(
                draws=mcmc_draws, 
                tune=1000, 
                chains=2, 
                return_inferencedata=True, 
                progressbar=False,
                random_seed=42
            )
            
        # Flatten chains and draws into a single array: (Total Samples, Categories)
        mcmc_samples = idata.posterior["theta"].values.reshape(-1, self.num_categories)
        
        # High-speed bootstrap upsample to reach exactly 'num_samples' (e.g. 1e6) 
        # This keeps down-stream matplotlib/animation execution fast and fully compatible.
        indices = np.random.choice(mcmc_samples.shape[0], size=self.num_samples, replace=True)
        return mcmc_samples[indices]
    
    def score_expected_value(self):
        """Calculate the expected value of the expected value from the surveys."""
        return self.expected_values.mean()
    
    def score_variance(self):
        """Calculate the variance of the survey scale mean based on the samples."""
        return self.expected_values.var()
    
    def probability_dist_of_differences(self, other):
        """Calculate the probability distribution of the difference in expected values."""
        self.dif_prop_dist = self.expected_values - other.expected_values 
        return self.dif_prop_dist

    def credible_interval_of_differences_percentile(self, other, confidence=0.98):
        """Calculate the percentile credible interval for the difference."""
        dif_samples = self.probability_dist_of_differences(other)
        lower_bound = np.percentile(dif_samples, (0.5 - confidence * 0.5) * 100)
        upper_bound = np.percentile(dif_samples, (0.5 + confidence * 0.5) * 100)
        return lower_bound, upper_bound
    
    def credible_interval_of_differences_gaussian_assumption(self, other, confidence=0.98):
        """Calculate the credible interval assuming an approximately Gaussian distribution."""
        dif_samples = self.probability_dist_of_differences(other)
        mean_diff = dif_samples.mean()
        std_diff = dif_samples.std()
        z_score = scipy.stats.norm.ppf(0.5 + confidence * 0.5)
        lower_bound = mean_diff - z_score * std_diff
        upper_bound = mean_diff + z_score * std_diff
        return lower_bound, upper_bound

    def probability_higher_score_than_other(self, other):
        """Calculate the probability that the mean score from self is higher than other."""
        if self.dif_prop_dist is None:
            self.probability_dist_of_differences(other)
        return np.mean(self.dif_prop_dist > 0)