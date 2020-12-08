"""
This script do the pre-processing of the original ASSISTments datasets: first on the interactions dataset
then on the texts dataset.
It generates interactions.csv and texts.csv
"""
import pandas as pd

from utils.constant import (
    CORRECT_HEADER,
    QUESTION_TEXT_HEADER,
    QUESTION_ID_HEADER,
    DATA_PATH,
    RAW_TEXT_PATH,
    RAW_INTERACTION_PATH,
    USER_ID_HEADER,
    TIMESTAMP_HEADER,
    MIN_INTERACTION
)
from utils.data_processing import int_processing, text_processing

# load the interactions dataset
interactions = pd.read_csv(RAW_INTERACTION_PATH,
                           usecols=[QUESTION_ID_HEADER, USER_ID_HEADER, TIMESTAMP_HEADER, CORRECT_HEADER,
                                    'template_id', 'problem_type', 'original'])
print("INTERACTIONS loaded")
# load the text dataset
texts = pd.read_csv(RAW_TEXT_PATH, usecols=[QUESTION_ID_HEADER, QUESTION_TEXT_HEADER])
print("TEXTS loaded")

# dict problem_id -> original
original_dict = dict(zip(interactions[QUESTION_ID_HEADER], interactions['original']))
# dict problem_id -> problem_type
type_dict = dict(zip(interactions[QUESTION_ID_HEADER], interactions['problem_type']))

# add to texts dataset the columns original and problem_type
texts['original'] = texts[QUESTION_ID_HEADER].map(original_dict)
texts['problem_type'] = texts[QUESTION_ID_HEADER].map(type_dict)


def split_original(row):
    """
    create a unique id for scaffolding problem (original=0) from the same template
    """
    if row['original'] == 0:
        return str(row['template_id']) + '000000' + str(row[QUESTION_ID_HEADER])
    return row['template_id']


# apply function split_original
interactions['template_id'] = interactions.apply(split_original, axis=1)

# dict problem_id -> template_id
template_dict = dict(zip(interactions[QUESTION_ID_HEADER], interactions['template_id']))
texts[QUESTION_ID_HEADER] = texts[QUESTION_ID_HEADER].map(template_dict)

interactions['template_id'] = interactions['template_id'].astype(int)

# template_id as key
interactions[QUESTION_ID_HEADER] = interactions['template_id']

# clean interactions dataset
interactions = int_processing(interactions, min_interaction=MIN_INTERACTION)

# delete from texts dataset problems with no enough interactions
texts = texts[texts[QUESTION_ID_HEADER].isin(set(interactions[QUESTION_ID_HEADER]))]

# clean texts dataset
texts = text_processing(texts)

# keep one text per template_id
texts.drop_duplicates(subset=QUESTION_ID_HEADER, keep='first', inplace=True)
# delete duplicates texts
texts.drop_duplicates(subset=QUESTION_TEXT_HEADER, keep=False, inplace=True)

interactions.to_csv(DATA_PATH + 'interactions.csv', index=False)
print("pre-processed INTERACTIONS saved in " + DATA_PATH)
texts.to_csv(DATA_PATH + 'texts.csv', index=False)
print("pre-processed TEXTS saved in " + DATA_PATH)
