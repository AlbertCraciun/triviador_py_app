from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class ScoreWindow(QWidget):
    def __init__(self, mainApp, roundAnswers):
        super().__init__()
        self.mainApp = mainApp
        self.roundAnswers = roundAnswers  # Răspunsurile pentru runda curentă
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Calculăm scorurile pentru runda curentă
        roundScores = self.calculateScores(self.roundAnswers)

        # Afișarea scorurilor
        for teamName in self.mainApp.teamNames:
            score = roundScores.get(teamName, 0)
            label = QLabel(f"{teamName}: Scor Runda: {score}, Total: {self.mainApp.totalScores[teamName]}")
            layout.addWidget(label)

        # Buton pentru continuare
        continueBtn = QPushButton('Continuă', self)
        continueBtn.clicked.connect(self.onContinue)
        layout.addWidget(continueBtn)

        self.setLayout(layout)
        self.setWindowTitle("Scoruri")
        self.setGeometry(300, 300, 400, 300)
        
    def calculateScores(self, roundAnswers):
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

    def onContinue(self):
        # Logică pentru trecerea la următorul ecran
        # De exemplu: revenire la ecranul de selecție a categoriilor sau încheierea jocului
        self.hide()
        self.mainApp.showNextScreen()
