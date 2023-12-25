from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class ChampionTransitionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch()  # Pentru centrare verticală

        # Titlul ferestrei
        titleLabelLayout = QHBoxLayout()
        titleLabelLayout.addStretch()
        titleLabel = QLabel("Tranziție Runde Campioni")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabelLayout.addWidget(titleLabel)
        titleLabelLayout.addStretch()
        layout.addLayout(titleLabelLayout)

        # Afișarea scorurilor din rundele anterioare
        scoresLayout = QVBoxLayout()  # Se folosește QVBoxLayout pentru a afișa scorurile în coloană
        for team, score in sorted(self.mainApp.totalScores.items(), key=lambda item: item[1], reverse=True):
            scoreLabelLayout = QHBoxLayout()
            scoreLabelLayout.addStretch()
            scoreLabel = QLabel(f"{team}: {score} puncte")
            scoreLabel.setAlignment(Qt.AlignCenter)
            scoreLabelLayout.addWidget(scoreLabel)
            scoreLabelLayout.addStretch()
            scoresLayout.addLayout(scoreLabelLayout)
        layout.addLayout(scoresLayout)

        # Butonul pentru începerea rundelor de campioni
        startChampionButtonLayout = QHBoxLayout()
        startChampionButtonLayout.addStretch()
        startChampionButton = QPushButton("Începe rundele campionilor")
        startChampionButton.setFixedWidth(300)
        startChampionButton.clicked.connect(self.startChampionRounds)
        startChampionButtonLayout.addWidget(startChampionButton, 0, Qt.AlignCenter)
        startChampionButtonLayout.addStretch()
        layout.addLayout(startChampionButtonLayout)

        layout.addStretch()  # Pentru centrare verticală
        self.setLayout(layout)
        self.setWindowTitle("Tranziție către Rundele Campionilor")
        self.showFullScreen()

    def startChampionRounds(self):
        self.mainApp.timerDuration -= 5  # Reducem timpul pe întrebare cu 5 secunde
        self.mainApp.selectionTime = 1 # Se alege un răspuns în 1 secundă
        self.mainApp.championTeams = sorted(self.mainApp.totalScores.keys(), key=lambda team: self.mainApp.totalScores[team], reverse=True)[:2]  # Se aleg primele două echipe din clasament
        print(self.mainApp.championTeams)
        self.mainApp.championScores[self.mainApp.championTeams[0]] += 50  # Primul loc începe cu un bonus de 50 puncte

        # Închiderea ferestrei de tranziție și afișarea primei întrebări pentru rundele de campioni
        self.close()
        self.mainApp.showNextScreen()
