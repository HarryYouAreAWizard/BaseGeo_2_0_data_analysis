
# import pandas as pd
# import re
# from pathlib import Path

# from histogramming import make_raw_histograms

from os import listdir
import numpy as np
from matplotlib.pyplot import subplots, show, close, title
from pyparsing import alphas
from monte_carlo import MonteCarloSampler
from actors import *
# from histogramming import sanitize_key
from plot_config import *

from bayesian_inference import *

global data_folder, figure_folder
data_folder = "BaseGeo_2_0\\all data excel"
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

def plot_histogram(example_question_1=None, example_question_2=None, folder=None):
    # plot a histogram of the raw data
    fig_raw_histogram, axs_raw_histogram = subplots(2, 1, figsize=(10, 15))
    axs_raw_histogram[0].bar(example_question_1.counts.index, example_question_1.counts.values)
    axs_raw_histogram[1].bar(example_question_2.counts.index, example_question_2.counts.values)
    axs_raw_histogram[0].set_title(f"Histogram UiT\nquestion: "
                                        + f"{example_question_1.raw_text}", 
                                        fontsize=fig_title_fs)
    axs_raw_histogram[0].set_xlabel("Response", fontsize=fig_axis_fs)
    axs_raw_histogram[0].set_ylabel("Density", fontsize=fig_axis_fs)
    axs_raw_histogram[0].tick_params(axis='both', which='major', 
                                        labelsize=fig_tick_fs, rotation=45)
    axs_raw_histogram[1].set_title(f"Histogram UiO\nquestion: "
                                        + f"{example_question_2.raw_text}", 
                                        fontsize=fig_title_fs)
    axs_raw_histogram[1].set_xlabel("Response", fontsize=fig_axis_fs)
    axs_raw_histogram[1].set_ylabel("Density", fontsize=fig_axis_fs)
    axs_raw_histogram[1].tick_params(axis='both', which='major', 
                                        labelsize=fig_tick_fs, rotation=45)

    fig_raw_histogram.tight_layout()
    fig_raw_histogram.savefig("..\\"+figure_folder+"\\"
                               + folder + f"\\raw {sanitize_key(example_question_1.raw_text)}.png")



def plot_marginalized_distributions(fig, axs, alphas_uit, alphas_uio):
    alpha_0_uit = np.sum(alphas_uit)
    alpha_0_uio = np.sum(alphas_uio)
    num_categories = len(alphas_uit)
    x = np.linspace(-0.1, 1, 1000)

    for i in range(num_categories):
        a_uit = alphas_uit[i]
        b_uit = alpha_0_uit - a_uit
        y_uit = beta.pdf(x, a_uit, b_uit)
        axs[0,i+1].plot(x, y_uit)
        axs[0,i+1].set_title(f"Marginalized distribution\nfor response {i+1} (UiT)", fontsize=ax_title_fs)
        axs[0,i+1].set_xlabel(f"p(response {i+1})", fontsize=ax_axis_fs)
        axs[0,i+1].set_ylabel("Density", fontsize=ax_axis_fs)
        axs[0,i+1].tick_params(axis='both', which='major', labelsize=ax_tick_fs)

        a_uio = alphas_uio[i]
        b_uio = alpha_0_uio - a_uio
        y_uio = beta.pdf(x, a_uio, b_uio)
        axs[1,i+1].plot(x, y_uio)
        axs[1,i+1].set_title(f"Marginalized distribution\nfor response {i+1} (UiO)", fontsize=ax_title_fs)
        axs[1,i+1].set_xlabel(f"p(response {i+1})", fontsize=ax_axis_fs)
        axs[1,i+1].set_ylabel("Density", fontsize=ax_axis_fs)
        axs[1,i+1].tick_params(axis='both', which='major', labelsize=ax_tick_fs)

