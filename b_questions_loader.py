import pandas as pd
import random

def load_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    questions = df.to_dict(orient='records')

    processed_questions = []
    for question in questions:
        if question['categorie'] == 'Departajare':
            # Tratați întrebările de departajare diferit
            processed_question = {
                'categorie': 'Departajare',
                'întrebare': question['întrebare'],
                'răspuns corect': question['răspuns corect']  # Presupunem că acesta este un număr
            }
        else:
            # Procesarea normală pentru celelalte întrebări
            answers = [question['răspuns corect'], question['răspuns1'], question['răspuns2'], question['răspuns3']]
            random.shuffle(answers)
            processed_question = {
                'categorie': question['categorie'],
                'întrebare': question['întrebare'],
                'răspunsuri': answers,
                'răspuns corect': question['răspuns corect']
            }
        processed_questions.append(processed_question)

    print(f"Am încărcat {len(processed_questions)} întrebări din fișierul {file_path}")
    return processed_questions