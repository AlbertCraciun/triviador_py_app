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
            roundScore = self.roundScores.get(teamName, 0)
            label = QLabel(f"{teamName}: Runda: {roundScore}, Total: {score}")
            layout.addWidget(label)

        # Buton pentru continuare
        continueBtn = QPushButton('Continuă', self)
        continueBtn.clicked.connect(self.onContinue)
        layout.addWidget(continueBtn)

        self.setLayout(layout)
        self.setWindowTitle("Scoruri")
        self.setGeometry(300, 300, 400, 300)

    def onContinue(self):
        # Logică pentru trecerea la următorul ecran
        # De exemplu: revenire la ecranul de selecție a categoriilor sau încheierea jocului
        self.mainApp.showNextScreen()
