


"""
this module have a reference to plots which does not function from the graveyard
"""

from bayesian_inference import Categorial2Dirichlet
from monte_carlo import DirichletSampler
from plots_basic_BI_and_MC import *

def perform_BI_and_MC_analysis(survey1, survey2, question, 
                     print_results=True, 
                     gate_on_significance=False, 
                     folder="Bayesian_inference",
                     use_libraries=False,
                     with_marginalized_distributions=False):
    
    # ---------------------------------extract question---------------------------------
    # pick out the specific question to analyze
    if isinstance(question, int):
        example_question_1 = survey1.questions[question]
        example_question_2 = survey2.questions[question]
    else:
        example_question_1 = survey1.search(question)
        example_question_2 = survey2.search(question)

        # ensure that the search returned a valid question
        if example_question_1 is None or example_question_2 is None:
            print(f"Question '{question}' not found in one of the surveys.")
            return

    if example_question_1.raw_text != example_question_2.raw_text:
        # questions must be the same
        return 

    if example_question_1.axis is None and example_question_2.axis is None:
        # questions must have a well-defined axis (one of the 7-point scales)
        return     
    
    if example_question_1.axis != example_question_2.axis:
        # questions must be on the same axis (scale)
        return 

    if example_question_1.counts is None or example_question_2.counts is None:
        # print(f"Question '{question}' has missing counts in one of the surveys.")
        return
    # ---------------------------------statistics---------------------------------
    # do Bayesian Inference    
    BI1 = Categorial2Dirichlet(example_question_1)
    BI2 = Categorial2Dirichlet(example_question_2)

    # extract results
    uit_p_postrior_mean = BI1.expected_value()
    uio_p_postrior_mean = BI2.expected_value()
    uit_p_postrior_variance = BI1.variance()
    uio_p_postrior_variance = BI2.variance()
    uit_p_prior_mean = BI1.prior_dist.mean()
    uio_p_prior_mean = BI2.prior_dist.mean()
    uit_p_prior_variance = BI1.prior_dist.var()
    uio_p_prior_variance = BI2.prior_dist.var()

    # do monte carlo sampling to estimate average score and uncertainty
    MC_1 = DirichletSampler(BI1.posterior_dist, num_samples=int(1e6))
    MC_2 = DirichletSampler(BI2.posterior_dist, num_samples=int(1e6))

    # UiT - UiO
    dif_samples = MC_1.probability_dist_of_differences(MC_2)
    dif_credible_interval = MC_1.credible_interval_of_differences_percentile(MC_2)
    dif_credible_interval_gaussian_assumption = MC_1.credible_interval_of_differences_gaussian_assumption(MC_2)
    prop_uit_higher_score_than_uio = MC_1.probability_higher_score_than_other(MC_2)

    scale_expected_value_1 = MC_1.score_expected_value()
    scale_expected_value_2 = MC_2.score_expected_value()
    scale_variance_1 = MC_1.score_variance()
    scale_variance_2 = MC_2.score_variance()


    significant = dif_credible_interval[0] > 0  or dif_credible_interval[1] < 0
    if gate_on_significance and not significant:
        plot_folder = folder + "\\all"
        # folder = "Bayesian_inference\\all"
    # else:
        plot_folder = folder + "\\significant"
        # folder = f"Bayesian_inference\\significant"

    if print_results:
        print(F"Expected value for actor 1: {scale_expected_value_1}")
        print(F"Expected value for actor 2: {scale_expected_value_2}")
        print(F"Variance for actor 1: {scale_variance_1}")
        print(F"Variance for actor 2: {scale_variance_2}")

    # print(f"{MC_1.expected_values = }")

    # ---------------------------------plotting---------------------------------
    plot_raw_histogram(example_question_1=example_question_1, 
                       example_question_2=example_question_2, 
                       folder=plot_folder)

    plot_prior(example_question_1=example_question_1, 
               uit_p_prior_mean=uit_p_prior_mean, 
               uit_p_prior_variance=uit_p_prior_variance, 
               BI1=BI1, 
               example_question_2=example_question_2, 
               uio_p_prior_mean=uio_p_prior_mean, 
               uio_p_prior_variance=uio_p_prior_variance, 
               BI2=BI2,
               folder=plot_folder, 
               with_marginalized_distributions=with_marginalized_distributions)

    plot_posterior(example_question_1=example_question_1, 
                   uit_p_mean=uit_p_postrior_mean, 
                   uit_p_variance=uit_p_postrior_variance, BI1=BI1,
                   example_question_2=example_question_2, 
                   uio_p_mean=uio_p_postrior_mean, 
                   uio_p_variance=uio_p_postrior_variance, BI2=BI2,
                   folder=plot_folder, 
                   with_marginalized_distributions=with_marginalized_distributions)
    
    plot_mean_score_with_error_bars(example_question_1=example_question_1, 
                                    example_question_2=example_question_2,
                                    scale_expected_value_1=scale_expected_value_1, 
                                    scale_expected_value_2=scale_expected_value_2,
                                    scale_variance_1=scale_variance_1, 
                                    scale_variance_2=scale_variance_2, 
                                    folder=plot_folder, )

    plot_distribution_of_differences(example_question_1=example_question_1, 
                                     dif_samples=dif_samples, 
                                     dif_credible_interval=dif_credible_interval, 
                                     dif_credible_interval_gaussian_assumption=dif_credible_interval_gaussian_assumption, 
                                     prop_uit_higher_score_than_uio=prop_uit_higher_score_than_uio,
                                     folder=plot_folder)


    return MC_1, MC_2




