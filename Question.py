from enum import Enum
import re
from pprint import pprint


class Question:
    question = ""
    correctAnswer = ""
    incorrectAnswers = []
    image = None


def read_questions(file_name):
    result = []
    with open(file_name, 'r') as fp:
        currentCategory = None
        currentQuestion = None
        for line in fp:
            m = re.match("(.*): (.*)", line)
            if m is None:
                continue
            key = m.group(1)
            statement = m.group(2)
            if key.upper() == "CATEGORY":
                if currentCategory is not None:
                    result.append(currentCategory)
                currentCategory = {}
                currentCategory['name'] = statement
                currentCategory['easy'] = []
                currentCategory['medium'] = []
                currentCategory['hard'] = []
            if key.upper() in {"QE", "QM", "QH"} and currentCategory is not None:
                currentQuestion = Question()
                currentQuestion.incorrectAnswers = []
                currentQuestion.question = statement
                answer_match = re.match("(.*): (.*)", fp.readline())
                count = 0
                while answer_match is not None:
                    if count == 0 and answer_match[1] == 'IMG':
                        currentQuestion.image = answer_match[2]
                    elif count == 0 and answer_match[1] == "A":
                        currentQuestion.correctAnswer = answer_match[2]
                        count += 1
                    else:
                        currentQuestion.incorrectAnswers.append(answer_match[2])
                    answer_match = re.match("(.*): (.*)", fp.readline())
                if key.upper() == "QE":
                    currentCategory['easy'].append(currentQuestion)
                elif key.upper() == "QM":
                    currentCategory['medium'].append(currentQuestion)
                elif key.upper() == "QH":
                    currentCategory['hard'].append(currentQuestion)
        result.append(currentCategory)
    return result
