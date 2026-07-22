


import pymc as pm
import numpy as np

num_groups = 5
# fit a simpler model for at every cutpoint
# fit binary logistic regression models for each cutpoint of the ordinal response variable
def make_binary_split_model(question, dataframe, cutpoint_j, quiet=False):
    y_binary = (dataframe[question].values > cutpoint_j).astype(np.int64)  # Y = j vs Y =< j
    group_idx = dataframe.institution.values
    year_vec = dataframe.year.values

    with pm.Model() as model:
        # intercepts
        intercept_mu = pm.Normal("intercept_mu", 0, 2) # no cutpoints, so we need a population intercept
        intercept_sigma = pm.HalfNormal("intercept_sigma", 1)
        intercept_offset = pm.Normal("intercept_offset", 0, 1, shape=num_groups)
        intercept_groups = pm.Deterministic("intercept_groups", intercept_mu + intercept_offset * intercept_sigma)

        # slopes
        slope_mu = pm.Normal("slope_mu", 0, 1)
        slope_sigma = pm.HalfNormal("slope_sigma", 1)
        slope_offset = pm.Normal("slope_offset", 0, 1, shape=num_groups)
        slope_groups = pm.Deterministic("slope_groups", slope_mu + slope_offset * slope_sigma)

        predictor = intercept_groups[group_idx] + slope_groups[group_idx] * year_vec
        y = pm.Bernoulli("y", logit_p=predictor, observed=y_binary)

        idata = pm.sample(
            nuts_sampler="numpyro", 
            draws=2000, 
            tune=2000, 
            target_accept=0.99, 
            quiet=quiet,
            chains=4,
            cores=4)
    return idata, model
