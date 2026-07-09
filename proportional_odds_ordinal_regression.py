


import pymc as pm
import numpy as np
import pytensor.tensor as pt  # Standard for PyMC v5+ (use aesara.tensor as at if on older v4)

K = 7 # number of choices on likert scale
num_groups = 5 # number of groups

def make_model(question, dataframe, quiet=False):

    with pm.Model() as model:

        # centered cutpoints
        cutpoints_init = np.linspace(-2, 2, K - 1) # <- initial guess: latent variable is centered around 0
        cutpoints = pm.Normal(
            "cutpoints",
            mu=cutpoints_init,
            sigma=3, # <- wide prior
            transform=pm.distributions.transforms.ordered,  # Guarantees cutpoint[i] < cutpoint[i+1]
            initval=cutpoints_init
        )

        slope_mu = pm.Normal("slope_mu", mu=0, sigma=1)
        slope_sigma = pm.HalfNormal("slope_sigma", sigma=1)
        
        # reparameterization trick
        slope_groups_offset = pm.Normal("slope_groups_offset", mu=0, sigma=1, size=num_groups)
        slope_groups = pm.Deterministic("slope_groups", slope_mu + slope_groups_offset * slope_sigma)

        # intercept_mu_population = pm.Normal(
        #     "intercept_mu_population",
        #     mu=9, 
        #     sigma=1,
        # )
        intercept_sigma_population = pm.HalfNormal(
            "intercept_sigma_population", sigma=1
        )

        # reparameterization trick
        intercept_groups_offset = pm.Normal("intercept_groups_offset", mu=0, sigma=1, size=num_groups)
        intercept_groups = pm.Deterministic("intercept_groups", intercept_groups_offset * intercept_sigma_population)
                                                            #  ^ the population mean is now constrained to 0, and it is up to the cutpoints to "center" the latent variable 

        # combine group intercepts and group slopes to form the predictor
        # predictor = slope * time + intercept                     <- linear regression
        # prior for this predictor: no effect -> slope = 0, intercept = 3 (middle of 0 indexed likert scale)
        predictor = pm.Deterministic(
            "predictor", slope_groups[dataframe.institution] * dataframe.year + intercept_groups[dataframe.institution]
        )

        # likelihood
        y = pm.OrderedLogistic("y", cutpoints=cutpoints, eta=predictor, observed=dataframe[question].values.astype(np.int64))


        # relics. year is now either 0 or 1
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


def analyze(question, dataframe, quiet=False):
    # get counts
    dataframe = dataframe.dropna(subset=[question], how='any').copy()

    # shift questions responses to be 0 indexed

    #     C:\Users\NoahH\AppData\Local\Temp\ipykernel_16632\2763623900.py:74: SettingWithCopyWarning: 
    # A value is trying to be set on a copy of a slice from a DataFrame.
    # Try using .loc[row_indexer,col_indexer] = value instead
    dataframe.loc[:, question] = dataframe.loc[:, question].astype(int) - 1

    # run mcmc
    idata, model = make_model(question, dataframe, quiet=quiet)
    divergent_count = idata.sample_stats.diverging.sum().item()


    return idata, model, divergent_count
    # az.summary(idata, var_names=["slope_mu", "slope_sigma", "intercept_mu_population", "intercept_sigma_population", "effect_after_7_years_population"])
    # az.plot_trace(idata, var_names=["slope_mu", "slope_sigma", "intercept_mu_population", "intercept_sigma_population", "effect_after_7_years_population"])