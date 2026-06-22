

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots, close
from plots import *

from checks import check_pair_of_questions
from actors import Survey
from hierarchical_modeling import find_posterior_distribution
import arviz as az

def test_hierarchical_model(question1, question2, load_from_saved_traces=False, quiet=False):

    if not load_from_saved_traces:
        uib_2019_survey_path = r"..\2019data\uib_2019_students.xlsx"
        uibgeophys_2019_survey_path = r"..\2019data\uibgeophys_2019_students.xlsx"
        uio_2019_survey_path = r"..\2019data\uio_2019_students.xlsx"
        uit_2019_survey_path = r"..\2019data\uit_2019_students.xlsx"
        unis_2019_survey_path = r"..\2019data\unis_2019_students.xlsx"

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

        question1s = [uib_2019_question1, uibgeophys_2019_question1, uio_2019_question1, uit_2019_question1, unis_2019_question1]
        question2s = [uib_2019_question2, uibgeophys_2019_question2, uio_2019_question2, uit_2019_question2, unis_2019_question2]

        check_pair_of_questions(question1s, question2s)

        # ----------------------------Run the hierarchical model----------------------------
        
        trace_question1 = find_posterior_distribution(
            uib_2019_question1,
            uibgeophys_2019_question1,
            uio_2019_question1,
            uit_2019_question1,
            unis_2019_question1,
            quiet=quiet
            )
        
        trace_question2 = find_posterior_distribution(
            uib_2019_question2,
            uibgeophys_2019_question2,
            uio_2019_question2,
            uit_2019_question2,
            unis_2019_question2,
            quiet=quiet
            )

        # save scores 
        scores_y1 = trace_question1.posterior['group_mean_scores'].values.reshape(-1, 5)
        scores_y2 = trace_question2.posterior['group_mean_scores'].values.reshape(-1, 5)
        population_mean_1 = trace_question1.posterior["population_mean_score"].values.flatten()
        population_mean_2 = trace_question2.posterior["population_mean_score"].values.flatten()
        np.save("..\\scores\\hierarchical_modeling\\score1.npy", scores_y1)
        np.save("..\\scores\\hierarchical_modeling\\score2.npy", scores_y2)
        np.save("..\\scores\\hierarchical_modeling\\mean_pop_score1.npy", population_mean_1)
        np.save("..\\scores\\hierarchical_modeling\\mean_pop_score2.npy", population_mean_2)
        # use arviz for a raw plot/diagnostics
        filename1 = f"Arviz raw posteriors {sanitize_key(question1)}"
        filename2 = f"Arviz raw posteriors {sanitize_key(question2)}"
        azplot1 = az.plot_trace_dist(trace_question1, combined=True)
        azplot2 = az.plot_trace_dist(trace_question2, combined=True)
        azplot1.add_title(filename1 + f"\n{question1s[0].year}")
        azplot2.add_title(filename2 + f"\n{question2s[0].year}")
        azplot1.savefig(f"..\\figures\\hierarchical_modeling test\\{filename1}.png")
        azplot2.savefig(f"..\\figures\\hierarchical_modeling test\\{filename2}.png")
    else:
        print("loading...")
        scores_y1 = np.load("..\\scores\\hierarchical_modeling\\score1.npy")
        scores_y2 = np.load("..\\scores\\hierarchical_modeling\\score2.npy")
        population_mean_1 = np.load("..\\scores\\hierarchical_modeling\\mean_pop_score1.npy")
        population_mean_2 = np.load("..\\scores\\hierarchical_modeling\\mean_pop_score2.npy")
    
    print("calculating difference distributions...")
    # 4. Calculate the difference distribution per group
    difference_distribution = scores_y2 - scores_y1

    # Now you can calculate credible intervals for the change in each university group!
    # e.g., for Group 0 (UiB):
    uib_change = difference_distribution[:, 0]    # example use       
    lower_bound = np.percentile(uib_change, 2.5)  #           
    upper_bound = np.percentile(uib_change, 97.5) #           

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
    axs[1, 2].set_title("Change in population", fontsize=ax_title_fs)
    for ax in axs.flatten(): 
        ax.tick_params(axis="both", which="major", labelsize=fig_tick_fs, labelbottom=True)
        ax.legend()
    fig.suptitle("Example use of the hierarchical method", fontsize=fig_title_fs)

    fig.tight_layout()
    filename = f"change_in_{sanitize_key(question1)}_to_{sanitize_key(question2)}"
    print(f"saving as {filename}")
    fig.savefig(f"..\\figures\\hierarchical_modeling test\\{filename}.png")
