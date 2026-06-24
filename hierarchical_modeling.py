




"""

Core module for performing the hierarcical analysis

this analysis is a hierarchical model, effectively eliminating the need of making decisions based the number of responses.

"""
import pymc as pm
import numpy as np

def concatenate_counts(*args):
    """
    Takes an arbitrary number of Question objects, extracts their 7-point 
    response counts, and stacks them into a 2D matrix of shape (n_groups, 7).
    """
    # q.counts.values returns the underlying numpy array of counts for categories 1-7
    matrix = np.array([q.counts.values for q in args])
    return matrix


def find_posterior_distribution(
        question_uib,
        question_uibgeophys,
        question_uio,
        question_uit,
        question_unis,
        quiet=False):
    
    # 1. Stack the counts from the 5 university groups into a (5, 7) matrix
    counts_data = concatenate_counts(
        question_uib,
        question_uibgeophys,
        question_uio,
        question_uit,
        question_unis,
    )

    # Total respondents per group (N) -> vector of length 5
    n_respondents_per_group = counts_data.sum(axis=1) 

    # The 1-7 Likert scale axis
    scale_values = np.array([1, 2, 3, 4, 5, 6, 7])

    # using example from pyMC documentation
    # https://www.pymc.io/projects/examples/en/latest/mixture_models/dirichlet_mixture_of_multinomials.html
    # the shape parameter have been changed from the example (to match this problem)
    with pm.Model() as model:

        # from example
        frac = pm.Dirichlet("frac", a=np.ones(7), shape=7)  # <- prior for the fraction of each category, modeled as Dirichlet. Note that alpha is chosen as the same as for the previous analysis
        conc = pm.Lognormal("conc", mu=1, sigma=1, shape=1)  # <- prior for the concentration parameter, modeled as Lognormal
        
        p = pm.Dirichlet("p", a=frac * conc, shape=(counts_data.shape[0], 7))  # <- group-level probabilities, modelled as Dirichlet
        
        counts = pm.Multinomial("counts", n=n_respondents_per_group, p=p, observed=counts_data)

        # calculate the mean scores for every sample 
        # this is not from the example. AI were helpful in interpreting the frac variable
        group_mean_scores = pm.Deterministic('group_mean_scores', pm.math.dot(p, scale_values))
        population_mean_score = pm.Deterministic("population_mean_score", pm.math.dot(frac, scale_values))

        # --- Run the MCMC Simulation 
        trace = pm.sample(
                draws=2000, 
                tune=2000, 
                target_accept=0.98, 
                nuts_sampler="numpyro", 
                return_inferencedata=True,
                quiet=quiet
            )
    return trace


"""decrepreated version of the hierarchical model, kept for reference


    # --- Build the Hierarchical Model ---
    with pm.Model() as hierarchical_model:

        # distribution of the parameter governing the distribution of the likelihood-parameter
        # alpha in the Dirichlet must be above 0 -> halfnormal
        # alpha = pm.HalfNormal(
        #     'alpha', 
        #     sigma=1, # sigma of the halfnormal distribution. choice based on the prior choice made during previous project, with alpha=1
        #     shape=7 # <- one for each category
        # )

        # alpha_raw = pm.HalfNormal(
        #     'alpha_raw', 
        #     sigma=1.0, # <-  prior choice made during previous project, with alpha=1
        #     shape=7 # <- one for each category
        # )
        # alpha = pm.Deterministic("alpha", pm.math.log(alpha_raw)+0.5)

        # Reparameteriation, this must be investigated further
        # fraction = pm.Dirichlet(
        #     'fraction', a=np.ones(7), shape=7
        # )
        # concentration_raw = pm.Exponential(
        #     'concentration_raw', lam=0.1
        # )
        # concentration = pm.Deterministic("concentration", concentration_raw + 3.0)

        # alpha = pm.Deterministic("alpha", fraction * concentration)

        alpha = pm.Exponential(
            'alpha', lam=0.2, shape=7
        )

        # distribution of the likelihood-parameter
        # choose distribution for theta, the distribution of the parameter of the likelihoood
        theta = pm.Dirichlet(
            'theta', 
            a=alpha, # <- prior
            shape=(counts_data.shape[0], 7) # <- (n_groups, n_categories) 
        )

        # likelihood
        # the data are produced by a multinomial distribution with parameters theta, whch themselves are dirichlet distributed
        obs = pm.Multinomial(
            'obs', 
            n=n_respondents_per_group, # <- total respondents per group 
            p=theta, # <- group-level probabilities, modelled as Dirichlet
            observed=counts_data, # <- the data
            shape=counts_data.shape # <- (n_groups, n_categories)
        )
        
        # theta (5, 7) dot scale_values (7,) results in a vector of 5 expected scores
        group_mean_scores = pm.Deterministic('group_mean_scores', pm.math.dot(theta, scale_values))
        
        # alpha are "pseudocounts" -> find density before calculating mean
        population_probabilities = alpha / pm.math.sum(alpha)
        population_mean_score = pm.Deterministic('population_mean_score', pm.math.dot(population_probabilities, scale_values))



        # --- Run the MCMC Simulation 
        trace = pm.sample(
            draws=2000, 
            tune=1000, 
            target_accept=0.95, 
            nuts_sampler="numpyro", 
            return_inferencedata=True,
            quiet=quiet
        )

    # the trace object contain the internal MCMC parameters, 
    # which can be accessed by their keys, defined in the first 
    # argument in the above lines
    return trace

"""