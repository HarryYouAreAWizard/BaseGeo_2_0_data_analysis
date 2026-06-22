#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: __main__.py
Author: Noah Nielsen
Date: 2026-04-18
Description: This script performs data analysis on the BaseGeo 2.0 survey data and generates plots.
"""

from actors import Survey
from plots import sanitize_key

#  global data_folder, figure_folder

def check_set_question_and_axes(questions):
    number_of_questions_without_axes = 0
    for q in questions:
        if q.axis is None:
            number_of_questions_without_axes += 1

    # handle case where there are no axes
    if number_of_questions_without_axes == 5:
        print(f"all questions missing axes, cannot compare")
        return
    
    # handle case where one detect_axis failed
    if number_of_questions_without_axes == 1:
        print(f"one question missing an axis, attempting to continue")

        # find the likely correct axis
        for q in questions:
            if q.axis is not None:
                proper_axis = q.axis

        # update the question missing an axis
        for q in questions:
            if q.axis is None:
                q.axis = proper_axis
            elif q.axis != proper_axis:
                print(f"inconsistent axes, cannot compare")
                return


    return

def check_pair_of_questions(question1s, question2s):
    """handling potential issues with questions"""
    
    # ensure that the question actually were found in all surveys
    for q in question1s + question2s:
        if isinstance(q, int):
            # .search returns 0 if question not found
            return
        
    check_set_question_and_axes(question1s)
    check_set_question_and_axes(question2s)

    if question1s[0].axis != question2s[0].axis:
        print("questions have different axes, cannot compare")
        # inconsistent axes
        return

    return 


