

"""
file: proportional_odds_ordinal_logistic_regression.py
author: Noah Nielsen
date: 2026-04-18
This module implements a proportional odds ordinal logistic regression model using PyMC.
the model were created before this file, but only defined in the notebook"""



import numpy as np
import pandas as pd
import pymc as pm


K = 7 # number of choices on likert scale
num_groups = 5 # number of universities in the dataset

def make_model(question, dataframe, quiet=False):

    with pm.Model() as model:

        # cutpoints
        cutpoints_init = np.linspace(-2, 2, K - 1) # <- initial guess: latent variable is centered around 0
        cutpoints = pm.Normal(
            "cutpoints",
            mu=cutpoints_init,
            sigma=3, # <- wide prior
            transform=pm.distributions.transforms.ordered,  # Guarantees cutpoint[i] < cutpoint[i+1]
            initval=cutpoints_init
        )

        # intercepts
        # no intercept_mu_population
        intercept_sigma_population = pm.HalfNormal(
            "intercept_sigma_population", sigma=1
        )
        # reparameterization trick
        intercept_groups_offset = pm.Normal("intercept_groups_offset", mu=0, sigma=1, size=num_groups)
        intercept_groups = pm.Deterministic("intercept_groups", intercept_groups_offset * intercept_sigma_population)
                                                            #  ^ the population mean is now constrained to 0, and it is up to the cutpoints to "center" the latent variable 
        # slopes
        slope_mu = pm.Normal("slope_mu", mu=0, sigma=1) # should have been named slope_mu_population
        slope_sigma = pm.HalfNormal("slope_sigma", sigma=1) # slope_sigma_population...
        # reparameterization trick
        slope_groups_offset = pm.Normal("slope_groups_offset", mu=0, sigma=1, size=num_groups)
        slope_groups = pm.Deterministic("slope_groups", slope_mu + slope_groups_offset * slope_sigma)

        # combine group intercepts and group slopes to form the predictor
        # predictor = slope * time + intercept                     <- linear regression
        predictor = pm.Deterministic(
            "predictor", slope_groups[dataframe.institution] * dataframe.year + intercept_groups[dataframe.institution]
        )

        # likelihood
        y = pm.OrderedLogistic("y", cutpoints=cutpoints, eta=predictor, observed=dataframe[question].values.astype(np.int64))


        # relics. year is now either 0 or 1. previously they were 0 and 7
        # still used in some tests
        effect_after_7_years_groups = pm.Deterministic(
            "effect_after_7_years_groups", slope_groups
        )
        effect_after_7_years_population = pm.Deterministic(
            "effect_after_7_years_population", slope_mu
        )

        # calculate odds ratios for population and groups
        odds_ratio_population = pm.Deterministic(
            "odds_ratio_population", pm.math.exp(slope_mu)
        )
        odds_ratio_groups = pm.Deterministic(
            "odds_ratio_groups", pm.math.exp(slope_groups)
        )
        
        idata = pm.sample(
            nuts_sampler="numpyro",
            draws=2000,
            tune=2000,
            target_accept=0.995,
            quiet=quiet,)
        
       
    return idata, model


