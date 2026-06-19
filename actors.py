#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: actors.py
Author: Noah Nielsen
Created: 2026-06-14
Description: This module defines the core classes for representing survey data, 
including Participant, Question, and Survey. These classes encapsulate the 
structure and behavior of survey data, allowing for organized access to participant 
responses, question details, and overall survey management. The Participant class 
represents individual respondents, the Question class handles the specifics of each 
survey question, and the Survey class manages the collection of questions and participants.
"""

import pandas as pd
import numpy as np
from axes_handling.axes import UNIVERSAL_OPTIONS, detect_axis, normalize_answer
from axes_handling.axes_special_cases import predefined_axes

class Participant:
    """not really used. Most of the information
    if encapsulated in Survey and Question classes
    
    Could be used for conditional analysis, eg only count results if participant 
    responded "x" to question "A".
    """
    def __init__(self, id, survey, answers):
        self.id = id
        self.survey = survey
        self.answers = answers

    def respond(self, question):
        return self.answers[question.raw_text].iloc[0]


class Question:
    """Represents a question in survey and contain all relevant data"""
    def __init__(self, key, responses):
        """is called from survey class."""
        self.raw_text = key
        self.responses = responses
        self.axis = detect_axis(responses)
        self.number_axis = range(1, 8)  # default to 7 point scale, can be adjusted if needed
        self.counts = self.get_counts()
        # self.counts = None
        self.total_counts = len(responses)

        # avoid these calculations if they are not needed
        self.sample_mean = None
        self.sample_variance = None
        self.sample_std = None


        # if self.axis is not None and self.axis[0] not in {"unknown", "ambiguous"}:
        #     self.sample_mean, self.sample_variance = self.sample_mean_and_variance()
        # else:
        #     self.sample_mean, self.sample_variance = None, None

        # self.sample_std = self.sample_variance ** 0.5 if self.sample_variance is not None else None

    def get_counts(self):
        """get the counts of each response category as a pandas Series, 
        using the axis labels as index. If the axis is not detected, 
        return the counts of unique normalized responses.
        
        We must ensure that we count everyting, that is, if there is a typo 
        in the original axis label for "1." then we still count the number of
        "1."s in the answers 
        """
        
        if self.axis is None:
            if self.raw_text[:len("Fieldwork skills.1")] == "Fieldwork skills.1":
                print(f"HERE")
                print(f"{self.responses = }")
            return    
    
        try:
            x = [response[:1] for response in self.responses if normalize_answer(response) is not None]   # pick out the first character of the response, which should be the number if it starts with a digit
        except TypeError as e:
            # if self.raw_text[:len("Fieldwork")] == "Fieldwork":
            #     print("Error in response creation")
            print(f"\n{e = }\n")
            return
    
        # pick out numbers
        x = [int(v) for v in x if v and v[0].isdigit()]
        x  = pd.Series(x)
        counts = x.value_counts() # count occurrences of each unique value
        # reindex to ensure all axis labels are present, filling missing ones with 0
        counts = counts.reindex(self.number_axis, # the actual axis labels 
                           fill_value=0)                    
        self.counts = counts


        return counts

    def sample_mean_and_variance(self):
        """get the sample mean and variance of the questions. 
        Not really used"""
        counts = self.counts
        total_counts = self.total_counts
        values = [int(label[0]) for label in counts.index if label[0].isdigit()]
        mean = sum(value * count for value, count in zip(values, counts.values)) / total_counts
        variance = sum(count * (value - mean) ** 2 for value, count in zip(values, counts.values)) / total_counts
        self.sample_mean = mean
        self.sample_variance = variance
        self.sample_std = self.sample_variance**0.5
        return mean, variance


class Survey:

    def __init__(self, path):

        self.path = path
        self.data = pd.read_excel(path)

        self.ids = self.data["$submission_id"].tolist()
        self.questions = self.get_questions()
    
    def get_participants(self):
        """participants identified from their ID"""
        self.participants = []
        for id in self.ids:
            answers = self.data[self.data["$submission_id"] == id]
            participant = Participant(id, self, answers)
            self.participants.append(participant)
        return self.participants
    
    def get_questions(self):
        """initialize all questions in the dataset"""
        self.questions = []
        for key in self.data.keys():
            question = Question(key, self.data[key].tolist())
            
            # handle funky special cases
            affected_survey_paths = predefined_axes.keys()
            if self.path in affected_survey_paths:
                affected_questions = predefined_axes[self.path].keys()
                if question.raw_text in affected_questions:
                    print("success")
                    question.axis = predefined_axes[self.path][question.raw_text]
                    question.get_counts()

            self.questions.append(question)

        return self.questions
    
    def search(self, query):
        """Search for questions matching the query and return a list of matching questions."""
        # matching_questions = []
        for question in self.questions:#self.get_questions():
            if query.lower() in question.raw_text.lower():
                return question

