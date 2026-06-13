
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
        
        # paths to the data
        uit_dataset_path = (r"..\BaseGeo_2_0\all data exel"  
                            + r"\uit.3.stud.data-98073-2024-02-15-1532.xlsx")
        uio_dataset_path = (r"..\BaseGeo_2_0\all data exel"
                            + r"\uio.4.stud.data-112060-2024-02-15-1625 (1).xlsx")
        # load using custom Survey class
        uit_survey = Survey(uit_dataset_path)
        uio_survey = Survey(uio_dataset_path)

        # pick out the specific question to analyze
        uit_example_question = uit_survey.questions()[100] 
        uio_example_question = uio_survey.questions()[100]

        # initialize the BayesianInference class
        uit_BI = BayesianInference(uit_example_question)
        uio_BI = BayesianInference(uio_example_question)

        # do the inference 
        uit_p_posterior = uit_BI.bayesian_inference()
        uio_p_posterior = uio_BI.bayesian_inference()

        # extract results
        uit_p_mean = uit_BI.expected_value()
        uio_p_mean = uio_BI.expected_value()
        uit_p_variance = uit_BI.variance()
        uio_p_variance = uio_BI.variance()

        # plot the posterior distributions as a bar plot with std error bars
        fig, axs = subplots(1, 2, figsize=(15, 10))
        axs[0].bar(uit_example_question.counts.index, uit_p_mean, 
                   yerr=uit_p_variance**0.5, capsize=30)
        axs[1].bar(uio_example_question.counts.index, uio_p_mean, 
                   yerr=uio_p_variance**0.5, capsize=30)
        
        # plot formatting
        axs[0].set_title(f"Posterior distribution for UiT\nquestion: "
                          + f"{uit_example_question.raw_text}", 
                          fontsize=fig_title_fs)
        axs[0].set_xlabel("Response", fontsize=fig_axis_fs)
        axs[0].set_ylabel("Density", fontsize=fig_axis_fs)
        axs[0].tick_params(axis='both', which='major', 
                           labelsize=fig_tick_fs, rotation=45)

        axs[1].set_title(f"Posterior distribution for UiO\nquestion: "
                          + f"{uio_example_question.raw_text}", 
                          fontsize=fig_title_fs)
        axs[1].set_xlabel("Response", fontsize=fig_axis_fs)
        axs[1].set_ylabel("Density", fontsize=fig_axis_fs)
        axs[1].tick_params(axis='both', which='major', 
                           labelsize=fig_tick_fs, rotation=45)
        fig.tight_layout()
        fig.savefig("..\\" + figure_folder + "\\" 
                    + "example_plots\\" + "example_posterior.png")


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