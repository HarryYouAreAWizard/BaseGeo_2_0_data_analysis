#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: __main__.py
Author: Noah Nielsen
Date: 2026-04-18
Description: This script performs data analysis on the BaseGeo 2.0 survey data and generates plots.
"""



import os
from pdb import pm

from actors import Survey
from bayesian_inference import Categorial2Dirichlet
from monte_carlo import DirichletSampler
from plots import *

from hierarchical_modeleing import find_posterior_distribution
#  global data_folder, figure_folder
data_folder = "BaseGeo_2_0\\all data excel"
figure_folder = "BaseGeo_2_0\\figures"


def perform_analysis(survey1, survey2, question, 
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

def find_viable_questions(survey1, survey2):
    """go thorugh two surveys and return a list of questions that are viable
    
    criteria for viability:
     - the questions must be the same
     - the axes must be well-defined
     - the axes must be the same
    
    """

    viable_questions = []
    for question1 in survey1.questions:
        for question2 in survey2.questions:
            if (question1.raw_text == question2.raw_text 
                and question1.axis is not None 
                and question2.axis is not None 
                and question1.axis == question2.axis):

                viable_questions.append(question1.raw_text)

    return viable_questions

def write_viable_questions():
    survey_educator_2019_path = r"2019data\data_2019_educators_reduced_questions.xlsx"
    survey_educator_2026_path = r"2026data\data_2026_educators.xlsx"
    survey_admintech_2019_path = r"2019data\data_2019_admintech_reduced_questions.xlsx"
    survey_admintech_2026_path = r"2026data\data_2026_admintech.xlsx"
    survey_student_2019_path = r"2019data\data_2019_students_reduced_questions.xlsx"
    survey_student_2026_path = r"2026data\data_2026_students.xlsx"
    

    survey_educator_2019_path = r"2019data\uit_2019_educators.xlsx"
    survey_educator_2026_path = r"2026data\uit_2026_educators.xlsx"
    survey_admintech_2019_path = r"2019data\uit_2019_admintech.xlsx"
    survey_admintech_2026_path = r"2026data\uit_2026_admintech.xlsx"
    survey_student_2019_path = r"2019data\uit_2019_students.xlsx"
    survey_student_2026_path = r"2026data\uit_2026_students.xlsx"
    survey_educator_2019 = Survey(survey_educator_2019_path)
    survey_educator_2026 = Survey(survey_educator_2026_path)
    survey_admintech_2019 = Survey(survey_admintech_2019_path)
    survey_admintech_2026 = Survey(survey_admintech_2026_path)
    survey_student_2019 = Survey(survey_student_2019_path)
    survey_student_2026 = Survey(survey_student_2026_path)

    viable_questions_educator = find_viable_questions(survey1=survey_educator_2019,
                                             survey2=survey_educator_2026,)
    viable_questions_admintech = find_viable_questions(survey1=survey_admintech_2019,
                                             survey2=survey_admintech_2026,)
    viable_questions_student = find_viable_questions(survey1=survey_student_2019,
                                             survey2=survey_student_2026,)
    


    with open(r"viable_questions\viable_questions.txt", mode="w") as doc:

        doc.write("\subsection{Viable questions educator}\n")
        for viable_question in viable_questions_educator: doc.write(f"\\\\ {viable_question}\n")
        doc.write("\clearpage\n\n\subsection{Viable questions admintech}\n")
        for viable_question in viable_questions_admintech: doc.write(f"\\\\ {viable_question}\n")
        doc.write("\clearpage\n\n\subsection{Viable questions student}\n")
        for viable_question in viable_questions_student: doc.write(f"\\\\ {viable_question}\n")

    return 

def test_hierarchical_model(question1, question2, load_from_saved_traces=False):

    if not load_from_saved_traces:
        uib_2019_survey_path = r"2019data\uib_2019_students.xlsx"
        uibgeophys_2019_survey_path = r"2019data\uibgeophys_2019_students.xlsx"
        uio_2019_survey_path = r"2019data\uio_2019_students.xlsx"
        uit_2019_survey_path = r"2019data\uit_2019_students.xlsx"
        unis_2019_survey_path = r"2019data\unis_2019_students.xlsx"

        uib_2019_survey = Survey(uib_2019_survey_path)
        uibgeophys_2019_survey = Survey(uibgeophys_2019_survey_path)
        uio_2019_survey = Survey(uio_2019_survey_path) 
        uit_2019_survey = Survey(uit_2019_survey_path)
        unis_2019_survey = Survey(unis_2019_survey_path)
        
        uib_2019_question1 = uib_2019_survey.search(question1)
        uibgeophys_2019_question1 = uibgeophys_2019_survey.search(question1)
        uio_2019_question1 = uio_2019_survey.search(question1)
        uit_2019_question1 = uit_2019_survey.search(question1)
        unis_2019_question1 = unis_2019_survey.search(question1)
        uib_2019_question2 = uib_2019_survey.search(question2)
        uibgeophys_2019_question2 = uibgeophys_2019_survey.search(question2)
        uio_2019_question2 = uio_2019_survey.search(question2)
        uit_2019_question2 = uit_2019_survey.search(question2)
        unis_2019_question2 = unis_2019_survey.search(question2)
        
        trace_question1 = find_posterior_distribution(
            uib_2019_question1,
            uibgeophys_2019_question1,
            uio_2019_question1,
            uit_2019_question1,
            unis_2019_question1)
        
        trace_question2 = find_posterior_distribution(
            uib_2019_question2,
            uibgeophys_2019_question2,
            uio_2019_question2,
            uit_2019_question2,
            unis_2019_question2)

        # save scores 
        scores_y1 = trace_question1.posterior['expected_scores'].values.reshape(-1, 5)
        scores_y2 = trace_question2.posterior['expected_scores'].values.reshape(-1, 5)
        population_mean_1 = trace_question1.posterior["population_mean_score"].values.flatten()
        population_mean_2 = trace_question2.posterior["population_mean_score"].values.flatten()
        np.save("scores\\hierarchical_modeling\\score1.npy", scores_y1)
        np.save("scores\\hierarchical_modeling\\score2.npy", scores_y2)
        np.save("scores\\hierarchical_modeling\\mean_pop_score1.npy", population_mean_1)
        np.save("scores\\hierarchical_modeling\\mean_pop_score2.npy", population_mean_2)

    else:
        print("loading...")
        scores_y1 = np.load("scores\\hierarchical_modeling\\score1.npy")
        scores_y2 = np.load("scores\\hierarchical_modeling\\score2.npy")
        population_mean_1 = np.load("scores\\hierarchical_modeling\\mean_pop_score1.npy")
        population_mean_2 = np.load("scores\\hierarchical_modeling\\mean_pop_score2.npy")

    
    print("calculating difference distributions...")
    # 4. Calculate the difference distribution per group
    difference_distribution = scores_y2 - scores_y1

    # Now you can calculate credible intervals for the change in each university group!
    # e.g., for Group 0 (UiB):
    uib_change = difference_distribution[:, 0]
    lower_bound = np.percentile(uib_change, 2.5)
    upper_bound = np.percentile(uib_change, 97.5)

    uib_change = difference_distribution[:, 0]
    uibgeophys_change = difference_distribution[:, 1]
    uio_change = difference_distribution[:, 2]
    uit_change = difference_distribution[:, 3]
    unis_change = difference_distribution[:, 4]
    total_change = population_mean_2 - population_mean_1
    print(f"{total_change.shape = }")
    # bounds for 95% credible interval
    uib_lower_bound = np.percentile(uib_change, 2.5)
    uibgeophys_lower_bound = np.percentile(uibgeophys_change, 2.5)
    uio_lower_bound = np.percentile(uio_change, 2.5)
    uit_lower_bound = np.percentile(uit_change, 2.5)
    unis_lower_bound = np.percentile(unis_change, 2.5)
    total_lower_bound = np.percentile(total_change, 2.5)
    uib_upper_bound = np.percentile(uib_change, 97.5)
    uibgeophys_upper_bound = np.percentile(uibgeophys_change, 97.5)
    uio_upper_bound = np.percentile(uio_change, 97.5)
    uit_upper_bound = np.percentile(uit_change, 97.5)
    unis_upper_bound = np.percentile(unis_change, 97.5)
    total_upper_bound = np.percentile(total_change, 97.5)

    print("plotting...")
    # plot the difference dist for each group and for the total distribution
    fig, axs=subplots(2, 3, figsize=(12, 8), sharex=True, sharey=True)
    bins = 100
    # histograms
    axs[0, 0].hist(uib_change, bins=bins, density=True)
    axs[0, 1].hist(uibgeophys_change, bins=bins, density=True)
    axs[0, 2].hist(uio_change, bins=bins, density=True)
    axs[1, 0].hist(uit_change, bins=bins, density=True)
    axs[1, 1].hist(unis_change, bins=bins, density=True)
    axs[1, 2].hist(total_change, bins=bins, density=True)
    # vlines
    axs[0, 0].vlines([uib_lower_bound, uib_upper_bound], 0, 3.5, label="95% cred. interval")
    axs[0, 1].vlines([uibgeophys_lower_bound, uibgeophys_upper_bound], 0, 3.5, label="95% cred. interval")
    axs[0, 2].vlines([uio_lower_bound, uio_upper_bound], 0, 3.5, label="95% cred. interval")
    axs[1, 0].vlines([uit_lower_bound, uit_upper_bound], 0, 3.5, label="95% cred. interval")
    axs[1, 1].vlines([unis_lower_bound, unis_upper_bound], 0, 3.5, label="95% cred. interval")
    axs[1, 2].vlines([total_lower_bound, total_upper_bound], 0, 3.5, label="95% cred. interval")

    axs[0, 0].set_title("Change in UiB", fontsize=ax_title_fs)
    axs[0, 1].set_title("Change in UiB Geophysics", fontsize=ax_title_fs)
    axs[0, 2].set_title("Change in UiO", fontsize=ax_title_fs)
    axs[1, 0].set_title("Change in UiT", fontsize=ax_title_fs)
    axs[1, 1].set_title("Change in UNIS", fontsize=ax_title_fs)
    axs[1, 2].set_title("Change in overall population", fontsize=ax_title_fs)
    for ax in axs.flatten(): 
        ax.tick_params(axis="both", which="major", labelsize=fig_tick_fs, labelbottom=True)
        ax.legend()
    fig.suptitle("Example use of the hierarchical method", fontsize=fig_title_fs)

    fig.tight_layout()
    fig.savefig(f"figures\\hierarchical_modeling\\change_in_{question1}_to_{question2}.png")

    close()

def main():
    test_hierarchical_model(
        "Fieldwork skills.1",
        "Fieldwork skills",
        load_from_saved_traces=False)
    # write_viable_questions()

    

if __name__ == "__main__":
    main()