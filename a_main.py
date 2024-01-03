from datetime import datetime
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from d_selection import CategorySelectionWindow
from b_questions_loader import load_questions_from_excel

from c_start_window import StartWindow
from j_end_game import EndGameWindow

class MainApp(QApplication):
        
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        
        self.categorySelectionWindow = None
        self.duelTransitionWindow = None
        self.championTransitionWindow = None
        
        # Inițializarea calei fișierului de log
        self.logFilePath = "game_log.txt"  # Asumăm că fișierul de log este în același director
        
        self.teamNames = []
        self.timerDuration = 30
        self.selectionTime = 30
        self.numClassicRounds = 0
        self.numThiefRounds = 0
        self.numChampionRounds = 0
        self.tempNumClassicRounds = 0
        self.tempNumThiefRounds = 0
        self.tempNumChampionRounds = 0
        self.startWindow = StartWindow(self)
        self.startWindow.show()
        self.championRoundsEnabled = False
        
        # Ajustați dimensiunile elementelor și fonturile
        self.buttonWidth = 700
        self.buttonHeight = 50
        self.backgroundColour = "black"
        # self.buttonColour = "#444"
        self.buttonColour = "black"
        self.buttonBorderColour = "#555"
        self.fontSize = 50
        self.fontColour = "white"
        self.fontFamily = "Arial"
        self.backgroundImage = "background triviador.png";
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.backgroundColour};
                color: {self.fontColour};
                font-family: {self.fontFamily};
                font-size: {self.fontSize}px;
            }}
            QLabel {{
                font-size: {self.fontSize}px;
                text-align: center;
            }}
            QPushButton {{
                background-color: {self.buttonColour};
                border: 2px solid {self.buttonBorderColour};
                border-radius: 10px;
                padding: 5px;
                font-size: {self.fontSize}px;
                min-height: {self.buttonHeight}px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: #666;
            }}
            QLineEdit {{
                border: 1px solid {self.buttonBorderColour};
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }}
            # QSpinBox {{
            #     border: 1px solid {self.buttonBorderColour};
            #     border-radius: 5px;
            #     padding: 5px;
            #     margin: 5px;
            # }}
            QCheckBox {{
                spacing: 100px;
            }}
            QComboBox {{
                border: 1px solid {self.buttonBorderColour};
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }}
        """)
        
        self.currentRound = 0

        self.currentTeamIndex = -1
        self.currentTeamName = self.teamNames[self.currentTeamIndex] if self.teamNames else None
        
        self.categories = set()
        self.questions = []
        self.selected_question = []
        self.selected_tiebreaker_question = []
        
        self.randomQuestion = False
        self.roundType = "classic"
        self.selectedOpponent = None
        self.selectedCategory = None
        
        # Inițializăm dicționare pentru contorizari
        self.tiebreakerCounts = {}
        self.totalQuestionCount = {}
        self.correctAnswersCount = {}
        self.championScores = {}
        self.totalScores = {}
        self.cumulativeScores = {}
        self.championTeams = []  # Echipele care participă la rundele de campioni

    def start_from_intermediate_state(self, intermediate_state_file):
            if intermediate_state_file:
                self.load_intermediate_state(intermediate_state_file)
                self.showNextScreen()
    
    def showNextScreen(self):
        
        #self.updateLog()
        
        if self.duelTransitionWindow is not None:
            self.duelTransitionWindow.close()
            self.duelTransitionWindow = None
            
        if self.championTransitionWindow is not None:
            self.championTransitionWindow.close()
            self.championTransitionWindow = None

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
        # Scrierea scorurilor în fișier
        self.saveScoresToFile()

        # Afișarea ferestrei de final de joc
        self.endGameWindow = EndGameWindow(self)
        self.endGameWindow.show()
        
    def saveScoresToFile(self):
        filename = f"scoruri_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('Scoruri finale\n')
            file.write(f'Runde clasice: {self.tempNumClassicRounds}\n')
            file.write(f'Runde de duel: {self.tempNumThiefRounds}\n')
            file.write(f'Runde de campioni: {self.tempNumChampionRounds}\n')
            file.write('-------------------\n')

             # Sortăm echipele mai întâi după scorurile de campioni (daca există) și apoi după scorurile totale
            sorted_teams = sorted(self.totalScores.keys(), key=lambda t: (self.championScores[t] > 0, self.totalScores[t]), reverse=True)

            for team in sorted_teams:
                score = self.totalScores[team]
                totalQuestions = self.totalQuestionCount[team]
                correctAnswers = self.correctAnswersCount[team]
                tiebreakerQuestions = self.tiebreakerCounts[team]
                championScore = self.championScores[team]

                file.write(f'Echipa: {team}\n')
                file.write(f'Scor: {score}\n')
                file.write(f'Champion score: {championScore}\n')
                file.write(f'Număr total întrebări: {totalQuestions}\n')
                file.write(f'Răspunsuri corecte: {correctAnswers}\n')
                file.write(f'Întrebări de departajare: {tiebreakerQuestions}\n')
                file.write('-------------------\n')
            
            # pune toate intrebarile utilizate in fisier
            file.write('Întrebări utilizate\n')
            for question in self.selected_question:
                file.write(f'{question}\n')
            for question in self.selected_tiebreaker_question:
                file.write(f'{question}\n')

            file.write('Joc terminat.\n')

        print(f"Scorurile au fost salvate în fișierul: {filename}")

    def updateLog(self):
        with open(self.logFilePath, 'w', encoding='utf-8') as file:
            file.write('Scoruri și întrebări până în prezent\n')
            file.write('-------------------\n')
            # Scrie scorurile și întrebările
            for team in sorted(self.totalScores.keys(), key=lambda t: (self.championScores[t] > 0, self.totalScores[t]), reverse=True):
                score = self.totalScores[team]
                totalQuestions = self.totalQuestionCount[team]
                correctAnswers = self.correctAnswersCount[team]
                tiebreakerQuestions = self.tiebreakerCounts[team]
                championScore = self.championScores[team]

                file.write(f'Echipa: {team}\n')
                file.write(f'Scor: {score}\n')
                file.write(f'Champion score: {championScore}\n')
                file.write(f'Număr total întrebări: {totalQuestions}\n')
                file.write(f'Răspunsuri corecte: {correctAnswers}\n')
                file.write(f'Întrebări de departajare: {tiebreakerQuestions}\n')
                file.write('-------------------\n')

            file.write('Întrebări utilizate până în prezent\n')
            for question in self.selected_question:
                file.write(f'{question}\n')
            for question in self.selected_tiebreaker_question:
                file.write(f'{question}\n')
    
    def load_intermediate_state(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # Inițializați mai întâi lista de echipe
            self.teamNames = []
            for line in lines:
                if ":" in line:  # Simplifică căutarea pentru linii care conțin ':'
                    key, value = line.strip().split(":", 1)
                    if key == 'Runda curentă':
                        self.roundType = value.strip().lower()
                    elif key == 'Runde clasice rămase':
                        self.numClassicRounds = int(value.strip())
                    elif key == 'Runde de duel rămase':
                        self.numThiefRounds = int(value.strip())
                    elif key == 'Runde de campioni rămase':
                        self.numChampionRounds = int(value.strip())
                    elif key == 'Echipa de rând':
                        self.currentTeamName = value.strip()
                    else:  # Presupunem că orice altceva este o echipă
                        team_name = key.strip()
                        score = int(value.strip())
                        self.teamNames.append(team_name)
                        self.totalScores[team_name] = score
                        self.tiebreakerCounts[team_name] = 0
                        self.totalQuestionCount[team_name] = 0
                        self.correctAnswersCount[team_name] = 0
                        self.championScores[team_name] = 0

            # Acum că avem lista de echipe, putem seta indexul echipei curente
            if self.currentTeamName in self.teamNames:
                self.currentTeamIndex = self.teamNames.index(self.currentTeamName)
            else:
                raise ValueError(f"Echipa curentă '{self.currentTeamName}' nu este în lista de echipe încărcată.")


if __name__ == '__main__':
    app = MainApp(sys.argv)
    if len(sys.argv) > 2:
        intermediate_state_file = sys.argv[1]
        question_file = sys.argv[2]
        app.loadQuestions(question_file)
        app.start_from_intermediate_state(intermediate_state_file)
    else:
        app.startWindow.showFullScreen()
    sys.exit(app.exec_())
