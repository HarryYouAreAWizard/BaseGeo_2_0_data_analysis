
import pandas as pd

from axes import UNIVERSAL_OPTIONS, detect_axis, normalize_answer

class Participant:
    def __init__(self, id, survey, answers):
        self.id = id
        self.survey = survey
        self.answers = answers

    def respond(self, question):
        return self.answers[question.raw_text].iloc[0]


class Question:
    def __init__(self, key, responses):
        self.raw_text = key
        self.responses = responses
        self.axis = detect_axis(responses)
        self.counts = self.get_counts()
        # self.counts = None
        self.total_counts = len(responses)


        if self.axis[0] not in {"unknown", "ambiguous"}:
            self.sample_mean, self.sample_variance = self.sample_mean_and_variance()
        else:
            self.sample_mean, self.sample_variance = None, None

        self.sample_std = self.sample_variance ** 0.5 if self.sample_variance is not None else None

    def detect_axis(self):
        """detect axis using the function from axes.py and store the found axis in self.axis"""
        self.axis = detect_axis(self.responses)

    def get_counts(self):
        """get the counts of each response category as a pandas Series, 
        using the axis labels as index. If the axis is not detected, 
        return the counts of unique normalized responses."""
        
        if self.axis is (None, None):
            return
        
        # # remove the responses that are in "UNIVERSAL_OPTIONS" from the counts, as they are not part of the actual axis
        # self.responses = [response for response in self.responses if response not in UNIVERSAL_OPTIONS]

        x = [normalize_answer(v) for v in self.responses]   # clean/normalize the responses
        x  = pd.Series(x)                                   #  convert to pd.Series
        x = x.value_counts()                                # count occurrences of each unique value
        # reindex to ensure all axis labels are present, filling missing ones with 0
        counts = x.reindex(self.axis[1],                    # the actual axis labels 
                           fill_value=0)                    
        self.counts = counts
        return counts

    def sample_mean_and_variance(self):
        counts = self.counts
        total_counts = self.total_counts
        values = [int(label[0]) for label in counts.index if label[0].isdigit()]
        mean = sum(value * count for value, count in zip(values, counts.values)) / total_counts
        variance = sum(count * (value - mean) ** 2 for value, count in zip(values, counts.values)) / total_counts
        return mean, variance


class Survey:

    def __init__(self, path):

        self.path = path
        self.data = pd.read_excel(path)
        self.ids = self.data["$submission_id"].tolist()
        self.questions = self.get_questions()
    
    def get_participants(self):
        self.participants = []
        for id in self.ids:
            answers = self.data[self.data["$submission_id"] == id]
            participant = Participant(id, self, answers)
            self.participants.append(participant)
        return self.participants
    
    def get_questions(self):
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
        # return matching_questions

