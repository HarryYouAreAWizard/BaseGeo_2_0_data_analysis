



import numpy as np
from scipy.stats import dirichlet, beta

class BayesianInference:

    def __init__(self, prior_alpha=np.ones(7)*1.1):
        self.prior_alpha = prior_alpha
        self.prior_dist = dirichlet(self.prior_alpha)
        self.posterior_dist = None
        self.posterior_alpha = None
        
    
    def bayesian_inference(self, counts):

        # update the distribution with the counts    
        self.posterior_alpha = self.prior_alpha + counts.values
        self.posterior_dist = dirichlet(self.posterior_alpha)
        print(f"{self.posterior_alpha = }")
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

    def credible_interval(self, cred_mass=0.95):
        lower_bound = self.posterior_dist.ppf((1 - cred_mass) / 2)
        upper_bound = self.posterior_dist.ppf(1 - (1 - cred_mass) / 2)
        return lower_bound, upper_bound
    

    def marginal_interval(self, confidence=0.95):


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
