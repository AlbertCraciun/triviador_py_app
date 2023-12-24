from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class DuelTransitionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch()  # Adaugă spațiu pentru centrare verticală

        titleLabel = QLabel("Runde Duel")
        titleLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titleLabel)

        # Afișarea scorurilor
        for team, score in sorted(self.mainApp.totalScores.items(), key=lambda item: item[1], reverse=True):
            scoreLabel = QLabel(f"{team}: {score} puncte")
            scoreLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(scoreLabel)

        startDuelButton = QPushButton("Începe Duelul")
        startDuelButton.clicked.connect(self.mainApp.startDuel)
        layout.addWidget(startDuelButton, 0, Qt.AlignCenter)

        layout.addStretch()  # Adaugă spațiu pentru centrare verticală
        self.setLayout(layout)
        self.setWindowTitle("Tranziție Runde Duel")
        self.setGeometry(300, 300, 400, 300)
