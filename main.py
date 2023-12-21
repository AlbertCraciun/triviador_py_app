import sys
from PyQt5.QtWidgets import QApplication
from category_selection_screen import CategorySelectionWindow
from game_config_screen import GameConfigWindow
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

    def showNextScreen(self):
        self.categorySelectionWindow = CategorySelectionWindow(self)
        self.startWindow.hide()  # Ascundem fereastra de start
        self.categorySelectionWindow.show()  # Afișăm fereastra de selecție a categoriilor
        
    def showQuestionScreen(self, question, answers):
        self.questionWindow = QuestionWindow(self, question, answers, teams=self.teamNames)
        self.questionWindow.show()

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
