import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from d_selection import CategorySelectionWindow
from g_duel_start import DuelTransitionWindow
from b_questions_loader import load_questions_from_excel

from c_start_window import StartWindow

class MainApp(QApplication):
        
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        
        self.categorySelectionWindow = None
        self.duelTransitionWindow = None
        
        self.teamNames = []
        self.timerDuration = 30
        self.selectionTime = 30
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
        
        self.categories = set()
        self.questions = []
        self.selected_question = []
        
        self.randomQuestion = False
        self.totalScores = {}
        self.roundType = "classic"
        self.selectedOpponent = None
        self.selectedCategory = None

    def showNextScreen(self):

        if self.teamNames:
            self.randomQuestion = False
            self.currentTeamIndex = (self.currentTeamIndex + 1) % len(self.teamNames)
            self.currentTeamName = self.teamNames[self.currentTeamIndex]
                
            if self.roundType == "classic":
                self.numClassicRounds -= 1
                print("\n--Echipa curentă: ", self.currentTeamName, "\nRunda curentă: ", self.roundType, "\nRunde clasice rămase: ", self.numClassicRounds, "\nRunde de duel rămase: ", self.numThiefRounds, "\nRunde de campioni rămase: ", self.numChampionRounds)
                self.categorySelectionWindow = CategorySelectionWindow(self)
                self.categorySelectionWindow.show() # Afișăm fereastra de selecție a categoriilor
            elif self.roundType == "thief":
                self.numThiefRounds -= 1
                print("\n--Echipa curentă: ", self.currentTeamName, "\nRunda curentă: ", self.roundType, "\nRunde clasice rămase: ", self.numClassicRounds, "\nRunde de duel rămase: ", self.numThiefRounds, "\nRunde de campioni rămase: ", self.numChampionRounds)
                self.categorySelectionWindow = CategorySelectionWindow(self)
                self.categorySelectionWindow.show() # Afișăm fereastra de selecție a categoriilor
            elif self.roundType == "champion":
                self.numChampionRounds -= 1
                print("\n--Echipa curentă: ", self.currentTeamName, "\nRunda curentă: ", self.roundType, "\nRunde clasice rămase: ", self.numClassicRounds, "\nRunde de duel rămase: ", self.numThiefRounds, "\nRunde de campioni rămase: ", self.numChampionRounds)
                self.categorySelectionWindow = CategorySelectionWindow(self)
                self.categorySelectionWindow.show()
            else:
                QMessageBox.critical(None, "Eroare", "Runda curentă nu este validă!")
                
        else:
            QMessageBox.critical(None, "Eroare", "Nu există echipe!")
            print("Nu există echipe!")
    
    def loadQuestions(self, filePath):
        # Încărcați întrebările din fișierul Excel specificat
        self.questions = load_questions_from_excel(filePath)
        
    def endGame(self):
        # Afișează un mesaj de felicitare sau un ecran final
        QMessageBox.information(None, "Joc Terminat", "Felicitări tuturor echipelor pentru participare!")
        self.quit()  # Încheie aplicația

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
