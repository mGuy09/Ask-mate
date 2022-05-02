import os

import connection


questions = os.environ["QUESTION"]
answers = os.environ["ANSWER"]

questions_data = connection.read_question(questions)
answers_data = connection.read_question(answers)
