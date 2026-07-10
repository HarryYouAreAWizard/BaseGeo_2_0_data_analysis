


"""AI generated templates, to be rewritten and understood

The intention with the unconstrained model is to test the proportional odds assumption.
"""

import pymc as pm
import numpy as np
import pytensor.tensor as pt  # Standard for PyMC v5+ (use aesara.tensor as at if on older v4)

K = 7 # number of choices on likert scale
num_groups = 5 # number of groups

def unconstrained_model(question, dataframe, quiet=False):
    num_splits = K - 1 # 6 splits for a 7-point scale

    with pm.Model() as model:

        # 1. Centered cutpoints (strictly ordered)
        cutpoints_init = np.linspace(-2, 2, num_splits)
        cutpoints = pm.Normal(
            "cutpoints",
            mu=cutpoints_init,
            sigma=3, 
            transform=pm.distributions.transforms.ordered,  
            initval=cutpoints_init,
            shape=num_splits # is this not implied by the initval?
        )

        # 2. Unconstrained Population Slopes
        # We now have 6 separate baseline slopes, one for each threshold split
        slope_mu = pm.Normal("slope_mu", mu=0, sigma=1, shape=num_splits)
        slope_sigma = pm.HalfNormal("slope_sigma", sigma=1)
        
        # 3. Hierarchical Group Slopes (Shape: num_groups x num_splits -> 5 x 6)
        slope_groups_offset = pm.Normal("slope_groups_offset", mu=0, sigma=1, size=(num_groups, num_splits))
        # Broadcasts slope_mu across the group dimensions
        slope_groups = pm.Deterministic("slope_groups", slope_mu + slope_groups_offset * slope_sigma)

        # 4. Group Intercepts (Shape: num_groups -> 5)
        # still onyl one intercept per group, since the cutpoints handle the thresholds
        intercept_sigma_population = pm.HalfNormal("intercept_sigma_population", sigma=1)
        intercept_groups_offset = pm.Normal("intercept_groups_offset", mu=0, sigma=1, size=num_groups)
        intercept_groups = pm.Deterministic("intercept_groups", intercept_groups_offset * intercept_sigma_population)

        # 5. Extract vectors matching the DataFrame rows
        # Get the group indices for each row
        group_idx = dataframe.institution.values
        year_vec = dataframe.year.values[:, None]  # Shape: (N, 1) to broadcast over splits

        # Pull the correct 6 slopes for each row's institution: shape (N, 6)
        row_slopes = slope_groups[group_idx] 
        # Pull the intercept for each row's institution: shape (N, 1)
        row_intercepts = intercept_groups[group_idx][:, None]

        # 6. Manual Cumulative Logistic Link Math
        # eta shape: (N, 6)
        eta = cutpoints - (row_slopes * year_vec + row_intercepts)
        phi = pm.math.sigmoid(eta)
        
        # Slice out individual category probabilities
        p_0 = phi[:, [0]]
        p_mid = phi[:, 1:] - phi[:, :-1]
        p_K = 1.0 - phi[:, [-1]]
        
        # Combine into an (N, 7) probability matrix
        probs = pt.concatenate([p_0, p_mid, p_K], axis=1)

        # 7. Likelihood
        y = pm.Categorical("y", p=probs, observed=dataframe[question].values.astype(np.int64))

        # Track population odds ratios for each of the 6 splits
        odds_ratio_population = pm.Deterministic(
            "odds_ratio_population", pm.math.exp(slope_mu)
        )
        
        idata = pm.sample(
            nuts_sampler="numpyro",
            draws=2000,
            tune=2000,
            target_accept=0.995,
            quiet=quiet)
        
    return idata, model



