from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class DuelTransitionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        titleLabel = QLabel("Runde Duel")
        layout.addWidget(titleLabel)

        for team, score in self.mainApp.totalScores.items():
            scoreLabel = QLabel(f"{team}: {score} puncte")
            layout.addWidget(scoreLabel)

        startDuelButton = QPushButton("Începe Duelul")
        startDuelButton.clicked.connect(self.mainApp.startDuel)
        layout.addWidget(startDuelButton)

        self.setLayout(layout)
        self.setWindowTitle("Tranziție Runde Duel")
        self.setGeometry(300, 300, 400, 300)

    # Implementează restul funcționalităților necesare
