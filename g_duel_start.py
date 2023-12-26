from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class DuelTransitionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.initUI()

    def initUI(self):
        buttonWidth = 700
        layout = QVBoxLayout()
        layout.addStretch()  # Adaugă spațiu pentru centrare verticală

        # Titlul pentru fereastra duelului
        titleLabelLayout = QHBoxLayout()
        titleLabelLayout.addStretch()
        titleLabel = QLabel("Runde Duel")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabelLayout.addWidget(titleLabel)
        titleLabelLayout.addStretch()
        layout.addLayout(titleLabelLayout)

        # Afișarea scorurilor
        scoresLayout = QVBoxLayout()  # Dacă scorurile sunt într-o coloană, altfel folosiți QHBoxLayout
        for team, score in sorted(self.mainApp.totalScores.items(), key=lambda item: item[1], reverse=True):
            scoreLabelLayout = QHBoxLayout()
            scoreLabelLayout.addStretch()
            scoreLabel = QLabel(f"{team}: {score} puncte")
            scoreLabel.setAlignment(Qt.AlignCenter)
            scoreLabelLayout.addWidget(scoreLabel)
            scoreLabelLayout.addStretch()
            scoresLayout.addLayout(scoreLabelLayout)
        layout.addLayout(scoresLayout)

        # Butonul pentru începerea duelului
        startDuelButtonLayout = QHBoxLayout()
        startDuelButtonLayout.addStretch()
        startDuelButton = QPushButton("Începe Duelul")
        startDuelButton.setFixedWidth(buttonWidth)
        startDuelButton.clicked.connect(self.mainApp.showNextScreen)
        startDuelButtonLayout.addWidget(startDuelButton, 0, Qt.AlignCenter)
        startDuelButtonLayout.addStretch()
        layout.addLayout(startDuelButtonLayout)

        layout.addStretch()  # Adaugă spațiu pentru centrare verticală
        self.setLayout(layout)
        self.setWindowTitle("Tranziție Runde Duel")
        self.showFullScreen()
