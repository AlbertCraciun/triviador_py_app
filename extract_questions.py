import pandas as pd
import random

def load_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    questions = df.to_dict(orient='records')  # Convertim fiecare rând într-un dicționar

    for question in questions:
        answers = [question['răspuns corect'], question['răspuns1'], question['răspuns2'], question['răspuns3']]
        random.shuffle(answers)  # Amestecăm răspunsurile
        question['answers'] = answers

    return questions
