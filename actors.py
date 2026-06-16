
import pandas as pd
import numpy as np
from axes import UNIVERSAL_OPTIONS, detect_axis, normalize_answer

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

    def detect_axis(self):
        """detect axis using the function from axes.py and store the found axis in self.axis"""
        return detect_axis(self.responses)

    def get_counts(self):
        """get the counts of each response category as a pandas Series, 
        using the axis labels as index. If the axis is not detected, 
        return the counts of unique normalized responses.
        
        We must ensure that we count everyting, that is, if there is a typo 
        in the original axis label for "1." then we still count the number of
        "1."s in the answers 
        """
        
        if self.axis is None:
            return
        

        # avoid running if there are nan in the answers
        for response in self.responses:
            normalized = normalize_answer(response)
            if normalized is None:
                return 

        # count over the "dirty axis" inherent in the responses
        x = [normalize_answer(v)[:1] for v in self.responses]   # pick out the first character of the normalized response, which should be the number if it starts with a digit
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
            self.questions.append(question)

        return self.questions
    
    def search(self, query):
        """Search for questions matching the query and return a list of matching questions."""
        # matching_questions = []
        for question in self.get_questions():
            if query.lower() in question.raw_text.lower():
                return question

