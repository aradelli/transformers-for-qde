# data folder
DATA_PATH = 'data/'
RESULT_PATH = 'data/results'
RAW_TEXT_PATH = 'data/ASSISTments2012DataSet-ProblemBodies.csv'
RAW_INTERACTION_PATH = 'data/ASSISTmentsData_reduced.csv'
CLEAN_TEXT_PATH = 'data/texts.csv'
CLEAN_INTERACTION_PATH = 'data/interactions.csv'
TEXT_DIFFICULTY_PATH = 'data/text_difficulty.csv'

# pre processing
MIN_INTERACTION = 50

# headers
ASSIGNMENT_ID_HEADER = 'assignment_id'
CORRECT_HEADER = 'correct'
QUESTION_ID_HEADER = 'problem_id'
QUESTION_TEXT_HEADER = 'body'
TIMESTAMP_HEADER = 'start_time'
USER_ID_HEADER = 'user_id'
DIFFICULTY_KEY = 'difficulty'
DISCRIMINATION_KEY = 'discrimination'

# values used in the IRT estimation
DIFFICULTY_MIN = -5.0
DIFFICULTY_MAX = 5.0
DEFAULT_DISCRIMINATION = 1.0
DISCRIMINATION_MIN = 1.0
DISCRIMINATION_MAX = 1.0
DEFAULT_GUESS = 0.0
DEFAULT_SLIP = 0.0
