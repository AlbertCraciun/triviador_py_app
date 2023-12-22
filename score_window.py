from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class ScoreWindow(QWidget):
    def __init__(self, mainApp, roundScores, totalScores):
        super().__init__()
        self.mainApp = mainApp
        self.roundScores = roundScores  # Scorurile pentru runda curentă
        self.totalScores = totalScores  # Scorurile totale
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Afișarea scorurilor
        for teamName, score in self.totalScores.items():
            # self.roundScore = self.calculateScores(teamAnswers, correctAnswer)
            label = QLabel(f"{teamName}: Runda: , Total: {score}")
            layout.addWidget(label)

        # Buton pentru continuare
        continueBtn = QPushButton('Continuă', self)
        continueBtn.clicked.connect(self.onContinue)
        layout.addWidget(continueBtn)

        self.setLayout(layout)
        self.setWindowTitle("Scoruri")
        self.setGeometry(300, 300, 400, 300)
        
    def calculateScores(self, teamAnswers, correctAnswer):
        # Calculul scorurilor în conformitate cu regulile specificate
        # teamAnswers este un dicționar cu formatul {teamName: answer}
        roundScores = {}
        for team, answer in teamAnswers.items():
            if answer == correctAnswer:
                if self.mainApp.currentTeamName == team:
                    # Echipa de rând cu răspuns corect
                    roundScores[team] = 40 if self.mainApp.randomQuestion else 20
                else:
                    # Celelalte echipe cu răspuns corect
                    roundScores[team] = 15 if self.mainApp.currentTeamName != team and self.mainApp.randomQuestion else 10
            else:
                # Răspuns greșit
                roundScores[team] = 0

        # Actualizarea scorurilor totale
        for team in self.mainApp.teamNames:
            self.totalScores[team] += roundScores.get(team, 0)

        return roundScores

    def onContinue(self):
        # Logică pentru trecerea la următorul ecran
        # De exemplu: revenire la ecranul de selecție a categoriilor sau încheierea jocului
        self.mainApp.nextTeam()
        self.mainApp.showNextScreen()
