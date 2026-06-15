



"""
animating aspects from the the data analysis 
"""
from plot_config import *
# from main import sanitize_key


def animate_monte_carlo_sampling(monte_carlo_sampler_1, monte_carlo_sampler_2, num_frames=100, folder=None, example_question_1=None):
    """Animate the Monte Carlo sampling process by plotting the distribution of the posterior
    distrbutions on their own axes along with the distribution of the difference between mean
    on a third axis, as the number of samples increases. """
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots(3, 1, figsize=(10, 5))

    def update(frame):
        for a in ax:
            a.clear()

        p_sample_1 = monte_carlo_sampler_1.samples[frame]
        p_sample_2 = monte_carlo_sampler_2.samples[frame]
        difference_dist = monte_carlo_sampler_1.dif_prop_dist[:frame]


        mean_score_1 = monte_carlo_sampler_1.expected_values[frame] - 1 # subtract 1 to get the x position correct
        mean_score_2 = monte_carlo_sampler_2.expected_values[frame] - 1

        # ax[0].vlines(0, 0, ax[0].get_ylim()[1], colors='black') # to check position encodin of .bar
        
        ax[0].bar(example_question_1.counts.index, p_sample_1)
        ax[1].bar(example_question_1.counts.index, p_sample_2)
        ax[2].hist(difference_dist, bins=100, density=True)

        ax[0].vlines(mean_score_1, 0, ax[0].get_ylim()[1], colors='red', linestyles='dashed', label=f"Mean: {mean_score_1:.2f}")
        ax[1].vlines(mean_score_2, 0, ax[1].get_ylim()[1], colors='red', linestyles='dashed', label=f"Mean: {mean_score_2:.2f}")

        ax[2].set_title(f"Difference in mean score\n{frame}", fontsize=fig_title_fs)
    
        ax[0].set_title(f"UiT", fontsize=fig_title_fs)
        ax[0].set_ylabel("Density", fontsize=fig_axis_fs)
        ax[1].set_title(f"UiO", fontsize=fig_title_fs)
        ax[1].set_ylabel("Density", fontsize=fig_axis_fs)
        ax[2].set_xlabel(r"$\mathbb{E}[X_\text{UiT}] - \mathbb{E}[X_\text{UiO}]$", fontsize=fig_axis_fs)
        fig.tight_layout()

        print(f"Frame {frame+1}/{num_frames}", end="\r")

    
    anim = FuncAnimation(fig, update, frames=num_frames, interval=33, repeat=False)
    
    # if folder is not None and example_question_1 is not None:
    anim.save("figures\\" + folder + "\\" + f"monte_carlo_sampling {example_question_1.raw_text}.gif", writer='imagemagick')
    
    plt.close(fig)