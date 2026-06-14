
# import pandas as pd
# import re
# from pathlib import Path

# from histogramming import make_raw_histograms

from os import listdir
import numpy as np
from matplotlib.pyplot import subplots, show, close, title
from monte_carlo import MonteCarloSampler
from actors import *
# from histogramming import sanitize_key
from plot_config import *

from bayesian_inference import *

global data_folder, figure_folder
data_folder = "BaseGeo_2_0\\all data exel"
figure_folder = "BaseGeo_2_0\\figures"

# control flags
make_raw_histograms = 0


def sanitize_key(key):
    bad_chars = [
        "?", "/", "."
    ]
    for bad_char in bad_chars:
        key = key.replace(bad_char, "")
    return key



def perform_analysis(survey1, survey2, question, print_results=True, gate_on_significance=False):
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
    # ensure that the two questions are the same


    if example_question_1.raw_text != example_question_2.raw_text:
        return 

    if example_question_1.axis == (None, None) and example_question_2.axis == (None, None):
        return     
    
    if example_question_1.axis != example_question_2.axis:
        return 

    # initialize the BayesianInference class   
    BI1 = BayesianInference(example_question_1)
    BI2 = BayesianInference(example_question_2)
    # do the inference 
    BI1.bayesian_inference()
    BI2.bayesian_inference()

    # do monte carlo sampling to estimate average score on scale and uncertainty
    MC_1 = MonteCarloSampler(BI1.posterior_dist)
    MC_2 = MonteCarloSampler(BI2.posterior_dist)

    # extract results
    uit_p_mean = BI1.expected_value()
    uio_p_mean = BI2.expected_value()
    uit_p_variance = BI1.variance()
    uio_p_variance = BI2.variance()

    # UiT - UiO
    dif_samples = MC_1.probability_dist_of_differences(MC_2)
    dif_conf_interval = MC_1.confidence_interval_of_differences(MC_2)
    dif_conf_interval_gaussian_assumption = MC_1.confidence_interval_of_differences_gaussian_assumption(MC_2)

    scale_expected_value_1 = MC_1.expected_value()
    scale_expected_value_2 = MC_2.expected_value()
    scale_variance_1 = MC_1.variance()
    scale_variance_2 = MC_2.variance()


    significant = dif_conf_interval[0] > 0  or dif_conf_interval[1] < 0
    if gate_on_significance and not significant:
        return

    if print_results:
        print(F"Expected value for actor 1: {scale_expected_value_1}")
        print(F"Expected value for actor 2: {scale_expected_value_2}")
        print(F"Variance for actor 1: {scale_variance_1}")
        print(F"Variance for actor 2: {scale_variance_2}")
    
    # plot the posterior distributions as a bar plot with std error bars
    fig_posterior_dist, axs_posterior_dist = subplots(1, 2, figsize=(20, 10))
    axs_posterior_dist[0].bar(example_question_1.counts.index, uit_p_mean, 
                                yerr=uit_p_variance**0.5, capsize=30)
    axs_posterior_dist[1].bar(example_question_2.counts.index, uio_p_mean, 
                                yerr=uio_p_variance**0.5, capsize=30)
    
    # plot formatting
    axs_posterior_dist[0].set_title(f"Posterior distribution for UiT\nquestion: "
                                        + f"{example_question_1.raw_text}", 
                                        fontsize=fig_title_fs)
    axs_posterior_dist[0].set_xlabel("Response", fontsize=fig_axis_fs)
    axs_posterior_dist[0].set_ylabel("Density", fontsize=fig_axis_fs)
    axs_posterior_dist[0].tick_params(axis='both', which='major', 
                                        labelsize=fig_tick_fs, rotation=45)

    axs_posterior_dist[1].set_title(f"Posterior distribution for UiO\nquestion: "
                                        + f"{example_question_2.raw_text}", 
                                        fontsize=fig_title_fs)
    axs_posterior_dist[1].set_xlabel("Response", fontsize=fig_axis_fs)
    axs_posterior_dist[1].set_ylabel("Density", fontsize=fig_axis_fs)
    axs_posterior_dist[1].tick_params(axis='both', which='major', 
                                        labelsize=fig_tick_fs, rotation=45)
    fig_posterior_dist.tight_layout()
    fig_posterior_dist.savefig("..\\" + figure_folder + "\\" 
                + "bayesian_inference\\" + f"posterior {sanitize_key(example_question_1.raw_text)}.png")

    
    # plot the expected value with error bars representing the variance
    fig_sample_means, ax_sample_means = subplots(figsize=(10, 5))
    ax_sample_means.errorbar([scale_expected_value_1, scale_expected_value_2], [r"UiT $\mathbb{E}[\mu] \pm \sigma_\mu$", r"UiO $\mathbb{E}[\mu] \pm \sigma_\mu$"], 
                xerr=[scale_variance_1**0.5, scale_variance_2**0.5], fmt='o', capsize=10)

    ax_sample_means.set_title(f"Expected value of the survey scale with Monte Carlo sampling\n"
                    + f"question: {sanitize_key(example_question_1.raw_text)}\n",
                    fontsize=fig_title_fs)
    ax_sample_means.set_xlabel("Expected value", fontsize=fig_axis_fs)
    ax_sample_means.tick_params(axis='both', which='major', labelsize=fig_tick_fs)
    fig_sample_means.tight_layout()
    fig_sample_means.savefig("..\\" + figure_folder + "\\" 
                + "bayesian_inference\\" + f"expected_value_dist {sanitize_key(example_question_1.raw_text)}.png")


    fig_dif_prop_dist, ax_dif_prop_dist = subplots(figsize=(10, 5))

    ax_dif_prop_dist.hist(dif_samples, bins=1000, density=True)
    ax_dif_prop_dist.set_title(f"Distribution of differences in expected values between UiT and UiO\n"
                    + f"question: {sanitize_key(example_question_1.raw_text)}\n",
                    fontsize=fig_title_fs)
    ax_dif_prop_dist.axvline(dif_conf_interval[0], color='red', linestyle='--', label="95% conf. interval (Percentiles)")
    ax_dif_prop_dist.axvline(dif_conf_interval[1], color='red', linestyle='--')
    ax_dif_prop_dist.axvline(dif_conf_interval_gaussian_assumption[0], color='blue', linestyle='--', label="95% conf. interval (Gaussian assumption)")
    ax_dif_prop_dist.axvline(dif_conf_interval_gaussian_assumption[1], color='blue', linestyle='--')
    ax_dif_prop_dist.legend(fontsize=fig_legend_fs)
    ax_dif_prop_dist.set_xlabel("Difference in Expected Values", fontsize=fig_axis_fs)
    ax_dif_prop_dist.set_ylabel("Density", fontsize=fig_axis_fs)
    ax_dif_prop_dist.set_xlabel(r"$\mathbb{E}[X_{\text{UiT}}] - \mathbb{E}[X_{\text{UiO}}]$", fontsize=fig_axis_fs)
    ax_dif_prop_dist.tick_params(axis='both', which='major', labelsize=fig_tick_fs)

    # ensure x-axis limits are symmetric around zero for better visualization of significance
    max_abs_dif = max(abs(dif_samples.min()), abs(dif_samples.max()))
    ax_dif_prop_dist.set_xlim(-max_abs_dif, max_abs_dif)

    fig_dif_prop_dist.tight_layout()
    fig_dif_prop_dist.savefig("..\\" + figure_folder + "\\"
                + "bayesian_inference\\" + f"difference_in_expected_values distribution {sanitize_key(example_question_1.raw_text)}.png")
    

    close()


