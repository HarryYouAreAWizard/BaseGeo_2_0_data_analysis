
# import pandas as pd
# import re
# from pathlib import Path

# from histogramming import make_raw_histograms

from os import listdir
import numpy as np
from matplotlib.pyplot import subplots, show, close, title
from actors import *
from histogramming import sanitize_key
from plot_config import *

from bayesian_inference import *

global data_folder, figure_folder
data_folder = "BaseGeo_2_0\\all data exel"
figure_folder = "BaseGeo_2_0\\figures"

# control flags
plot_example = 1
make_raw_histograms = 0

def example_plot(question, ax, title="Example Plot"):

    counts = question.counts
    density = counts / counts.sum()
    ax.bar(density.index, density.values)
    ax.set_title(title, fontsize=fig_title_fs)
    ax.set_xlabel("Response", fontsize=fig_axis_fs)
    ax.set_ylabel("Density", fontsize=fig_axis_fs)
    ax.tick_params(axis='both', which='major', labelsize=fig_tick_fs, rotation=45)


def main():

    if plot_example:
        
        uit_dataset_path = r"..\BaseGeo_2_0\all data exel\uit.3.stud.data-98073-2024-02-15-1532.xlsx"
        uit_survey = Survey(uit_dataset_path)
        uit_example_question = uit_survey.questions()[100] # pick question number 100 as example

        uio_dataset_path = r"..\BaseGeo_2_0\all data exel\uio.4.stud.data-112060-2024-02-15-1625 (1).xlsx"
        uio_survey = Survey(uio_dataset_path)
        uio_example_question = uio_survey.questions()[100]


        # plot the questions side by side
        fig, axs = subplots(1, 2, figsize=(12, 10))
        example_plot(uit_example_question, axs[0], title=f"UiT\n{uit_example_question.raw_text}")
        example_plot(uio_example_question, axs[1], title=f"UiO\n{uio_example_question.raw_text}")
        fig.tight_layout()
        fig.savefig("..\\" + figure_folder + "\\" + "example_plots\\" + "example_plots" + ".png")

        # do Bayesian inference for the UiT question to find the posterior distribution of propabilities for each response category
        uit_BI = BayesianInference()
        uio_BI = BayesianInference()

        uit_p_posterior = uit_BI.bayesian_inference(uit_example_question.counts)
        uit_p_maximum_likelihood_estimate = uit_BI.maximum_a_posteriori()
        uit_p_variance = uit_BI.variance()
        uit_p_credible_interval = uit_BI.marginal_interval()
    
        print(f"{uit_p_maximum_likelihood_estimate = }")
        print(f"{uit_p_variance = }")
        uit_cred_interval_lower = uit_p_credible_interval[0]
        uit_cred_interval_upper = uit_p_credible_interval[1]
        print(f"UiT credible intervals:")
        for i in range(7):
            print(f"{uit_cred_interval_lower[i]:<5.4f} - {uit_cred_interval_upper[i]:<5.4f},    {uit_cred_interval_upper[i] - uit_cred_interval_lower[i]:<10.4f}")

        # plot the posterior distribution as a bar plot with std error bars
        fig, ax = subplots(figsize=(10, 10))
        ax.bar(uit_example_question.counts.index, uit_p_posterior.mean(), 
               yerr=uit_p_variance**0.5, capsize=30)
        ax.set_title(f"Posterior distribution for UiT question\n{uit_example_question.raw_text}", fontsize=fig_title_fs)
        ax.set_xlabel("Response", fontsize=fig_axis_fs)
        ax.set_ylabel("Density", fontsize=fig_axis_fs)
        ax.tick_params(axis='both', which='major', labelsize=fig_tick_fs, rotation=45)
        fig.tight_layout()
        fig.savefig("..\\" + figure_folder + "\\" + "example_plots\\" + "example_posterior.png")
        close()




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