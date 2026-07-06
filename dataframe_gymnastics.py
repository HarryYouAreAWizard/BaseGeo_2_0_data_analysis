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

    # merge dataframes with the questions available in all dataframes
    common_questions_students_2019 = list(
        set(df_uib_2019_students_raw.columns) 
        & set(df_uibgeophys_2019_students_raw.columns) 
        & set(df_uio_2019_students_raw.columns) 
        & set(df_uit_2019_students_raw.columns) 
        & set(df_unis_2019_students_raw.columns)
    )

    # pick out the common questions from each dataframe
    df_uib_2019_students_common_questions = df_uib_2019_students_raw[common_questions_students_2019].copy()
    df_uibgeophys_2019_students_common_questions = df_uibgeophys_2019_students_raw[common_questions_students_2019].copy()
    df_uio_2019_students_common_questions = df_uio_2019_students_raw[common_questions_students_2019].copy()
    df_uit_2019_students_common_questions = df_uit_2019_students_raw[common_questions_students_2019].copy()
    df_unis_2019_students_common_questions = df_unis_2019_students_raw[common_questions_students_2019].copy()

    # merge the dataframes containing only the common questions
    df_2019_students = pd.concat([
        df_uib_2019_students_common_questions, 
        df_uibgeophys_2019_students_common_questions, 
        df_uio_2019_students_common_questions, 
        df_uit_2019_students_common_questions, 
        df_unis_2019_students_common_questions
        ], ignore_index=True)

    # add a column with the year
    df_2019_students["year"] = year_2019

    # add a column with the institution index
    def convert_text_university_to_numeric_2019_students(df):
        df["institution"] = df["Which of these educational institutions are you studying at?"].replace(
            map_institution
        )
        return df

    df_2019_students = convert_text_university_to_numeric_2019_students(df_2019_students)

    return df_2019_students, common_questions_students_2019

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

    # merge dataframes with the questions available in all dataframes
    common_questions_educators_2019 = list(
        set(df_uib_2019_educators_raw.columns) 
        & set(df_uibgeophys_2019_educators_raw.columns) 
        & set(df_uio_2019_educators_raw.columns) 
        & set(df_uit_2019_educators_raw.columns) 
        & set(df_unis_2019_educators_raw.columns)
    )

    # pick out the common questions from each dataframe
    df_uib_2019_educators_common_questions = df_uib_2019_educators_raw[common_questions_educators_2019].copy()
    df_uibgeophys_2019_educators_common_questions = df_uibgeophys_2019_educators_raw[common_questions_educators_2019].copy()
    df_uio_2019_educators_common_questions = df_uio_2019_educators_raw[common_questions_educators_2019].copy()
    df_uit_2019_educators_common_questions = df_uit_2019_educators_raw[common_questions_educators_2019].copy()
    df_unis_2019_educators_common_questions = df_unis_2019_educators_raw[common_questions_educators_2019].copy()

    # merge the dataframes containing only the common questions
    df_2019_educators = pd.concat([
        df_uib_2019_educators_common_questions, 
        df_uibgeophys_2019_educators_common_questions, 
        df_uio_2019_educators_common_questions, 
        df_uit_2019_educators_common_questions, 
        df_unis_2019_educators_common_questions
        ], ignore_index=True)

    # add a column with the year
    df_2019_educators["year"] = year_2019

    # add a column with the institution index
    def convert_text_university_to_numeric_2019_educators(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2019_educators = convert_text_university_to_numeric_2019_educators(df_2019_educators)
    return df_2019_educators, common_questions_educators_2019

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

    # find the questions that are present in all dataframes 
    common_questions_2019_admintech = list(
        set(df_uib_2019_noneducators_raw.columns)
        & set(df_uibgeophys_noneducators_raw.columns)
        & set(df_uio_2019_noneducators_raw.columns)
        & set(df_uit_2019_noneducators_raw.columns)
        # & set(df_unis_2019_noneducators_raw.columns) # <- does not exist
        & set(df_uib_2019_admintech_raw.columns) 
        & set(df_uibgeophys_2019_admintech_raw.columns) 
        & set(df_uio_2019_admintech_raw.columns) 
        & set(df_uit_2019_admintech_raw.columns) 
        & set(df_unis_2019_admintech_raw.columns)
    )

    # pick out the common questions from each dataframe
    df_uib_2019_noneducators_common_questions = df_uib_2019_noneducators_raw[common_questions_2019_admintech].copy()
    df_uibgeophys_noneducators_common_questions = df_uibgeophys_noneducators_raw[common_questions_2019_admintech].copy()
    df_uio_2019_noneducators_common_questions = df_uio_2019_noneducators_raw[common_questions_2019_admintech].copy()
    df_uit_2019_noneducators_common_questions = df_uit_2019_noneducators_raw[common_questions_2019_admintech].copy()
    # df_unis_2019_noneducators_common_questions = df_unis_2019_noneducators_raw[common_questions_2019_admintech].copy() # <- does not exist
    df_uib_2019_admintech_common_questions = df_uib_2019_admintech_raw[common_questions_2019_admintech].copy()
    df_uibgeophys_2019_admintech_common_questions = df_uibgeophys_2019_admintech_raw[common_questions_2019_admintech].copy()
    df_uio_2019_admintech_common_questions = df_uio_2019_admintech_raw[common_questions_2019_admintech].copy()
    df_uit_2019_admintech_common_questions = df_uit_2019_admintech_raw[common_questions_2019_admintech].copy()
    df_unis_2019_admintech_common_questions = df_unis_2019_admintech_raw[common_questions_2019_admintech].copy()

    # merge the dataframes containing only the common questions
    df_2019_admintech = pd.concat([
        df_uib_2019_noneducators_common_questions,
        df_uibgeophys_noneducators_common_questions,
        df_uio_2019_noneducators_common_questions,
        df_uit_2019_noneducators_common_questions,
        # df_unis_2019_noneducators_common_questions, # <- does not exist
        df_uib_2019_admintech_common_questions, 
        df_uibgeophys_2019_admintech_common_questions, 
        df_uio_2019_admintech_common_questions, 
        df_uit_2019_admintech_common_questions, 
        df_unis_2019_admintech_common_questions
        ], ignore_index=True)

    # add a column with the year
    df_2019_admintech["year"] = year_2019

    # add a column with the institution index
    def convert_text_university_to_numeric_2019_admintech(df):
        df["institution"] = df["Where are you employed?"].replace(
            map_institution
        )
        return df

    df_2019_admintech = convert_text_university_to_numeric_2019_admintech(df_2019_admintech)
    return df_2019_admintech, common_questions_2019_admintech


def load_2026_data_students_filter_with_2019(common_questions_students_2019):
    # load data
    df_2026_students_path = "..\\2026data\\data_2026_students.xlsx"
    df_2026_students_raw = pd.read_excel(df_2026_students_path)

    # a special case. we should be able to check for whitespace
    df_2026_students_raw["Fieldwork skills"] = df_2026_students_raw[" Fieldwork skills"]

    common_questions_students_2019_2026 = list(
        set(df_2026_students_raw.columns) 
        & set(common_questions_students_2019)
    )

    # pick out the common questions from the dataframe
    df_2026_students = df_2026_students_raw[common_questions_students_2019_2026].copy()

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

def load_2026_data_educators_filter_with_2019(common_questions_educators_2019):
    # load data
    df_2026_educators_path = "..\\2026data\\data_2026_educators.xlsx"
    df_2026_educators_raw = pd.read_excel(df_2026_educators_path)

    # find the questions that are present in both dataframes
    common_questions_educators_2019_2026 = list(
        set(df_2026_educators_raw.columns) 
        & set(common_questions_educators_2019)
    )

    # pick out the common questions from the dataframe
    df_2026_educators = df_2026_educators_raw[common_questions_educators_2019_2026].copy()

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

def load_2026_data_admintech_filter_with_2019(common_questions_2019_admintech):
    # load data
    df_2026_admintech_path = "..\\2026data\\data_2026_admintech.xlsx"
    df_2026_admintech_raw = pd.read_excel(df_2026_admintech_path)

    # find the questions that are present in both dataframes
    common_questions_admintech_2019_2026 = list(
        set(df_2026_admintech_raw.columns) 
        & set(common_questions_2019_admintech)
    )

    # pick out the common questions from the dataframe
    df_2026_admintech = df_2026_admintech_raw[common_questions_admintech_2019_2026].copy()

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
    df_2026_admintech):
    # students
    common_questions_students = list(
          set(df_2019_students.columns) 
        & set(df_2026_students.columns)
    )
    df_2019_students_ready_to_merge = df_2019_students[common_questions_students].copy()
    df_2026_students_ready_to_merge = df_2026_students[common_questions_students].copy()
    df_students = pd.concat([df_2019_students_ready_to_merge, df_2026_students_ready_to_merge], ignore_index=True)

    # educators
    common_questions_educators = list(
          set(df_2019_educators.columns) 
        & set(df_2026_educators.columns)
    )
    df_2019_educators_ready_to_merge = df_2019_educators[common_questions_educators].copy()
    df_2026_educators_ready_to_merge = df_2026_educators[common_questions_educators].copy()
    df_educators = pd.concat([df_2019_educators_ready_to_merge, df_2026_educators_ready_to_merge], ignore_index=True)

    # admintech
    common_questions_admintech = list(
          set(df_2019_admintech.columns) 
        & set(df_2026_admintech.columns)
    )
    df_2019_admintech_ready_to_merge = df_2019_admintech[common_questions_admintech].copy()
    df_2026_admintech_ready_to_merge = df_2026_admintech[common_questions_admintech].copy()
    df_admintech = pd.concat([df_2019_admintech_ready_to_merge, df_2026_admintech_ready_to_merge], ignore_index=True)


    # example_question = "Have you experienced strong stress symptoms * in your study up to the exam?"
    # example_question = "Theoretical understanding.1"
    # example_question = "year"
    # df_2019_students[example_question].value_counts()
    # df_2026_students[example_question].value_counts()
    # df_students[example_question].value_counts()

    return (
        df_students, 
        df_educators, 
        df_admintech, 
        common_questions_students, 
        common_questions_educators, 
        common_questions_admintech
    )
