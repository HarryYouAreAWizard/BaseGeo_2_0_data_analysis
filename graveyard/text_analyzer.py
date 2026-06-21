


import os

global data_folder, figure_folder
data_folder = "BaseGeo_2_0\\all data exel"
question_folder = "BaseGeo_2_0\\questions pdf"
figure_folder = "BaseGeo_2_0\\figures"

def print_questions():
    list_of_questions = os.listdir(question_folder)
    for question_file in list_of_questions:
        path = question_folder + "\\" + question_file
        doc = open(path)
        for line in doc:
            print(line)