import pandas as pd
import random

def load_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    questions = df.to_dict(orient='records')

    processed_questions = []
    for question in questions:
        answers = [question['răspuns corect'], question['răspuns1'], question['răspuns2'], question['răspuns3']]
        random.shuffle(answers)

        # Păstrăm răspunsul corect și categoria pentru fiecare întrebare
        processed_question = {
            'categorie': question['categorie'],
            'întrebare': question['întrebare'],
            'răspunsuri': answers,
            'răspuns corect': question['răspuns corect']
        }
        processed_questions.append(processed_question)

    return processed_questions