def main():

    # paths to the data
    uit_dataset_path = (r"..\BaseGeo_2_0\all data exel"  
                        + r"\uit.3.stud.data-98073-2024-02-15-1532.xlsx")
    uio_dataset_path = (r"..\BaseGeo_2_0\all data exel"
                        + r"\uio.4.stud.data-112060-2024-02-15-1625 (1).xlsx")
    
    # load using custom Survey class
    uit_survey = Survey(uit_dataset_path)
    uio_survey = Survey(uio_dataset_path)
    
    for i in range(len(uit_survey.questions)):
        if uit_survey.questions[i].raw_text[0] == "L":
            print(f"Question {i}: {uit_survey.questions[i].raw_text}")

    # for question in uit_survey.questions:
    #     if question.raw_text[0] == "L":
    #         print(f"Analyzing question: {question.raw_text}")

    perform_analysis(uit_survey, uio_survey, question="Laboratory skills", print_results=1, gate_on_significance=0)
    perform_analysis(uit_survey, uio_survey, question="Laboratory skills.1", print_results=1, gate_on_significance=0)
    # for question in uit_survey.questions:
    #     perform_analysis(uit_survey, uio_survey, question=question.raw_text, print_results=0, gate_on_significance=1)
    #     perform_analysis(uit_survey, uio_survey, question=question.raw_text, print_results=0, gate_on_significance=1)


    if make_raw_histograms:
        files = listdir(data_folder)
        for file in files:
            print(f"{file}")
            data = pd.read_excel(data_folder + "\\" + file)
            path = figure_folder + "\\" + file[:-5] + "\\" + "raw_histograms"
            Path(path).mkdir(parents=True, exist_ok=True)
            make_raw_histograms(data, path, quiet=1, use_only_known_axes=1)


if __name__ == "__main__":
    main()