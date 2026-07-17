
"""
file: parameter_recovery.py
author: Noah Nielsen
date: 2026-04-18
This module provides functions for simulating survey data and testing the 
parameter recovery of the proportional odds ordinal logistic regression 
model implemented in proportional_odds_ordinal_logistic_regression.py.
"""

import numpy as np
import pandas as pd

year_2019 = 0
year_2026 = 1


# simulate a survey with distinct values for each group and year, and then fit the model to see if it can recover the parameters.

def make_data(shift):
    n_samples = 1000
    year = np.random.choice([year_2019, year_2026], size=n_samples)
    institution = np.random.choice([0, 1, 2, 3, 4], size=n_samples)
    
    base_score = 4.0
    
    # Apply shift
    interaction_effect = (
        - shift * ((year == year_2026) & (institution == 0))
        + shift * ((year == year_2026) & (institution == 1))
    )
    
    # Add Standard Logistic Noise, epsilon ~ Logistic(location=0, scale=1.0)
    # noise chosen to match the scale of the logistic distribution used in the OrderedLogistic likelihood
    noise = np.random.logistic(0, 1.0, size=n_samples)
    
    # Continuous latent rating
    latent_rating = base_score + interaction_effect + noise
    
    # map to some choice Ordinal Categories using Thresholds (Cutpoints)
    thresholds = [1.5, 2.5, 3.8, 4.5, 5.5, 6.5]
    
    # np.digitize returns indices from 0 to len(thresholds)
    # Adding 1 converts it to a 1-7 scale rating
    explicit_rating = np.digitize(latent_rating, thresholds) + 1
    
    df = pd.DataFrame({
        "latent_rating": latent_rating,
        "explicit_rating": explicit_rating,
        "year": year,
        "institution": institution
    })
    return df