def plot_prior(example_question_1=None, uit_p_prior_mean=None, uit_p_prior_variance=None, BI1=None,
               example_question_2=None, uio_p_prior_mean=None, uio_p_prior_variance=None, BI2=None,
               folder=None, with_marginalized_distributions=False):
    # plot the prior distributions of the categorical probabilities
    if with_marginalized_distributions:
        fig_prior_dist, axs_prior_dist = subplots(2, 8, figsize=(30, 15))
    else:
        fig_prior_dist, axs_prior_dist = subplots(2, 1, figsize=(10, 15))
        axs_prior_dist = np.reshape(axs_prior_dist, (2,1)) # reshape to 2x1 for consistent indexing with the marginalized distribution case

    # plot survey 1
    axs_prior_dist[0,0].bar(example_question_1.counts.index, uit_p_prior_mean, 
                            yerr=uit_p_prior_variance**0.5, capsize=30)

    axs_prior_dist[0,0].set_title(f"Prior distribution for UiT\nquestion: "
                                        + f"{example_question_1.raw_text}", 
                                        fontsize=fig_title_fs)
    axs_prior_dist[0,0].set_xlabel("Response", fontsize=fig_axis_fs)
    axs_prior_dist[0,0].set_ylabel("Density", fontsize=fig_axis_fs)
    axs_prior_dist[0,0].tick_params(axis='both', which='major', 
                                        labelsize=fig_tick_fs, rotation=45)
    # plot survey 2
    axs_prior_dist[1,0].bar(example_question_2.counts.index, uio_p_prior_mean, 
                                yerr=uio_p_prior_variance**0.5, capsize=30)
    axs_prior_dist[1,0].set_title(f"Prior distribution for UiO\nquestion: "
                                        + f"{example_question_2.raw_text}", 
                                        fontsize=fig_title_fs)
    axs_prior_dist[1,0].set_xlabel("Response", fontsize=fig_axis_fs)
    axs_prior_dist[1,0].set_ylabel("Density", fontsize=fig_axis_fs)
    axs_prior_dist[1,0].tick_params(axis='both', which='major', 
                                        labelsize=fig_tick_fs, rotation=45)

    if with_marginalized_distributions:
        # plot marginalized distributions for each response category for UiT
        alphas_uit = BI1.prior_alpha
        alphas_uio = BI2.prior_alpha
        plot_marginalized_distributions(fig_prior_dist, axs_prior_dist, alphas_uit, alphas_uio)


    # save plot
    fig_prior_dist.tight_layout()
    fig_prior_dist.savefig("..\\" + figure_folder + "\\" 
                + folder + "\\" + f"prior {sanitize_key(example_question_1.raw_text)}.png")

def plot_posterior(example_question_1=None, uit_p_mean=None, uit_p_variance=None, BI1=None,
                   example_question_2=None, uio_p_mean=None, uio_p_variance=None, BI2=None,
                   folder=None, with_marginalized_distributions=False):
    # plot the posterior distributions of the categorical probabilities
    if with_marginalized_distributions:
        fig_posterior_dist, axs_posterior_dist = subplots(2, 8, figsize=(30, 15))
    else:
        fig_posterior_dist, axs_posterior_dist = subplots(2, 1, figsize=(10, 15))
        axs_posterior_dist = np.reshape(axs_posterior_dist, (2,1)) # reshape to 2x1 for consistent indexing with the marginalized distribution case
    # plot survey 1
    axs_posterior_dist[0,0].bar(example_question_1.counts.index, uit_p_mean, 
                                yerr=uit_p_variance**0.5, capsize=30)
    
    axs_posterior_dist[0,0].set_title(f"Posterior distribution for UiT\nquestion: "
                                        + f"{example_question_1.raw_text}", 
                                        fontsize=fig_title_fs)
    axs_posterior_dist[0,0].set_xlabel("Response", fontsize=fig_axis_fs)
    axs_posterior_dist[0,0].set_ylabel("Density", fontsize=fig_axis_fs)
    axs_posterior_dist[0,0].tick_params(axis='both', which='major', 
                                        labelsize=fig_tick_fs, rotation=45)
    # plot survey 2
    axs_posterior_dist[1,0].bar(example_question_2.counts.index, uio_p_mean, 
                                yerr=uio_p_variance**0.5, capsize=30)
    axs_posterior_dist[1,0].set_title(f"Posterior distribution for UiO\nquestion: "
                                        + f"{example_question_2.raw_text}", 
                                        fontsize=fig_title_fs)
    axs_posterior_dist[1,0].set_xlabel("Response", fontsize=fig_axis_fs)
    axs_posterior_dist[1,0].set_ylabel("Density", fontsize=fig_axis_fs)
    axs_posterior_dist[1,0].tick_params(axis='both', which='major', 
                                        labelsize=fig_tick_fs, rotation=45)
    
    if with_marginalized_distributions:
        alphas_uit = BI1.posterior_alpha
        alphas_uio = BI2.posterior_alpha
        plot_marginalized_distributions(fig_posterior_dist, axs_posterior_dist, alphas_uit, alphas_uio)
        for i, row in enumerate(axs_posterior_dist):
            for j, ax in enumerate(row):
                if j != 0:
                    ax.set_xlim(-0.1, 0.75)
        # save plot
    fig_posterior_dist.tight_layout()
    fig_posterior_dist.savefig("..\\" + figure_folder + "\\" 
                + folder + "\\" + f"posterior {sanitize_key(example_question_1.raw_text)}.png")

