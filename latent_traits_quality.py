"""
This script compares the latent traits of the questions, calculate on different interactions subsets of the same size.
INPUT: min_interactions for subset, model (1PL or 2PL)
It generates stats about the difference of lt on the 2 subsets.
example:
subset 1: difficulty[question1] = 0.1 . . .
subset 2: difficulty[question1] = 0.3 . . .
result: difference[question1] = 0.2 . . . .
"""

from datetime import datetime

import pandas as pd

from utils.constant import (
    CORRECT_HEADER,
    USER_ID_HEADER,
    QUESTION_ID_HEADER,
    TIMESTAMP_HEADER,
    DIFFICULTY_MIN,
    DIFFICULTY_MAX,
    DISCRIMINATION_MIN,
    DISCRIMINATION_MAX,
    DEFAULT_GUESS,
    CLEAN_INTERACTION_PATH,
    RESULT_PATH,
    MIN_INTERACTION
)
from utils.estimators import irt_estimation

if DISCRIMINATION_MAX == DISCRIMINATION_MIN:
    model = "1PL"
else:
    model = "2PL"
# description to save in output file
description = "Model: " + model + "\n"
description += "Minimum interactions per problem is: " + str(MIN_INTERACTION) + "\n"

interactions = pd.read_csv(CLEAN_INTERACTION_PATH,
                           usecols=[QUESTION_ID_HEADER, USER_ID_HEADER, TIMESTAMP_HEADER, CORRECT_HEADER])
print("INTERACTIONS loaded")

interactions = interactions[
    interactions[QUESTION_ID_HEADER].groupby(interactions[QUESTION_ID_HEADER]).transform('size') >= MIN_INTERACTION * 2]

print(interactions[QUESTION_ID_HEADER].nunique())
g1 = interactions.groupby(QUESTION_ID_HEADER).head(MIN_INTERACTION)
g2 = interactions.groupby(QUESTION_ID_HEADER).tail(MIN_INTERACTION)

user_g1, question_g1 = irt_estimation(g1, (DIFFICULTY_MIN, DIFFICULTY_MAX),
                                      (DISCRIMINATION_MIN, DISCRIMINATION_MAX), DEFAULT_GUESS)
user_g2, question_g2 = irt_estimation(g2, (DIFFICULTY_MIN, DIFFICULTY_MAX),
                                      (DISCRIMINATION_MIN, DISCRIMINATION_MAX), DEFAULT_GUESS)

d1 = pd.DataFrame.from_dict(question_g1)
d1.rename(columns={'difficulty': 'difficulty_g1', 'discrimination': 'discrimination_g1'}, inplace=True)

d2 = pd.DataFrame.from_dict(question_g2)
d2.rename(columns={'difficulty': 'difficulty_g2', 'discrimination': 'discrimination_g2'}, inplace=True)

columns_df = ['difficulty_g1', 'difficulty_g2']
columns_ds = ['discrimination_g1', 'discrimination_g2']
merged = pd.concat([d1, d2], axis=1)
discrimination_n = merged[columns_ds]
difficulty_n = merged[columns_df]

x = difficulty_n['difficulty_g1'] - difficulty_n['difficulty_g2']
mean_diff = (x.abs().mean() * 100) / (DIFFICULTY_MAX - DIFFICULTY_MIN)
description += "avg difference Difficulty: " + str(mean_diff) + "%" + "\n"

x = discrimination_n['discrimination_g1'] - discrimination_n['discrimination_g2']
mean_discr = (x.abs().mean() * 100) / (DIFFICULTY_MAX - DIFFICULTY_MIN)
description += "avg difference Discrimination: " + str(mean_discr) + "%" + "\n"

print("RESULT:\n")
print(description)
file_name = '/lt_quality_'
file_name += datetime.now().strftime('%b%d_%H-%M-%S') + '.txt'
f = open(RESULT_PATH + file_name, "w")
f.write(description)
f.close()
