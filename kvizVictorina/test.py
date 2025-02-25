from questions import question_lite, question_normal, question_hard
import random

correctAnswersInARow = 0
question_number = 1  # Инициализируем с 0
difficulty_level = 1  # Здесь можно изменять уровень сложности: 1 - легкий, 2 - нормальный, 3 - сложный
reward = 0
level = 0


def get_questions_by_difficulty(level):
    if level == 1:
        return question_lite
    elif level == 2:
        return question_normal
    elif level == 3:
        return question_hard
    else:
        return []


def split_the_wrong_questions_lite(question):
    question_parts = question['wrong answer'].split(', ')
    question["wrong answer1"] = question_parts[0] if len(question_parts) > 0 else None
    question["wrong answer2"] = question_parts[1] if len(question_parts) > 1 else None
    question["wrong answer3"] = question_parts[2] if len(question_parts) > 2 else None
    return question


def new_data(question):
    ques = split_the_wrong_questions_lite(question)
    wrong_answers = [ques["wrong answer1"], ques["wrong answer2"], ques["wrong answer3"]]
    right_answer = ques['right answer']

    # Убираем None из ответа
    wrong_answers = [ans for ans in wrong_answers if ans is not None]
    all_answers = wrong_answers + [right_answer]
    random.shuffle(all_answers)

    user_all_answer = ', '.join(all_answers)  # Форматированный вывод
    return user_all_answer, right_answer


def revand_for_correct_answers_in_a_Row(correctAnswersInARow, reward):
    if correctAnswersInARow in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
        reward += 5
        print(f"Ого! Вы ответили на {correctAnswersInARow} вопроса подряд, "
              f"теперь вы будете получать на {reward} очков больше")
    return reward


while True:
    questions = get_questions_by_difficulty(difficulty_level)

    if question_number <= len(questions):
        questionl = questions[question_number]  # Получаем текущий вопрос каждый раз
        user_all_answer, right_answer = new_data(questionl)
        print(questionl['question'])
        print(f'Варианты ответов: \n{user_all_answer}')
        user_answer = input("Введите вариант ответа: ").lower()

        if user_answer.replace('ё', "е").lower() == right_answer.replace("ё", "е").lower():
            print("You WIN")
            correctAnswersInARow += 1
            question_number += 1
            level += 1
        else:
            print('You UNWIN')
            correctAnswersInARow = 0

        # Уровень сложности повышается после определенного количества правильных ответов, например 3
        if correctAnswersInARow >= 3:
            difficulty_level += 1
            question_number = 0  # Сбрасываем номер вопроса для нового уровня сложности
            correctAnswersInARow = 0  # Сбрасываем счетчик правильных ответов
    else:
        print("Вы исчерпали все вопросы на этом уровне сложности.")
        break

"""from questions import question_lite, question_normal, question_hard
import random

correctAnswersInARow = 0
question_number = 1
difficulty_level = 1
level = 0


def split_the_wrong_questions_lite(question):
    question_parts = question['wrong answer'].split(', ')
    question["wrong answer1"] = question_parts[0] if len(question_parts) > 0 else None
    question["wrong answer2"] = question_parts[1] if len(question_parts) > 1 else None
    question["wrong answer3"] = question_parts[2] if len(question_parts) > 2 else None
    return question


def new_data(question):
    ques = split_the_wrong_questions_lite(question)
    wrong_answers = [ques["wrong answer1"], ques["wrong answer2"], ques["wrong answer3"]]
    right_answer = ques['right answer']

    # Убираем None из ответа
    wrong_answers = [ans for ans in wrong_answers if ans is not None]
    all_answers = wrong_answers + [right_answer]
    random.shuffle(all_answers)

    user_all_answer = ', '.join(all_answers)  # Форматированный вывод
    return user_all_answer, right_answer


if difficulty_level == 1:
    while question_number <= len(question_lite):
        questionl = question_lite[question_number]  # Получаем текущий вопрос каждый раз
        user_all_answer, right_answer = new_data(questionl)
        print(questionl['question'])
        print(f'Варианты ответов: \n{user_all_answer}')
        user_answer = input("Введите вариант ответа: ").lower()

        if user_answer.replace('ё', "е").lower() == right_answer.replace("ё", "е").lower():
            print("You WIN")
            correctAnswersInARow += 1
            question_number += 1
            level += 1
        else:
            print('You UNWIN')
            correctAnswersInARow = 0
"""
