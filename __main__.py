#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: __main__.py
Author: Noah Nielsen
Date: 2026-06-16
Description: This script performs data analysis on the BaseGeo 2.0 survey data and generates plots.
"""



from os import listdir
import numpy as np
from matplotlib.pyplot import subplots, show, close, title
from scipy.stats import beta

from monte_carlo import MonteCarloSampler
from actors import Survey, Question
from plots import *
from bayesian_inference import BayesianInference
from animations import animate_monte_carlo_sampling

#  global data_folder, figure_folder
data_folder = "BaseGeo_2_0\\all data excel"
figure_folder = "BaseGeo_2_0\\figures"

# control flags
animate = 1


def perform_analysis(survey1, survey2, question, 
                     print_results=True, 
                     gate_on_significance=False, 
                     folder="Bayesian_inference",
                     use_libraries=False):
    
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


    
    # ---------------------------------statistics---------------------------------
    # initialize the BayesianInference class   
    BI1 = BayesianInference(example_question_1)
    BI2 = BayesianInference(example_question_2)
    # do the inference 
    BI1.bayesian_inference()
    BI2.bayesian_inference()

    # do monte carlo sampling to estimate average score on scale and uncertainty
    MC_1 = MonteCarloSampler(BI1.posterior_dist, num_samples=int(1e6))
    MC_2 = MonteCarloSampler(BI2.posterior_dist, num_samples=int(1e6))

    # extract results
    uit_p_mean = BI1.expected_value()
    uio_p_mean = BI2.expected_value()
    uit_p_variance = BI1.variance()
    uio_p_variance = BI2.variance()
    # also find the prior distribution
    uit_p_prior_mean = BI1.prior_dist.mean()
    uio_p_prior_mean = BI2.prior_dist.mean()
    uit_p_prior_variance = BI1.prior_dist.var()
    uio_p_prior_variance = BI2.prior_dist.var()

    # UiT - UiO
    dif_samples = MC_1.probability_dist_of_differences(MC_2)
    dif_credible_interval = MC_1.credible_interval_of_differences_percentile(MC_2)
    dif_credible_interval_gaussian_assumption = MC_1.credible_interval_of_differences_gaussian_assumption(MC_2)
    prop_uit_higher_score_than_uio = MC_1.probability_higher_score_than_other(MC_2)

    scale_expected_value_1 = MC_1.expected_value()
    scale_expected_value_2 = MC_2.expected_value()
    scale_variance_1 = MC_1.variance()
    scale_variance_2 = MC_2.variance()


    significant = dif_credible_interval[0] > 0  or dif_credible_interval[1] < 0
    if gate_on_significance and not significant:
        return

    if print_results:
        print(F"Expected value for actor 1: {scale_expected_value_1}")
        print(F"Expected value for actor 2: {scale_expected_value_2}")
        print(F"Variance for actor 1: {scale_variance_1}")
        print(F"Variance for actor 2: {scale_variance_2}")

    print(f"{MC_1.expected_values = }")

    # ---------------------------------plotting---------------------------------
    plot_raw_histogram(example_question_1=example_question_1, 
                       example_question_2=example_question_2, 
                       folder=folder)

    plot_prior(example_question_1=example_question_1, 
               uit_p_prior_mean=uit_p_prior_mean, 
               uit_p_prior_variance=uit_p_prior_variance, 
               BI1=BI1, 
               example_question_2=example_question_2, 
               uio_p_prior_mean=uio_p_prior_mean, 
               uio_p_prior_variance=uio_p_prior_variance, 
               BI2=BI2,
               folder=folder, 
               with_marginalized_distributions=True)

    plot_posterior(example_question_1=example_question_1, 
                   uit_p_mean=uit_p_mean, 
                   uit_p_variance=uit_p_variance, BI1=BI1,
                   example_question_2=example_question_2, 
                   uio_p_mean=uio_p_mean, 
                   uio_p_variance=uio_p_variance, BI2=BI2,
                   folder=folder, 
                   with_marginalized_distributions=True)
    
    plot_mean_score_with_error_bars(example_question_1=example_question_1, 
                                    example_question_2=example_question_2,
                                    scale_expected_value_1=scale_expected_value_1, 
                                    scale_expected_value_2=scale_expected_value_2,
                                    scale_variance_1=scale_variance_1, 
                                    scale_variance_2=scale_variance_2, 
                                    folder=folder, )

    plot_distribution_of_differences(example_question_1=example_question_1, 
                                     dif_samples=dif_samples, 
                                     dif_credible_interval=dif_credible_interval, 
                                     dif_credible_interval_gaussian_assumption=dif_credible_interval_gaussian_assumption, 
                                     prop_uit_higher_score_than_uio=prop_uit_higher_score_than_uio,
                                     folder=folder)
    close() #close plots


    return MC_1, MC_2

def main():

    # paths to the data
    uit_dataset_path = (r"..\BaseGeo_2_0\all data excel"  
                        + r"\uit.3.stud.data-98073-2024-02-15-1532.xlsx")
    uio_dataset_path = (r"..\BaseGeo_2_0\all data excel"
                        + r"\uio.4.stud.data-112060-2024-02-15-1625 (1).xlsx")
    
    # load using custom Survey class
    uit_survey = Survey(uit_dataset_path)
    uio_survey = Survey(uio_dataset_path)

    # perform_analysis(uit_survey, uio_survey, question="Laboratory skills", print_results=1, gate_on_significance=0)
    # perform_analysis(uit_survey, uio_survey, question="Laboratory skills.1", print_results=1, gate_on_significance=0)
    # perform_analysis(uit_survey, uio_survey, question="Spatial skills (romlig forståelse)", print_results=1, gate_on_significance=0)
    # perform_analysis(uit_survey, uio_survey, question="Spatial skills (romlig forståelse).1", print_results=1, gate_on_significance=0)
    
    MC_uit, MC_uio = perform_analysis(uit_survey, uio_survey, question="i feel comfortable as a student here", 
                     print_results=0, gate_on_significance=False, folder="example_plots", use_libraries=True)
    if animate:
        animate_monte_carlo_sampling(MC_uit, MC_uio, num_frames=1000, folder="example_plots", example_question_1=uit_survey.search("i feel comfortable as a student here"))
    # for question in uit_survey.questions:
    #     perform_analysis(uit_survey, uio_survey, question=question.raw_text, print_results=0, gate_on_significance=1)
    #     perform_analysis(uit_survey, uio_survey, question=question.raw_text, print_results=0, gate_on_significance=1)

if __name__ == "__main__":
    main()