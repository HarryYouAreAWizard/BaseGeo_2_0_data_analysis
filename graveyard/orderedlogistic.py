



import pymc as pm






# from https://github.com/pymc-devs/pymc-examples/blob/main/examples/generalized_linear_models/GLM-ordinal-regression.ipynb
def constrainedUniform(N, min=0, max=1):
    return pm.Deterministic(
        "cutpoints",
        pt.concatenate(
            [
                np.ones(1) * min,
                pt.extra_ops.cumsum(pm.Dirichlet("cuts_unknown", a=np.ones(N - 2))) * (max - min)
                + min,
            ]
        ),
    )




def survey_model(counts, quiet=False):
    """
    ordered logistic regression model for survey data
    """
    
    K = 7 # number of choices in likert scale

    with pm.Model() as model:

        # cutpoints defined from constrained uniform (following pyMC documentation)
        cutpoints = constrainedUniform(K, 0, K)