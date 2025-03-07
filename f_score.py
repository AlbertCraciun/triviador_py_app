from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from g_duel_start import DuelTransitionWindow
from i_champion_start import ChampionTransitionWindow

class ScoreWindow(QWidget):
    def __init__(self, mainApp, roundAnswers, correctAnser, question):
        super().__init__()
        self.mainApp = mainApp
        self.roundAnswers = roundAnswers  # Răspunsurile pentru runda curentă
        self.correctAnser = correctAnser  # Răspunsul corect pentru runda curentă
        self.question = question  # Întrebarea curentă
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.initUI()

    def initUI(self):
        buttonWidth = 700
        layout = QVBoxLayout()
        
        roundScores = self.calculateScores(self.roundAnswers)
        
        # raspuns corect
        correctLayout = QHBoxLayout()
        correctLayout.addStretch()
        correctLabel = QLabel(f"Răspuns corect: {self.correctAnser}")
        correctLabel.setWordWrap(True)  # Activează împărțirea textului pe mai multe linii
        correctLabel.setAlignment(Qt.AlignCenter)
        correctLayout.addWidget(correctLabel)
        correctLayout.addStretch()
        layout.addLayout(correctLayout)

        if self.mainApp.roundType == 'classic' or self.mainApp.roundType == 'thief':
            for teamName in self.mainApp.teamNames:
                scoreLayout = QHBoxLayout()
                scoreLayout.addStretch()

                score = roundScores.get(teamName, 0)
                label = QLabel(f"Echipa {teamName}: Scor Runda: {score}, Total: {self.mainApp.totalScores[teamName]}")
                label.setAlignment(Qt.AlignCenter)
                scoreLayout.addWidget(label)

                scoreLayout.addStretch()
                layout.addLayout(scoreLayout)
        
        if self.mainApp.roundType == 'champion':
            for teamName in self.mainApp.championTeams:
                scoreLayout = QHBoxLayout()
                scoreLayout.addStretch()

                score = roundScores.get(teamName, 0)
                label = QLabel(f"Echipa {teamName}: Scor Runda: {score}, Total: {self.mainApp.championScores[teamName]}")
                label.setAlignment(Qt.AlignCenter)
                scoreLayout.addWidget(label)

                scoreLayout.addStretch()
                layout.addLayout(scoreLayout)

        # # Buton pentru continuare
        # continueBtnLayout = QHBoxLayout()
        # continueBtnLayout.addStretch()

        # continueBtn = QPushButton('Continuă', self)
        # continueBtn.setFixedWidth(buttonWidth)
        # continueBtn.clicked.connect(self.onContinue)
        # continueBtnLayout.addWidget(continueBtn, 0, Qt.AlignCenter)

        # continueBtnLayout.addStretch()
        # layout.addLayout(continueBtnLayout)
        
        # # Buton pentru corectare răspuns
        # correctAnswerBtnLayout = QHBoxLayout()
        # correctAnswerBtnLayout.addStretch()
        
        # self.correctAnswerBtn = QPushButton('Corectează Răspuns', self)
        # self.correctAnswerBtn.setFixedWidth(buttonWidth)
        # self.correctAnswerBtn.clicked.connect(self.openCorrectAnswerDialog)
        # correctAnswerBtnLayout.addWidget(self.correctAnswerBtn, 0, Qt.AlignCenter)
        
        # correctAnswerBtnLayout.addStretch()
        # layout.addLayout(correctAnswerBtnLayout)
        
        # Layout pentru butoane
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()

        # Buton pentru continuare
        continueBtn = QPushButton('Continuă', self)
        continueBtn.setFixedWidth(buttonWidth)
        continueBtn.clicked.connect(self.onContinue)
        buttonsLayout.addWidget(continueBtn, 0, Qt.AlignCenter)

        # # Buton pentru corectare răspuns
        # self.correctAnswerBtn = QPushButton('Corectează răspuns', self)
        # self.correctAnswerBtn.setFixedWidth(buttonWidth)
        # self.correctAnswerBtn.clicked.connect(self.openCorrectAnswerDialog)
        # buttonsLayout.addWidget(self.correctAnswerBtn, 0, Qt.AlignCenter)

        buttonsLayout.addStretch()

        # Adaugă layout-ul cu butoane la layout-ul principal
        layout.addLayout(buttonsLayout)
        
        # Crează un loc pentru grafice în layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Adăugă un spațiu elastic înainte de a adăuga graficul în layout pentru a împinge tot conținutul în sus
        layout.addStretch(1)

        # Actualizează graficul cu scoruri și desenează graficul
        self.updateGraph()
        self.canvas.draw()
            
        # Create a scroll area
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)  # Allow the content widget to resize with the scroll area
        scrollArea.setAlignment(Qt.AlignCenter)
        scrollArea.setFixedWidth(1680)
        scrollArea.setFixedHeight(1050)

        # Set the layout as the content of the scroll area
        scrollWidget = QWidget()
        scrollWidget.setLayout(layout)
        scrollArea.setWidget(scrollWidget)
        
        self.setWindowTitle("Scoruri")
        self.showFullScreen()
    
    # TODO: verify correct answer dialog
    def openCorrectAnswerDialog(self):
        # Dialog to select the correct answer
        dialog = QMessageBox(self)
        dialog.setWindowTitle('Selectează Răspunsul Corect')
        dialog.setText('Care este răspunsul corect?')
        
        # Assuming 'self.question' holds the current question data
        for i, option in enumerate(self.question['răspunsuri']):
            button = dialog.addButton(option, QMessageBox.AcceptRole)
            button.clicked.connect(lambda _, i=i: self.correctAnswer(i))
        
        dialog.exec_()

    def correctAnswer(self, correct_index):
        # Update the correct answer
        correct_answer = self.question['răspunsuri'][correct_index]
        self.question['răspuns corect'] = correct_answer
        
        # Re-calculate the scores based on the new correct answer
        roundScores = self.calculateScores(self.roundAnswers)
        
        # Update the cumulative scores with the new scores
        for team, score in roundScores.items():
            if self.mainApp.cumulativeScores[team]:
                # Înlocuiește ultimul scor cu noul scor corectat
                self.mainApp.cumulativeScores[team][-1] = self.mainApp.totalScores[team]
        
        # Update the score labels with new scores
        for teamName in self.mainApp.teamNames:
            scoreLabel = self.findChild(QLabel, f'score_{teamName}')
            if scoreLabel:
                score = roundScores.get(teamName, 0)
                scoreLabel.setText(f"{teamName}: Scor Runda: {score}, Total: {self.mainApp.totalScores[teamName]}")
        
        # Redraw the graph with the new scores
        self.updateGraph()

        
    def calculateScores(self, roundAnswers):
        
        if self.mainApp.roundType == 'classic':
            roundScores = {}
            for team, correct in roundAnswers.items():
                if correct:
                    # Scorul pentru răspuns corect
                    if self.mainApp.currentTeamName == team:
                        # Echipa de rând cu răspuns corect
                        score = 40 if self.mainApp.randomQuestion else 20
                    else:
                        # Celelalte echipe cu răspuns corect
                        if self.mainApp.currentTeamName is not None and self.mainApp.currentTeamName in roundAnswers:
                            score = 15 if not roundAnswers[self.mainApp.currentTeamName] else 10
                else:
                    # Scorul pentru răspuns greșit
                    score = 0
                roundScores[team] = score
                self.mainApp.totalScores[team] += score  # Actualizăm scorul total
            return roundScores
        
        elif self.mainApp.roundType == 'thief':
            
            attackingTeam = self.mainApp.currentTeamName
            defendingTeam = self.mainApp.selectedOpponent

            roundScores = {}
            for team, correct in roundAnswers.items():
                if team not in [attackingTeam, defendingTeam]:
                    # Pentru restul echipelor care nu sunt în duel
                    score = 5 if correct else 0
                elif team == attackingTeam:
                    # Echipa care atacă
                    if correct:
                        # Dacă echipa care atacă a răspuns corect
                        if roundAnswers.get(defendingTeam) == False:
                            # Și echipa apărată a răspuns greșit
                            score = 20
                        else:
                            # Ambii participanți au răspuns corect, deci se inițiază departajarea
                            QMessageBox.warning(self, 'Eroare', 'Ambele echipe au răspuns corect si nu s-a tratat cazul!')
                    else:
                        # Echipa care atacă a răspuns greșit
                        score = 0
                elif team == defendingTeam:
                    # Echipa care este apărată
                    if correct:
                        # Dacă echipa apărată a răspuns corect
                        score = 10
                    else:
                        # Echipa apărată a răspuns greșit
                        if roundAnswers.get(attackingTeam) == False:
                            # Dacă echipa care atacă a răspuns și ea greșit
                            score = 0  # Echipa apărată nu pierde puncte
                        else:
                            # Echipa apărată a răspuns greșit și echipa care atacă a răspuns corect
                            score = -20  # Pierde 20 de puncte

                roundScores[team] = score
                self.mainApp.totalScores[team] += score  # Actualizăm scorul total

            return roundScores
    
        elif self.mainApp.roundType == 'champion':
            roundScores = {}
            for team, correct in roundAnswers.items():
                if correct:
                    score = 50
                else:
                    score = 0
                roundScores[team] = score
                self.mainApp.championScores[team] += score  # Actualizăm scorul total
            return roundScores
    
        else:
            QMessageBox.critical(None, "Eroare", "Runda curentă nu este validă!")
            return None

    def updateGraph(self):
        ax = self.ax
        
        # Inițializăm un dicționar pentru a stoca scorurile pentru fiecare echipă
        if not hasattr(self.mainApp, 'cumulativeScores'):
            self.mainApp.cumulativeScores = {team: [0] for team in self.mainApp.teamNames}

        print("\nScoruri totale:")
        print(self.mainApp.cumulativeScores)
        
        # Adaugă scorurile actuale la scorurile cumulative
        for team in self.mainApp.teamNames:
            if team not in self.mainApp.cumulativeScores or not isinstance(self.mainApp.cumulativeScores[team], list):
                self.mainApp.cumulativeScores[team] = [0]
            self.mainApp.cumulativeScores[team].append(self.mainApp.totalScores[team])

        ax.clear()

        # Setează intervale pentru axa X (numere întregi) și axa Y (multiplii de 5)
        max_rounds = max(len(scores) for scores in self.mainApp.cumulativeScores.values())
        max_score = max(max(scores) for scores in self.mainApp.cumulativeScores.values())
        ax.set_xticks(range(max_rounds))
        ax.set_yticks(range(0, max_score + 1, 5))

        # Desenăm liniile pentru fiecare echipă
        for team, scores in self.mainApp.cumulativeScores.items():
            rounds = list(range(len(scores)))
            ax.plot(rounds, scores, label=team)

        # Adaugă linii punctate pe grafic
        ax.grid(which='both', linestyle='--', linewidth=0.5, color='grey')

        # Activează doar liniile grid pentru axa Y
        ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, color='grey')
        ax.grid(True, which='major', axis='x', linestyle='--', linewidth=0.5, color='grey')

        ax.set_title("Evoluția scorurilor pe echipe")
        ax.set_xlabel("Runde")
        ax.set_ylabel("Scoruri totale")
        ax.legend()  # Adăugarea legendei

        self.canvas.draw()

    
    def onContinue(self):
        self.close()  # Închidem fereastra curentă de scoruri
        
        # Verificăm ce tip de rundă este și dacă mai sunt runde rămase
        if self.mainApp.roundType == 'classic':
            if self.mainApp.numClassicRounds > 0:
                # Dacă mai sunt runde clasice, afișăm ecranul de selecție categorie
                print('A. Score - branch classic - numClassicRounds > 0')
                self.mainApp.showNextScreen()
            elif self.mainApp.numThiefRounds > 0:
                # Dacă s-au terminat rundele clasice, dar mai sunt runde de duel
                self.mainApp.roundType = 'thief'  # Schimbăm tipul rundei în 'thief'
                self.mainApp.duelTransitionWindow = DuelTransitionWindow(self.mainApp)
                print('B. Score - branch classic - numThiefRounds > 0')
                self.mainApp.duelTransitionWindow.show()  # Afișăm ecranul de tranziție către duel
            elif self.mainApp.numChampionRounds > 0:
                # Dacă nu mai sunt nici runde clasice, nici de duel, dar sunt runde de campioni
                self.mainApp.roundType = 'champion'  # Schimbăm tipul rundei în 'champion'
                print('C. Score - branch classic - numChampionRounds > 0')
                self.mainApp.championTransitionWindow = ChampionTransitionWindow(self.mainApp)
                self.mainApp.championTransitionWindow.show()  # Afișăm ecranul de tranziție către campioni
            else:
                # Dacă nu mai sunt runde de niciun tip, jocul se termină
                print('D. Score - branch classic - END GAME')
                self.mainApp.endGame()

        elif self.mainApp.roundType == 'thief':
            if self.mainApp.numThiefRounds > 0:
                # Dacă mai sunt runde de duel, continuăm cu duelurile
                print('E. Score - branch thief - numThiefRounds > 0')
                self.mainApp.showNextScreen()
            elif self.mainApp.numChampionRounds > 0:
                # Dacă s-au terminat rundele de duel, dar sunt runde de campioni
                print('F. Score - branch thief - numChampionRounds > 0')
                self.mainApp.roundType = 'champion'
                self.mainApp.championTransitionWindow = ChampionTransitionWindow(self.mainApp)
                self.mainApp.championTransitionWindow.show()
            else:
                # Dacă nu mai sunt runde de duel sau campioni, jocul se termină
                print('G. Score - branch thief - END GAME')
                self.mainApp.endGame()

        elif self.mainApp.roundType == 'champion':
            if self.mainApp.numChampionRounds > 0:
                # Dacă mai sunt runde de campioni, continuăm cu acestea
                print('H. Score - branch champion - numChampionRounds > 0')
                self.mainApp.showNextScreen()
            else:
                # Dacă nu mai sunt runde de campioni, jocul se termină
                print('I. Score - branch champion - END GAME')
                self.mainApp.endGame()

