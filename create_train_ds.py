"""
This script creates the dataset: text - difficulty - [discrimination]
"""

import pandas as pd

from utils.constant import (
    QUESTION_ID_HEADER,
    DIFFICULTY_MIN,
    DIFFICULTY_MAX,
    DISCRIMINATION_MIN,
    DISCRIMINATION_MAX,
    DEFAULT_GUESS,
    CLEAN_INTERACTION_PATH,
    CLEAN_TEXT_PATH,
    DATA_PATH
)
from utils.estimators import irt_estimation

# read cleaned interactions
interactions = pd.read_csv(CLEAN_INTERACTION_PATH)
print("INTERACTIONS loaded")
# fit the IRT model
user_d, question_d = irt_estimation(interactions, (DIFFICULTY_MIN, DIFFICULTY_MAX),
                                    (DISCRIMINATION_MIN, DISCRIMINATION_MAX), DEFAULT_GUESS)

df = pd.DataFrame.from_dict(question_d)
texts = pd.read_csv(CLEAN_TEXT_PATH)
print("TEXTS loaded")
final = pd.merge(texts, df, right_index=True, left_on=QUESTION_ID_HEADER)

final.to_csv(DATA_PATH + 'text_difficulty.csv', index=False)
print("text + latent traits dataset saved in " + DATA_PATH)
