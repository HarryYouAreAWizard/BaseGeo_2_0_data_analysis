#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: plot_config.py
Author: Noah Nielsen
Created: 2026-06-16
Description: Configuration module for plot styling.
"""

#  global data_folder, figure_folder
data_folder = "BaseGeo_2_0\\all data excel"
figure_folder = "BaseGeo_2_0\\figures"



fig_title_fs = 20
fig_axis_fs = 16
fig_tick_fs = 12
fig_legend_fs = 12

ax_title_fs = 16
ax_axis_fs = 12
ax_tick_fs = 10

def sanitize_key(key):
    bad_chars = [
        "?", "/", "."
    ]
    for bad_char in bad_chars:
        key = key.replace(bad_char, "")
    return key

