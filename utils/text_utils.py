import re
import unicodedata

from bs4 import BeautifulSoup


def clean_html(text):
    """
    given a string that contains html tags return plain text
    """
    clean = BeautifulSoup(text, features="lxml").get_text(strip=True, separator=" ")
    # remove \xa0
    clean = unicodedata.normalize("NFKD", clean)
    return clean


def sep_exp(text):
    """
    given a string add a space before and after expression token
    3x+2=1 to 3x + 2 = 1
    """
    pat = re.compile(r"([-+/*=><])")
    return pat.sub(" \\1 ", text)


def remove_url(text):
    """
    given a string remove url
    """
    return re.sub(r'[\S]+\.(net|com|org|info|edu|gov|uk|de|ca|jp|fr|au|us|ru|ch|it|nel|se|no|es|mil)[\S]*\s?', '', text)


def remove_newline(text):
    """
    given a string remove new line
    """
    return text.replace("\r\n", " ").replace("\n", " ")


def remove_page(text):
    """
      given a string remove the ref about the exercise number/page at the beginning
    """
    words = text.split()
    page = ["page", "Page", "Pg", "Pg.", "pg", "pg."]

    if len(words) >= 3:
        if words[0] in page and any(map(str.isdigit, words[1])) and words[2][0] == '#':
            return " ".join(words[3:])

    elif len(words) >= 3:
        if words[0] in page and any(map(str.isdigit, words[1])):
            return " ".join(words[2:])

    return text


def remove_question(text):
    """
         given a string remove the ref about the question number/page at the beginning
    """
    words = text.split()
    questions = ["Question", "question"]

    if len(words) >= 2:
        if words[0] in questions and any(map(str.isdigit, words[1])):
            return " ".join(words[2:])
    return text


def remove_hash(text):
    """
             given a string remove # at the beginning.
    """
    words = text.split()

    if len(words) > 0:
        if '#' in words[0]:
            return " ".join(words[1:])
    return text


def replace_underscore(text):
    """
        given a string replace multiple underscore with only one
    """
    return re.sub('_+', '_', text)
