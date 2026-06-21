

"""
To improve the data analysis, we should use existing libraries, instead of the custom ones. This one 
levarages pyMC for Bayesian inference. It is possible to extend it to also do the Monte Carlo sampling.

Using existing libraries are better, since they are more readable and if project is getting peer reviewed, 
they are more likely to be accepted.

"""


import numpy as np
import pymc
import arviz


class bayesian_inference_with_libraries:
    def __init__(self, observed_counts, prior_alpha=np.ones(7)*1.0):
        self.observed_counts = observed_counts
        self.prior_alpha = prior_alpha

        self.prior_dist = None
        self.posterior_dist = None

    def perform_inference(self):
        """Perform Bayesian inference using PyMC to update beliefs about response category probabilities based on observed data."""

        with pymc.Model() as model:
            # Define priors for the probabilities of each category
            prior = pymc.Dirichlet('p', a=self.prior_alpha)  # Customizable prior over 7 categories

            # Define likelihood based on observed data (example: counts of each category)
            likelihood = pymc.Multinomial('likelihood', n=sum(self.observed_counts), p=prior, observed=self.observed_counts)

            # Sample from the posterior distribution
            trace = pymc.sample(1000, tune=1000)

        summary = arviz.summary(trace)

        self.prior_dist = prior
        self.posterior_dist = trace

        return trace, summary

    def expected_value(self):
        """Calculate the expected value of the posterior distribution."""
        if self.posterior_dist is None:
            raise ValueError("Posterior distribution not computed. Call perform_inference() first.")
        return self.posterior_dist.mean()
    
    def variance(self):
        """Calculate the variance of the posterior distribution."""
        if self.posterior_dist is None:
            raise ValueError("Posterior distribution not computed. Call perform_inference() first.")
        return self.posterior_dist.var()
    
    def credible_interval(self, confidence=0.95):
        """Calculate the credible interval for the posterior distribution."""
        if self.posterior_dist is None:
            raise ValueError("Posterior distribution not computed. Call perform_inference() first.")
        lower_bound = (1 - confidence) / 2
        upper_bound = 1 - lower_bound
        return self.posterior_dist.ppf([lower_bound, upper_bound])