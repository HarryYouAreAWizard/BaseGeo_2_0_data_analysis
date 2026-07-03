#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: checks.py
Author: Noah Nielsen
Date: 2026-04-22
Description: This script checks questions
"""


#  global data_folder, figure_folder
CHECK_SUCCES = 0
CHECK_MISSING_AXES = 1
CHECK_INCONSISTENT_AXES = 2
CHECK_QUESTION_NOT_FOUND = 3


def check_set_question_and_axes(questions):
    number_of_questions_without_axes = 0
    for q in questions:
        if q.axis is None:
            number_of_questions_without_axes += 1

    # handle case where there are no axes
    if number_of_questions_without_axes == 5:
        # print(f"all questions missing axes, cannot compare")
        return CHECK_MISSING_AXES
    
    # handle case where one detect_axis failed
    if 0 < number_of_questions_without_axes < 5:
        # print(f"one question missing an axis, attempting to continue") 

        # find the likely correct axis
        for q in questions:
            if q.axis is not None:
                proper_axis = q.axis

        # update the question missing an axis
        for q in questions:
            if q.axis is None:
                q.axis = proper_axis
            elif q.axis != proper_axis:
                # print(f"inconsistent axes, cannot compare")
                # print(f"{q.axis = }")
                # print(f"{proper_axis = }")
                return CHECK_INCONSISTENT_AXES


    return 0 

def check_pair_of_questions(question1s, question2s):
    """handling potential issues with questions"""
    
    # ensure that the question actually were found in all surveys
    for q in question1s + question2s:
        if isinstance(q, int):
            # .search returns 0 if question not found
            return CHECK_QUESTION_NOT_FOUND
        
    status_1 = check_set_question_and_axes(question1s)
    status_2 = check_set_question_and_axes(question2s)

    # perform final axis check after possible axis correction
    # all axes must be the same
    one_of_the_axes = question1s[0].axis
    for q in question1s + question2s:
        if q.axis != one_of_the_axes:
            return CHECK_INCONSISTENT_AXES

    if status_1 != CHECK_SUCCES or status_2 != CHECK_SUCCES:
        return -1

    return CHECK_SUCCES



