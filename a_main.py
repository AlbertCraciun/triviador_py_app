import sys
from PyQt5.QtWidgets import QApplication
from d_category_selection import CategorySelectionWindow
from g_duel_start import DuelTransitionWindow
from h_duel_selection import DuelSelectionWindow
from e_question_window import QuestionWindow
from b_questions_loader import load_questions_from_excel

from c_start_window import StartWindow

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
        
        self.currentTeamIndex = -1
        self.currentTeamName = self.teamNames[self.currentTeamIndex] if self.teamNames else None
        
        self.questions = []
        self.selected_question = []
        
        self.randomQuestion = False
        self.totalScores = {}
        self.roundType = "Classic"
        self.passedRounds = 0

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
            self.currentTeamIndex = (self.currentTeamIndex + 1) % len(self.teamNames)
            self.currentTeamName = self.teamNames[self.currentTeamIndex]
            self.passedRounds += 1

            # Verificăm dacă s-au terminat rundele clasice
            if self.passedRounds > self.numClassicRounds:
                # Dacă există runde de duel, le începem
                if self.numThiefRounds > 0 and self.roundType == "Classic":
                    self.roundType = "Thief"
                    self.numThiefRounds -= 1
                    self.startDuel()
                # Dacă nu mai sunt runde de duel, trecem la runde de campioni, dacă sunt specificate
                elif self.numChampionRounds > 0 and self.roundType != "Champion":
                    self.roundType = "Champion"
                    self.numChampionRounds -= 1
                    # TODO: Implementați logica pentru a începe runda de campioni
                # Dacă nu mai sunt nici runde de duel, nici de campioni, jocul se termină
                else:
                    # TODO: Implementați logica pentru a încheia jocul
                    pass
    
    def loadQuestions(self, filePath):
        # Încărcați întrebările din fișierul Excel specificat
        self.questions = load_questions_from_excel(filePath)
        
    def startDuel(self):
        # Afișăm fereastra de tranziție către duel
        self.duelTransitionWindow = DuelTransitionWindow(self)
        self.duelTransitionWindow.show()

    def initiateDuel(self, opponent, category):
        # Logica pentru inițierea duelului
        self.selectedOpponent = opponent
        self.selectedCategory = category
        # TODO: ... cod pentru a începe duelul, cum ar fi afișarea unei întrebări ...
        
    def endGame(self):
        # Afișează un mesaj de felicitare sau un ecran final
        # QMessageBox.information(None, "Joc Terminat", "Felicitări tuturor echipelor pentru participare!")
        self.quit()  # Încheie aplicația

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
