from utils.constant import QUESTION_ID_HEADER, USER_ID_HEADER, CORRECT_HEADER, QUESTION_TEXT_HEADER
from utils.text_utils import (clean_html, remove_hash, remove_newline,
                              remove_page, remove_question, remove_url,
                              sep_exp)


def int_processing(df, min_interaction=50):
    """
    given interaction dataset:
    - select significant columns
    - keep first attempt for each user
    - convert decimal value to binary
    - remove items with less than min_interaction
    :param df: interactions dataframe QUESTION_ID, USER_ID, TIMESTAMP, CORRECT
    :param min_interaction: min number of interactions (log) x problem
    :return: pre-processed dataframe
    """
    df.sort_values('start_time', inplace=True)
    df.drop_duplicates(subset=[QUESTION_ID_HEADER, USER_ID_HEADER],
                       keep='first',
                       inplace=True)
    df[CORRECT_HEADER] = df[CORRECT_HEADER].astype(int)
    df = df[df[QUESTION_ID_HEADER].groupby(df[QUESTION_ID_HEADER]).transform('size') >= min_interaction]

    return df


def text_processing(df, transform_only=False):
    """
    preprocessing of the dataframe that contains the texts: remove useless part of the text and remove bad questions
    :param df: dataframe QUESTION_ID, QUESTION_TEXT
    :return: cleaned dataframe QUESTION_ID, QUESTION_TEXT
    """
    df[QUESTION_TEXT_HEADER] = df[QUESTION_TEXT_HEADER].astype(str)
    df[QUESTION_TEXT_HEADER] = df[QUESTION_TEXT_HEADER].apply(lambda x: transform(x))
    if transform_only:
        return df

    df = df[df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) > 2)]

    pattern = 'Sorry, that is incorrect'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'If your answer is positive'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Submit your answer from the textbook'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'QUESTION'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 10)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'your answer from your worksheet'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Choose A, B, C or D'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 10)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Please select the correct answer to question'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 10)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Number'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 3)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Problem'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 3)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Please record your answer to Question'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 10)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Be careful!'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 5)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Watch video'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 5)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Do not enter labels.'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 6)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Term 3 Sheet 4'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 6)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Enter your answer from your bubble sheet'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 10)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    pattern = 'Enter the number ONLY'
    p = df[df[QUESTION_TEXT_HEADER].str.contains(pattern)
           & df[QUESTION_TEXT_HEADER].map(lambda x: len(x.split()) < 10)]
    df = df.loc[~df[QUESTION_ID_HEADER].isin(p[QUESTION_ID_HEADER])]

    df.reset_index(drop=True, inplace=True)
    return df


def transform(text):
    """
    apply multiple functions to clean the text
    :param text: string of the question
    :return: transformed string
    """
    text = clean_html(text)
    text = remove_url(text)
    text = remove_newline(text)
    text = sep_exp(text)
    text = remove_page(text)
    text = remove_question(text)
    text = remove_hash(text)

    return text
