#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
File: dataframe_gymnastics.py
Author: Noah Nielsen
Created: 2026-07-06
Description: This module provides the functions for loading, merging and filtering of the BaseGeo
data, using pandas dataframe
"""

import pandas as pd
# we need to describe the instiution with an index
map_institution = {
    "UiB": 0,
    "UiB Geophysics": 1,
    "UiO": 2,
    "UiT": 3,
    "UNIS": 4,
    "UiB: Geophysical Institute": 1,
    "UiB Geovitenskap": 0,
    "UiB Geofysikk": 1,
    "uib": 0,
    "uibgeophys": 1,
    "uio": 2,
    "uit": 3,
    "unis": 4
}

# for better compatibility with pymc, we describe the years with 0 and 1
year_2019 = 0
year_2026 = 1

def load_2019_data_students():
    df_uib_2019_students_path = "..\\2019data\\uib_2019_students.xlsx"
    df_uibgeophys_2019_students_path = "..\\2019data\\uibgeophys_2019_students.xlsx"
    df_uio_2019_students_path = "..\\2019data\\uio_2019_students.xlsx"
    df_uit_2019_students_path = "..\\2019data\\uit_2019_students.xlsx"
    df_unis_2019_students_path = "..\\2019data\\unis_2019_students.xlsx"
    df_uib_2019_students_raw = pd.read_excel(df_uib_2019_students_path)
    df_uibgeophys_2019_students_raw = pd.read_excel(df_uibgeophys_2019_students_path)
    df_uio_2019_students_raw = pd.read_excel(df_uio_2019_students_path)
    df_uit_2019_students_raw = pd.read_excel(df_uit_2019_students_path)
    df_unis_2019_students_raw = pd.read_excel(df_unis_2019_students_path)

    # remove whirtespace from the column names
    df_uib_2019_students_raw.columns = df_uib_2019_students_raw.columns.str.strip()
    df_uibgeophys_2019_students_raw.columns = df_uibgeophys_2019_students_raw.columns.str.strip()
    df_uio_2019_students_raw.columns = df_uio_2019_students_raw.columns.str.strip()
    df_uit_2019_students_raw.columns = df_uit_2019_students_raw.columns.str.strip()
    df_unis_2019_students_raw.columns = df_unis_2019_students_raw.columns.str.strip()

    # merge dataframes, only keeping the questions that are available in all dataframes
    df_2019_students = pd.concat([
        df_uib_2019_students_raw, 
        df_uibgeophys_2019_students_raw, 
        df_uio_2019_students_raw, 
        df_uit_2019_students_raw, 
        df_unis_2019_students_raw
        ], ignore_index=True,
        join="inner") 

    # add a column with the year
    df_2019_students["year"] = year_2019

    # add a column with the institution index
    def convert_text_university_to_numeric_2019_students(df):
        df["institution"] = df["Which of these educational institutions are you studying at?"].replace(
            map_institution
        )
        return df

    df_2019_students = convert_text_university_to_numeric_2019_students(df_2019_students)

    return df_2019_students#, common_questions_students_2019

def load_2019_data_educators():
    # load data
    df_uib_2019_educators_path = "..\\2019data\\uib_2019_educators.xlsx"
    df_uibgeophys_2019_educators_path = "..\\2019data\\uibgeophys_2019_educators.xlsx"
    df_uio_2019_educators_path = "..\\2019data\\uio_2019_educators.xlsx"
    df_uit_2019_educators_path = "..\\2019data\\uit_2019_educators.xlsx"
    df_unis_2019_educators_path = "..\\2019data\\unis_2019_educators.xlsx"
    df_uib_2019_educators_raw = pd.read_excel(df_uib_2019_educators_path)
    df_uibgeophys_2019_educators_raw = pd.read_excel(df_uibgeophys_2019_educators_path)
    df_uio_2019_educators_raw = pd.read_excel(df_uio_2019_educators_path)
    df_uit_2019_educators_raw = pd.read_excel(df_uit_2019_educators_path)
    df_unis_2019_educators_raw = pd.read_excel(df_unis_2019_educators_path)

    # remove whitespace from the column names
    df_uib_2019_educators_raw.columns = df_uib_2019_educators_raw.columns.str.strip()
    df_uibgeophys_2019_educators_raw.columns = df_uibgeophys_2019_educators_raw.columns.str.strip()
    df_uio_2019_educators_raw.columns = df_uio_2019_educators_raw.columns.str.strip()
    df_uit_2019_educators_raw.columns = df_uit_2019_educators_raw.columns.str.strip()
    df_unis_2019_educators_raw.columns = df_unis_2019_educators_raw.columns.str.strip()

    # define special cases for the 2019 educators data
    special_cases = {
        "My own role/ experiences as a teacher":
            "My own role / experiences as a teacher",
        "To what extent is there coherence (connectedness) between the courses in the study programme?": 
            "To what extent do you think there is coherence (connectedness) between the courses in the study programme?",
        "To what extent does the education prepare students for future work in geoscience?":
            "To what extent do you think the education at your institution prepare students for their future work in geoscience?",
        "To what extent does the education at your institution prepare students for their future work in geoscience?":
            "To what extent do you think the education at your institution prepare students for their future work in geoscience?",
        "Informal feedback from students":
            "Informal feed-back from students",
        "That a colleague is present while you teach and afterwards gives you feedback (peer review)":
            "That a colleague is present while you teach and afterwards gives you feedback (peer feedback)",
    }

    # rename columns in the dataframes based on the special cases
    df_uib_2019_educators_raw.rename(columns=special_cases, inplace=True)
    df_uibgeophys_2019_educators_raw.rename(columns=special_cases, inplace=True)
    df_uio_2019_educators_raw.rename(columns=special_cases, inplace=True)
    df_uit_2019_educators_raw.rename(columns=special_cases, inplace=True)
    df_unis_2019_educators_raw.rename(columns=special_cases, inplace=True)

    # merge dataframes, only keeping the questions that are available in all dataframes
    df_2019_educators = pd.concat([
        df_uib_2019_educators_raw, 
        df_uibgeophys_2019_educators_raw, 
        df_uio_2019_educators_raw, 
        df_uit_2019_educators_raw, 
        df_unis_2019_educators_raw
        ], ignore_index=True,
        join="inner") # <- replaces the many lines of code above


    # add a column with the year
    df_2019_educators["year"] = year_2019

    # add a column with the institution index
    def convert_text_university_to_numeric_2019_educators(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2019_educators = convert_text_university_to_numeric_2019_educators(df_2019_educators)
    return df_2019_educators#, common_questions_educators_2019

def load_2019_data_admintech():
    # load data
    df_uib_2019_noneducators_path = "..\\2019data\\uib_2019_non_teaching_researcher.xlsx"
    df_uibgeophys_noneducators_path = "..\\2019data\\uibgeophys_2019_non_teaching_researcher.xlsx"
    df_uio_2019_noneducators_path = "..\\2019data\\uio_2019_non_teaching_researcher.xlsx"
    df_uit_2019_noneducators_path = "..\\2019data\\uit_2019_non_teaching_researcher.xlsx"
    df_unis_2019_noneducators_path = "..\\2019data\\unis_2019_non_teaching_researcher.xlsx"
    df_uib_2019_admintech_path = "..\\2019data\\uib_2019_admintech.xlsx"
    df_uibgeophys_2019_admintech_path = "..\\2019data\\uibgeophys_2019_admintech.xlsx" 
    df_uio_2019_admintech_path = "..\\2019data\\uio_2019_admintech.xlsx"
    df_uit_2019_admintech_path = "..\\2019data\\uit_2019_admintech.xlsx"
    df_unis_2019_admintech_path = "..\\2019data\\unis_2019_admintech.xlsx"
    df_uib_2019_noneducators_raw = pd.read_excel(df_uib_2019_noneducators_path)
    df_uibgeophys_noneducators_raw = pd.read_excel(df_uibgeophys_noneducators_path)
    df_uio_2019_noneducators_raw = pd.read_excel(df_uio_2019_noneducators_path)
    df_uit_2019_noneducators_raw = pd.read_excel(df_uit_2019_noneducators_path)
    # df_unis_2019_noneducators_raw = pd.read_excel(df_unis_2019_noneducators_path) # <- does not exist
    df_uib_2019_admintech_raw = pd.read_excel(df_uib_2019_admintech_path)
    df_uibgeophys_2019_admintech_raw = pd.read_excel(df_uibgeophys_2019_admintech_path)
    df_uio_2019_admintech_raw = pd.read_excel(df_uio_2019_admintech_path)
    df_uit_2019_admintech_raw = pd.read_excel(df_uit_2019_admintech_path)
    df_unis_2019_admintech_raw = pd.read_excel(df_unis_2019_admintech_path)

    # remove whitespace from the column names
    df_uib_2019_noneducators_raw.columns = df_uib_2019_noneducators_raw.columns.str.strip()
    df_uibgeophys_noneducators_raw.columns = df_uibgeophys_noneducators_raw.columns.str.strip()
    df_uio_2019_noneducators_raw.columns = df_uio_2019_noneducators_raw.columns.str.strip()
    df_uit_2019_noneducators_raw.columns = df_uit_2019_noneducators_raw.columns.str.strip()
    # df_unis_2019_noneducators_raw.columns = df_unis_2019_noneducators_raw.columns.str.strip()
    df_uib_2019_admintech_raw.columns = df_uib_2019_admintech_raw.columns.str.strip()
    df_uibgeophys_2019_admintech_raw.columns = df_uibgeophys_2019_admintech_raw.columns.str.strip()
    df_uio_2019_admintech_raw.columns = df_uio_2019_admintech_raw.columns.str.strip()
    df_uit_2019_admintech_raw.columns = df_uit_2019_admintech_raw.columns.str.strip()
    df_unis_2019_admintech_raw.columns = df_unis_2019_admintech_raw.columns.str.strip()
    
    # merge dataframes, only keeping the questions that are available in all dataframes
    df_2019_admintech = pd.concat([
        df_uib_2019_noneducators_raw,
        df_uibgeophys_noneducators_raw,
        df_uio_2019_noneducators_raw,
        df_uit_2019_noneducators_raw,
        # df_unis_2019_noneducators_raw, # <- does not exist
        df_uib_2019_admintech_raw, 
        df_uibgeophys_2019_admintech_raw, 
        df_uio_2019_admintech_raw, 
        df_uit_2019_admintech_raw, 
        df_unis_2019_admintech_raw
        ], ignore_index=True,
        join="inner") # <- replaces the many lines of code above


    # add a column with the year
    df_2019_admintech["year"] = year_2019

    # add a column with the institution index
    def convert_text_university_to_numeric_2019_admintech(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2019_admintech = convert_text_university_to_numeric_2019_admintech(df_2019_admintech)
    return df_2019_admintech#, common_questions_2019_admintech


def load_2026_data_students():
    # load data
    df_2026_students_path = "..\\2026data\\data_2026_students.xlsx"
    df_2026_students_raw = pd.read_excel(df_2026_students_path)

    # remove whitespace from the column names
    df_2026_students_raw.columns = df_2026_students_raw.columns.str.strip()

    # avoid filtering now, just copy the dataframe
    df_2026_students = df_2026_students_raw.copy()

    # add the column with the university names and the year
    df_2026_students["Where are you studying?"] = df_2026_students_raw["Where are you studying?"]
    df_2026_students["year"] = year_2026

    # add a column with the institution index
    def convert_text_university_to_numeric_2026(df):
        df["institution"] = df["Where are you studying?"].replace(
            map_institution
        )
        return df

    df_2026_students = convert_text_university_to_numeric_2026(df_2026_students)
    return df_2026_students

def load_2026_data_educators():
    # load data
    df_2026_educators_path = "..\\2026data\\data_2026_educators.xlsx"
    df_2026_educators_raw = pd.read_excel(df_2026_educators_path)

    # remove whitespace from the column names
    df_2026_educators_raw.columns = df_2026_educators_raw.columns.str.strip()

    # avoid filtering now, just copy the dataframe
    df_2026_educators = df_2026_educators_raw.copy()

    # add the column with the university names and the year
    df_2026_educators["Where are you employed?"] = df_2026_educators_raw["Where are you employed?"]
    df_2026_educators["year"] = year_2026

    # add a column with the institution index
    def convert_text_university_to_numeric_2026(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2026_educators = convert_text_university_to_numeric_2026(df_2026_educators)
    return df_2026_educators

def load_2026_data_admintech():
    # load data
    df_2026_admintech_path = "..\\2026data\\data_2026_admintech.xlsx"
    df_2026_admintech_raw = pd.read_excel(df_2026_admintech_path)

    # remove whitespace from the column names
    df_2026_admintech_raw.columns = df_2026_admintech_raw.columns.str.strip()

    # avoid filtering now, just copy the dataframe
    df_2026_admintech = df_2026_admintech_raw.copy()

    # add the column with the university names and the year
    df_2026_admintech["Where are you employed?"] = df_2026_admintech_raw["Where are you employed?"]
    df_2026_admintech["year"] = year_2026

    # add a column with the institution index
    def convert_text_university_to_numeric_2026(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2026_admintech = convert_text_university_to_numeric_2026(df_2026_admintech)
    return df_2026_admintech


def merge_2019_with_2026(
    df_2019_students, 
    df_2019_educators, 
    df_2019_admintech, 
    df_2026_students, 
    df_2026_educators, 
    df_2026_admintech,
    special_cases_good_questions
):
    """ 
    Merge dataframes
    students with students
    educators with educators
    admintech with admintech

    first handles special cases, where we can analyze som questions, but the questions are not ordered properly
    The scheme for this is defined in the notebook 

    Afterwards is merges with the pandad concatenate function, merging only the intersection of the columns

    Generally not a pretty function, with code written explicitly. Could be rewritten if time permits
    """
    
    # before any merging, we must ensure that the cases with incorrect numbering are taken care of
    # this could have been done smarter, but is it currently done explicitly

    # the special cases handling are NOT done as renaming, since we want delete the wrong data
    # students
    special_cases_students = special_cases_good_questions["students"]
    print(f"handling special cases {special_cases_students.keys()}")
    for key, value in special_cases_students.items():
        # overwrite column "value" and fill it with the responses from the "key" column
        print(f"column {value} now contain resposes previously known as {key} in 2019 students dataframe")

        # drop the column with the right name but wrong data first
        df_2019_students.drop(columns=[value], inplace=True)  
        
        # create a new column with the correct name and fill it with the responses from the wrong column
        df_2019_students[value] = df_2019_students[key]
        
        # drop the column with the wrong name but right data
        df_2019_students.drop(columns=[key], inplace=True)

    # educators
    special_cases_educators = special_cases_good_questions["educators"]
    print(f"handling special cases {special_cases_educators.keys()}")
    for key, value in special_cases_educators.items():
        # overwrite column "value" and fill it with the responses from the "key" column
        print(f"column {value} now contain resposes previously known as {key} in 2019 educators dataframe")
        
        # drop the column with the right name but wrong data first
        df_2019_educators.drop(columns=[value], inplace=True)
        
        # create a new column with the correct name and fill it with the responses from the wrong column
        df_2019_educators[value] = df_2019_educators[key]
        
        # drop the column with the wrong name but right data
        df_2019_educators.drop(columns=[key], inplace=True)

    # admintech
    special_cases_admintech = special_cases_good_questions["admintech"]
    print(f"handling special cases {special_cases_admintech.keys()}")
    for key, value in special_cases_admintech.items():
        # overwrite column "value" and fill it with the responses from the "key" column
        print(f"column {value} now contain resposes previously known as {key} in 2019 admintech dataframe")
        
        # drop the column with the right name but wrong data first
        df_2019_admintech.drop(columns=[value], inplace=True)
        
        # create a new column with the correct name and fill it with the responses from the wrong column
        df_2019_admintech[value] = df_2019_admintech[key]
        
        # drop the column with the wrong name but right data
        df_2019_admintech.drop(columns=[key], inplace=True) 


    # merging
    df_students = pd.concat([df_2019_students, df_2026_students], ignore_index=True, join="inner")
    df_educators = pd.concat([df_2019_educators, df_2026_educators], ignore_index=True, join="inner")
    df_admintech = pd.concat([df_2019_admintech, df_2026_admintech], ignore_index=True, join="inner")

    return (
        df_students, 
        df_educators, 
        df_admintech,
    ) 


# Loose loading. Allows for loading of questions that are different across surveys. 
# Used for plotting raw data
def load_loose_educators_data_2019():
    """Load all the data from 2019 survey. Use special cases to allow
    merging of questions that are not exactly the same in all surveys.
    """

    df_uib_2019_educators_path = "..\\2019data\\uib_2019_educators.xlsx"
    df_uibgeophys_2019_educators_path = "..\\2019data\\uibgeophys_2019_educators.xlsx"
    df_uio_2019_educators_path = "..\\2019data\\uio_2019_educators.xlsx"
    df_uit_2019_educators_path = "..\\2019data\\uit_2019_educators.xlsx"
    df_unis_2019_educators_path = "..\\2019data\\unis_2019_educators.xlsx"
    df_uib_2019_educators_raw = pd.read_excel(df_uib_2019_educators_path)
    df_uibgeophys_2019_educators_raw = pd.read_excel(df_uibgeophys_2019_educators_path)
    df_uio_2019_educators_raw = pd.read_excel(df_uio_2019_educators_path)
    df_uit_2019_educators_raw = pd.read_excel(df_uit_2019_educators_path)
    df_unis_2019_educators_raw = pd.read_excel(df_unis_2019_educators_path)

    # remove whitespace from the column names
    df_uib_2019_educators_raw.columns = df_uib_2019_educators_raw.columns.str.strip()
    df_uibgeophys_2019_educators_raw.columns = df_uibgeophys_2019_educators_raw.columns.str.strip()
    df_uio_2019_educators_raw.columns = df_uio_2019_educators_raw.columns.str.strip()
    df_uit_2019_educators_raw.columns = df_uit_2019_educators_raw.columns.str.strip()
    df_unis_2019_educators_raw.columns = df_unis_2019_educators_raw.columns.str.strip()

    # define special cases for the 2019 educators data
    special_cases = {
        "To what extent do you think there is coherence (connectedness) between the courses in the study programme?":
            "To what extent is there coherence (connectedness) between the courses in the study programme?",
        "To what extent does the education at your institution prepare students for their future work in geoscience?":
            "To what extent does the education prepare students for future work in geoscience?",
        "My own role/ experiences as a teacher":
            "My own role / experiences as a teacher",
        "I am able to achieve the goals I set myself as a teacher":
            "I am able to achieve the goals I set for myself",
        "Informal feed-back from students":
            "Informal feedback from students",
        "It is my impression that most students feel comfortable in the department":
            "It is my impression that most students feel comfortable as students at the department",
        "It is my impression that the students have good possibilities for social contact with other students":
            "It is my impression that the students have good possibilities for social contact with their fellow students",
        "Private and/or public employers are involved in teaching (e.g. lecturing, evaluations, visits) at the institution":
            "Private and/or public employers are involved in teaching (e.g. lecturing, evaluations, visits, other initiatives) at the institution",
    }

    # rename columns in the dataframes based on the special cases
    df_uib_2019_educators_raw.rename(columns=special_cases, inplace=True)
    df_uibgeophys_2019_educators_raw.rename(columns=special_cases, inplace=True)
    df_uio_2019_educators_raw.rename(columns=special_cases, inplace=True)
    df_uit_2019_educators_raw.rename(columns=special_cases, inplace=True)
    df_unis_2019_educators_raw.rename(columns=special_cases, inplace=True)

    # merge dataframes, only keeping the questions that are available in all dataframes
    # however, now the questions are renamed beforehand to match
    df_2019_educators_population = pd.concat([
        df_uib_2019_educators_raw, 
        df_uibgeophys_2019_educators_raw, 
        df_uio_2019_educators_raw, 
        df_uit_2019_educators_raw, 
        df_unis_2019_educators_raw
        ], ignore_index=True,
        join="inner")

   
    # add a column with the institution index
    def convert_text_university_to_numeric_2019_educators(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2019_educators_population = convert_text_university_to_numeric_2019_educators(df_2019_educators_population)

    # only save "population", which is all the data. We filter it later
    dataframe_dict = {
        "population": df_2019_educators_population,
    }
    return dataframe_dict

def load_loose_students_data_2019():
    """Load all the data from 2019 survey. Use special cases to allow
    merging of questions that are not exactly the same in all surveys."""
    df_uib_2019_students_path = "..\\2019data\\uib_2019_students.xlsx"
    df_uibgeophys_2019_students_path = "..\\2019data\\uibgeophys_2019_students.xlsx"
    df_uio_2019_students_path = "..\\2019data\\uio_2019_students.xlsx"
    df_uit_2019_students_path = "..\\2019data\\uit_2019_students.xlsx"
    df_unis_2019_students_path = "..\\2019data\\unis_2019_students.xlsx"
    df_uib_2019_students_raw = pd.read_excel(df_uib_2019_students_path)
    df_uibgeophys_2019_students_raw = pd.read_excel(df_uibgeophys_2019_students_path)
    df_uio_2019_students_raw = pd.read_excel(df_uio_2019_students_path)
    df_uit_2019_students_raw = pd.read_excel(df_uit_2019_students_path)
    df_unis_2019_students_raw = pd.read_excel(df_unis_2019_students_path)

    # remove whitespace from the column names
    df_uib_2019_students_raw.columns = df_uib_2019_students_raw.columns.str.strip()
    df_uibgeophys_2019_students_raw.columns = df_uibgeophys_2019_students_raw.columns.str.strip()
    df_uio_2019_students_raw.columns = df_uio_2019_students_raw.columns.str.strip()
    df_uit_2019_students_raw.columns = df_uit_2019_students_raw.columns.str.strip()
    df_unis_2019_students_raw.columns = df_unis_2019_students_raw.columns.str.strip()


    # define special cases for the 2019 students data
    special_cases = {
        "To what extent does the education prepare you for future work in geoscience?":
            "To what extent does the education at your institution prepare you for your future work in geoscience?",
        "To what extent is here connection between the courses in the study programme?":
            "To what extent do you think there is connectedness between the courses in the study programme?",
    }

    # rename columns in the dataframes based on the special cases
    df_uib_2019_students_raw.rename(columns=special_cases, inplace=True)
    df_uibgeophys_2019_students_raw.rename(columns=special_cases, inplace=True)
    df_uio_2019_students_raw.rename(columns=special_cases, inplace=True)
    df_uit_2019_students_raw.rename(columns=special_cases, inplace=True)
    df_unis_2019_students_raw.rename(columns=special_cases, inplace=True)

    # merge dataframes, only keeping the questions that are available in all dataframes
    # however, now the questions are renamed beforehand to match
    df_2019_students_population = pd.concat([
        df_uib_2019_students_raw,
        df_uibgeophys_2019_students_raw,
        df_uio_2019_students_raw,
        df_uit_2019_students_raw,
        df_unis_2019_students_raw
    ], ignore_index=True,
        join="inner") # <- replaces the many lines of code above

    
    # add a column with the institution index
    def convert_text_university_to_numeric_2019_students(df):
        df["institution"] = df["Which of these educational institutions are you studying at?"].replace(
            map_institution
        )
        return df


    df_2019_students_population = convert_text_university_to_numeric_2019_students(df_2019_students_population)


    dataframe_dict = {
        "population": df_2019_students_population,
    }
    return dataframe_dict

def load_loose_admintech_data_2019():
    # load data
    df_uib_2019_noneducators_path = "..\\2019data\\uib_2019_non_teaching_researcher.xlsx"
    df_uibgeophys_noneducators_path = "..\\2019data\\uibgeophys_2019_non_teaching_researcher.xlsx"
    df_uio_2019_noneducators_path = "..\\2019data\\uio_2019_non_teaching_researcher.xlsx"
    df_uit_2019_noneducators_path = "..\\2019data\\uit_2019_non_teaching_researcher.xlsx"
    df_unis_2019_noneducators_path = "..\\2019data\\unis_2019_non_teaching_researcher.xlsx"
    df_uib_2019_admintech_path = "..\\2019data\\uib_2019_admintech.xlsx"
    df_uibgeophys_2019_admintech_path = "..\\2019data\\uibgeophys_2019_admintech.xlsx" 
    df_uio_2019_admintech_path = "..\\2019data\\uio_2019_admintech.xlsx"
    df_uit_2019_admintech_path = "..\\2019data\\uit_2019_admintech.xlsx"
    df_unis_2019_admintech_path = "..\\2019data\\unis_2019_admintech.xlsx"
    df_uib_2019_noneducators_raw = pd.read_excel(df_uib_2019_noneducators_path)
    df_uibgeophys_2019_noneducators_raw = pd.read_excel(df_uibgeophys_noneducators_path)
    df_uio_2019_noneducators_raw = pd.read_excel(df_uio_2019_noneducators_path)
    df_uit_2019_noneducators_raw = pd.read_excel(df_uit_2019_noneducators_path)
    # df_unis_2019_noneducators_raw = pd.read_excel(df_unis_2019_noneducators_path) # <- does not exist
    df_uib_2019_admintech_raw = pd.read_excel(df_uib_2019_admintech_path)
    df_uibgeophys_2019_admintech_raw = pd.read_excel(df_uibgeophys_2019_admintech_path)
    df_uio_2019_admintech_raw = pd.read_excel(df_uio_2019_admintech_path)
    df_uit_2019_admintech_raw = pd.read_excel(df_uit_2019_admintech_path)
    df_unis_2019_admintech_raw = pd.read_excel(df_unis_2019_admintech_path)

    # remove whitespace from the column names
    df_uib_2019_noneducators_raw.columns = df_uib_2019_noneducators_raw.columns.str.strip()
    df_uibgeophys_2019_noneducators_raw.columns = df_uibgeophys_2019_noneducators_raw.columns.str.strip()
    df_uio_2019_noneducators_raw.columns = df_uio_2019_noneducators_raw.columns.str.strip()
    df_uit_2019_noneducators_raw.columns = df_uit_2019_noneducators_raw.columns.str.strip()
    # df_unis_2019_noneducators_raw.columns = df_unis_2019_noneducators_raw.columns.str.strip()
    df_uib_2019_admintech_raw.columns = df_uib_2019_admintech_raw.columns.str.strip()
    df_uibgeophys_2019_admintech_raw.columns = df_uibgeophys_2019_admintech_raw.columns.str.strip()
    df_uio_2019_admintech_raw.columns = df_uio_2019_admintech_raw.columns.str.strip()
    df_uit_2019_admintech_raw.columns = df_uit_2019_admintech_raw.columns.str.strip()
    df_unis_2019_admintech_raw.columns = df_unis_2019_admintech_raw.columns.str.strip()
    
    # define special cases for the 2019 admintecg data
    special_cases = {
        "To what extent does the education prepare students for future work in geoscience?":
            "To what extent does the education at your institution prepare students for their future work in geoscience?",        
        "To what extent is there coherence (connectedness) between the courses in the study programme?":
            "To what extent do you think there is coherence (connectedness) between the courses in the study programme?",
    }


    # rename columns in the dataframes based on the special cases
    df_uib_2019_noneducators_raw.rename(columns=special_cases, inplace=True)
    df_uibgeophys_2019_noneducators_raw.rename(columns=special_cases, inplace=True)
    df_uio_2019_noneducators_raw.rename(columns=special_cases, inplace=True)
    df_uit_2019_noneducators_raw.rename(columns=special_cases, inplace=True)
    # df_unis_2019_noneducators_raw.rename(columns=special_cases, inplace=True) # <- does not exist
    df_uib_2019_admintech_raw.rename(columns=special_cases, inplace=True)
    df_uibgeophys_2019_admintech_raw.rename(columns=special_cases, inplace=True)
    df_uio_2019_admintech_raw.rename(columns=special_cases, inplace=True)
    df_uit_2019_admintech_raw.rename(columns=special_cases, inplace=True)
    df_unis_2019_admintech_raw.rename(columns=special_cases, inplace=True)

    # merge dataframes, only keeping the questions that are available in all dataframes
    # however, now the questions are renamed beforehand to match
    df_2019_admintech = pd.concat([
        df_uib_2019_noneducators_raw,
        df_uibgeophys_2019_noneducators_raw,
        df_uio_2019_noneducators_raw,
        df_uit_2019_noneducators_raw,
        # df_unis_2019_noneducators_raw, # <- does not exist
        df_uib_2019_admintech_raw, 
        df_uibgeophys_2019_admintech_raw, 
        df_uio_2019_admintech_raw, 
        df_uit_2019_admintech_raw, 
        df_unis_2019_admintech_raw
        ], ignore_index=True,
        join="inner") # <- replaces the many lines of code above

    # add a column with the year
    df_2019_admintech["year"] = year_2019

    # add a column with the institution index
    def convert_text_university_to_numeric_2019_admintech(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df
    
    df_2019_admintech = convert_text_university_to_numeric_2019_admintech(df_2019_admintech)


    dataframe_dict = {
        "population": df_2019_admintech,
    }
    return dataframe_dict




def load_loose_educators_data_2026():
    # load data
    df_2026_educators_path = "..\\2026data\\data_2026_educators.xlsx"
    df_2026_educators_raw = pd.read_excel(df_2026_educators_path)

    # remove whitespace from the column names
    df_2026_educators_raw.columns = df_2026_educators_raw.columns.str.strip()

    # just copy the raw
    df_2026_educators = df_2026_educators_raw.copy()

    # add the column with the university names and the year
    df_2026_educators["Where are you employed?"] = df_2026_educators_raw["Where are you employed?"]
    df_2026_educators["year"] = year_2026

    # add a column with the institution index
    def convert_text_university_to_numeric_2026(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2026_educators = convert_text_university_to_numeric_2026(df_2026_educators)
    return df_2026_educators

def load_loose_students_data_2026():
    # load data
    df_2026_students_path = "..\\2026data\\data_2026_students.xlsx"
    df_2026_students_raw = pd.read_excel(df_2026_students_path)

    # remove whitespace from the column names
    df_2026_students_raw.columns = df_2026_students_raw.columns.str.strip()

    # just copy the raw
    df_2026_students = df_2026_students_raw.copy()

    # add the column with the university names and the year
    df_2026_students["Where are you studying?"] = df_2026_students_raw["Where are you studying?"]
    df_2026_students["year"] = year_2026

    # add a column with the institution index
    def convert_text_university_to_numeric_2026(df):
        df["institution"] = df["Where are you studying?"].replace(
            map_institution
        )
        return df

    df_2026_students = convert_text_university_to_numeric_2026(df_2026_students)
    return df_2026_students

def load_loose_admintech_data_2026():
    # load data
    df_2026_admintech_path = "..\\2026data\\data_2026_admintech.xlsx"
    df_2026_admintech_raw = pd.read_excel(df_2026_admintech_path)

    # remove whitespace from the column names
    df_2026_admintech_raw.columns = df_2026_admintech_raw.columns.str.strip()

    # just copy the raw
    df_2026_admintech = df_2026_admintech_raw.copy()

    # add the column with the university names and the year
    df_2026_admintech["Where are you employed?"] = df_2026_admintech_raw["Where are you employed?"]
    df_2026_admintech["year"] = year_2026

    # add a column with the institution index
    def convert_text_university_to_numeric_2026(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2026_admintech = convert_text_university_to_numeric_2026(df_2026_admintech)
    return df_2026_admintech