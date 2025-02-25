"""
4. Квиз-викторина
Программа задает пользователю вопросы (например, по общим знаниям)
 и подсчитывает количество правильных ответов.
Можно добавить несколько вариантов ответов на каждый вопрос.
"""
from questions import question_lite, question_normal, question_hard
import random

correctAnswersInARow = 0
question_number = 1
questionl = question_lite[question_number]
questionN = question_normal[question_number]
questionh = question_hard[question_number]
difficulty_level = 1
level = 0


def split_the_wrong_questions_lite(questionl):
    question_parts = questionl['wrong answer'].split(', ')
    questionl["wrong answer1"] = question_parts[0]

    if len(question_parts) > 1:
        questionl["wrong answer2"] = question_parts[1]
    else:
        questionl["wrong answer2"] = None  # или любое другое значение по умолчанию

    if len(question_parts) > 2:
        questionl["wrong answer3"] = question_parts[2]
    else:
        questionl["wrong answer3"] = None  # или любое другое значение по умолчанию

    return questionl

def new_data():
    ques = split_the_wrong_questions_lite(questionl)
    wrong_answer1 = ques["wrong answer1"]
    wrong_answer2 = ques["wrong answer2"]
    wrong_answer3 = ques["wrong answer3"]
    right_answer = questionl['right answer']

    all_answer = [wrong_answer1, wrong_answer2, wrong_answer3, right_answer]
    random.shuffle(all_answer)
    user_all_answer = str(all_answer).replace('[', '').replace(']', '').replace("'", "")
    return user_all_answer, right_answer

def split_the_wrong_questions_norm(questionN):
    while True:
        question_parts = questionN['wrong answer'].split(', ')
        questionN["wrong answer1"] = question_parts[0]
        if len(question_parts) > 2:
            questionN["wrong answer2"] = question_parts[1]
        if len(question_parts) > 1:
            questionN["wrong answer3"] = question_parts[2]
            break
    return questionN["wrong answer1"], questionN["wrong answer2"], questionN["wrong answer3"]

def split_the_wrong_questions_hard(questionh):
    while True:
        question_parts = questionh['wrong answer'].split(', ')
        questionh["wrong answer1"] = question_parts[0]
        if len(question_parts) > 2:
            questionh["wrong answer2"] = question_parts[1]
        if len(question_parts) > 1:
            questionh["wrong answer3"] = question_parts[2]
            break
    return questionh["wrong answer1"], questionh["wrong answer2"], questionh["wrong answer3"]


if difficulty_level == 1:
    while question_number <= len(question_lite):
        user_all_answer, right_answer = new_data()
        print(questionl['question'])
        print(f'Варианты ответов: \n{user_all_answer} ')
        user_answer = input("Введите вариант ответа: ").lower()
        if user_answer.replace('ё', "е").lower() == right_answer.replace("ё", "е").lower():
            print("You WIN")
            correctAnswersInARow += 1
            question_number += 1
            level += 1
        else:
            print('You UNWIN')
            correctAnswersInARow = 0
