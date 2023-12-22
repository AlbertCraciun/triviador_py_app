import sys
from PyQt5.QtWidgets import QApplication
from category_selection_screen import CategorySelectionWindow
from question_screen import QuestionWindow

from start_screen import StartWindow

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
        self.setStyleSheet("QWidget { background-color: black; }")
        # self.setStyleSheet("QWidget { font-size: 14pt; }")
        # self.setStyleSheet("QWidget { color: white; }") ## in loc de QWidgent poate fi trecut Qdialog sau altceva
        
        self.currentTeamIndex = 1
        self.currentTeamName = self.teamNames[self.currentTeamIndex] if self.teamNames else None

    def showNextScreen(self):
        self.categorySelectionWindow = CategorySelectionWindow(self)
        self.startWindow.hide()  # Ascundem fereastra de start
        self.categorySelectionWindow.show()  # Afișăm fereastra de selecție a categoriilor
        
    def showQuestionScreen(self, question, answers):
        self.questionWindow = QuestionWindow(self, question, answers, teams=self.teamNames)
        self.questionWindow.show()

    def nextTeam(self):
        if self.teamNames:
            self.currentTeamIndex = (self.currentTeamIndex + 1) % len(self.teamNames)
            self.currentTeamName = self.teamNames[self.currentTeamIndex]

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
