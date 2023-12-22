import sys
from PyQt5.QtWidgets import QApplication
from category_selection_window import CategorySelectionWindow
from question_window import QuestionWindow
from questions_loader import load_questions_from_excel

from start_window import StartWindow

class MainApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.teamNames = []
        self.timerDuration = 30
        self.categorySelectionTime = 30
        self.numClassicRounds = 0
        self.numThiefRounds = 0
        self.numChampionRounds = 0
        self.startWindow = StartWindow(self)
        self.startWindow.show()
        self.championRoundsEnabled = False
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: white; 
                font-family: Arial;
            }
            QLabel {
                font-size: 18px;
                text-align: center;
            }
            QPushButton {
                background-color: #444;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
                font-size: 16px;
                min-height: 30px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QLineEdit {
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }
            # QSpinBox {
            #     border: 1px solid #555;
            #     border-radius: 5px;
            #     padding: 5px;
            #     margin: 5px;
            # }
            QCheckBox {
                spacing: 5px;
            }
        """)
        # self.setStyleSheet("QWidget { font-size: 14pt; }")
        # self.setStyleSheet("QWidget { color: white; }") ## in loc de QWidgent poate fi trecut Qdialog sau altceva
        
        self.currentTeamIndex = -1
        self.currentTeamName = self.teamNames[self.currentTeamIndex] if self.teamNames else None
        
        self.questions = []
        self.selected_question = []
        
        self.randomQuestion = False
        self.totalScores = {}
        self.roundType = None

    def showNextScreen(self):
        self.nextTeam()
        self.categorySelectionWindow = CategorySelectionWindow(self)
        self.startWindow.hide()  # Ascundem fereastra de start
        self.categorySelectionWindow.show()  # Afișăm fereastra de selecție a categoriilor
        
    def showQuestionScreen(self, question, answers):
        self.questionWindow = QuestionWindow(self, question, answers, teams=self.teamNames)
        self.questionWindow.show()

    def nextTeam(self):
        if self.teamNames:
            self.randomQuestion = False
            self.currentTeamIndex = (self.currentTeamIndex + 1) % len(self.teamNames) # Trecem la următoarea echipă din listă (sau prima dacă am ajuns la final)
            self.currentTeamName = self.teamNames[self.currentTeamIndex] # Actualizăm numele echipei de rând
    
    def loadQuestions(self, filePath):
        # Încărcați întrebările din fișierul Excel specificat
        self.questions = load_questions_from_excel(filePath)

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