def plot_mean_score_with_error_bars(example_question_1=None, example_question_2=None, 
                                    scale_expected_value_1=None, scale_expected_value_2=None,
                                scale_variance_1=None, scale_variance_2=None, folder=None):

    # plot the mean score with error bars (standard deviation)
    fig_sample_means, ax_sample_means = subplots(figsize=(10, 5))
    ax_sample_means.errorbar([scale_expected_value_1, scale_expected_value_2], [r"UiT $\mathbb{E}[\mu] \pm \sigma_\mu$", r"UiO $\mathbb{E}[\mu] \pm \sigma_\mu$"], 
                xerr=[scale_variance_1**0.5, scale_variance_2**0.5], fmt='o', capsize=10)
    # plot confidence intervals of mean score
    ax_sample_means.set_title(f"Expected value of the survey scale with Monte Carlo sampling\n"
                    + f"question: {sanitize_key(example_question_1.raw_text)}\n",
                    fontsize=fig_title_fs)
    ax_sample_means.set_xlabel("Expected value", fontsize=fig_axis_fs)
    ax_sample_means.tick_params(axis='both', which='major', labelsize=fig_tick_fs)
    # save plot
    fig_sample_means.tight_layout()
    fig_sample_means.savefig("..\\" + figure_folder + "\\" 
                + folder + "\\" + f"expected_value_dist {sanitize_key(example_question_1.raw_text)}.png")

def plot_distribution_of_differences(example_question_1=None, dif_samples=None, 
                                     dif_credible_interval=None, dif_credible_interval_gaussian_assumption=None, folder=None):
    # plot the distribution of the differences of mean scores from the Monte Carlo simulations
    fig_dif_prop_dist, ax_dif_prop_dist = subplots(figsize=(10, 5))
    ax_dif_prop_dist.hist(dif_samples, bins=1000, density=True)
    ax_dif_prop_dist.set_title(f"Distribution of differences in expected values between UiT and UiO\n"
                    + f"question: {sanitize_key(example_question_1.raw_text)}\n",
                    fontsize=fig_title_fs)
    # plot confidence intervals of difference of mean scores
    ax_dif_prop_dist.axvline(dif_conf_interval[0], color='red', linestyle='--', label="90% conf. interval (Percentiles)")
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
    # save
    fig_dif_prop_dist.tight_layout()
    fig_dif_prop_dist.savefig("..\\" + figure_folder + "\\"
                + folder + "\\" + f"difference_in_expected_values distribution {sanitize_key(example_question_1.raw_text)}.png")
    




def perform_analysis(survey1, survey2, question, print_results=True, gate_on_significance=False, folder="Bayesian_inference"):
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

    if example_question_1.axis == (None, None) and example_question_2.axis == (None, None):
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
    MC_1 = MonteCarloSampler(BI1.posterior_dist)
    MC_2 = MonteCarloSampler(BI2.posterior_dist)

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


    # ---------------------------------plotting---------------------------------
    plot_histogram(example_question_1=example_question_1, example_question_2=example_question_2, folder=folder)

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
                                     folder=folder)
    close() #close plots


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
    
    perform_analysis(uit_survey, uio_survey, question="i feel comfortable as a student here", 
                     print_results=0, gate_on_significance=False, folder="example_plots")

    # for question in uit_survey.questions:
    #     perform_analysis(uit_survey, uio_survey, question=question.raw_text, print_results=0, gate_on_significance=1)
    #     perform_analysis(uit_survey, uio_survey, question=question.raw_text, print_results=0, gate_on_significance=1)

if __name__ == "__main__":
    main()