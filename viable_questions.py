


from actors import Survey

def find_viable_questions(survey1, survey2):
    """go thorugh two surveys and return a list of questions that are viable
    
    criteria for viability:
     - the questions must be the same
     - the axes must be well-defined
     - the axes must be the same
    
    """

    viable_questions = []
    for question1 in survey1.questions:
        for question2 in survey2.questions:

            if question1.raw_text != question2.raw_text:
                continue
            if question1.axis is None:
                continue
            if question2.axis is None:
                continue
            if question1.axis != question2.axis:
                continue
            
            viable_questions.append(question1.raw_text)

    return viable_questions

def write_viable_questions():
    survey_educator_2019_path = r"2019data\data_2019_educators_reduced_questions.xlsx"
    survey_educator_2026_path = r"2026data\data_2026_educators.xlsx"
    survey_admintech_2019_path = r"2019data\data_2019_admintech_reduced_questions.xlsx"
    survey_admintech_2026_path = r"2026data\data_2026_admintech.xlsx"
    survey_student_2019_path = r"2019data\data_2019_students_reduced_questions.xlsx"
    survey_student_2026_path = r"2026data\data_2026_students.xlsx"
    

    survey_educator_2019_path = r"2019data\uit_2019_educators.xlsx"
    survey_educator_2026_path = r"2026data\uit_2026_educators.xlsx"
    survey_admintech_2019_path = r"2019data\uit_2019_admintech.xlsx"
    survey_admintech_2026_path = r"2026data\uit_2026_admintech.xlsx"
    survey_student_2019_path = r"2019data\uit_2019_students.xlsx"
    survey_student_2026_path = r"2026data\uit_2026_students.xlsx"
    survey_educator_2019 = Survey(survey_educator_2019_path)
    survey_educator_2026 = Survey(survey_educator_2026_path)
    survey_admintech_2019 = Survey(survey_admintech_2019_path)
    survey_admintech_2026 = Survey(survey_admintech_2026_path)
    survey_student_2019 = Survey(survey_student_2019_path)
    survey_student_2026 = Survey(survey_student_2026_path)

    viable_questions_educator = find_viable_questions(survey1=survey_educator_2019,
                                             survey2=survey_educator_2026,)
    viable_questions_admintech = find_viable_questions(survey1=survey_admintech_2019,
                                             survey2=survey_admintech_2026,)
    viable_questions_student = find_viable_questions(survey1=survey_student_2019,
                                             survey2=survey_student_2026,)
    


    with open(r"viable_questions\viable_questions.txt", mode="w") as doc:

        doc.write("\subsection{Viable questions educator}\n")
        for viable_question in viable_questions_educator: doc.write(f"\\\\ {viable_question}\n")
        doc.write("\clearpage\n\n\subsection{Viable questions admintech}\n")
        for viable_question in viable_questions_admintech: doc.write(f"\\\\ {viable_question}\n")
        doc.write("\clearpage\n\n\subsection{Viable questions student}\n")
        for viable_question in viable_questions_student: doc.write(f"\\\\ {viable_question}\n")

    return 


