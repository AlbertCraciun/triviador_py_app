from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

class EndGameWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Titlu
        title = QLabel('Joc Terminat')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Determinarea câștigătorului și a scorului său
        winner, highestScore = max(self.mainApp.totalScores.items(), key=lambda item: item[1])
        correctAnswersCount = self.mainApp.correctAnswersCount[winner]
        totalQuestions = self.mainApp.totalQuestionCount[winner]

        # Afișarea detaliilor câștigătorului
        winnerDetails = QLabel(f'Câștigător: {winner}\nScor (runde clasice & duel): {highestScore}\nScorul rundelor campionilor: {self.mainApp.championScores[winner]}\n{correctAnswersCount}/{totalQuestions} răspunsuri corecte la întrebările cu variante\nÎntrebări de departajare: {self.mainApp.tiebreakerCounts[winner]}')
        winnerDetails.setAlignment(Qt.AlignCenter)
        layout.addWidget(winnerDetails)

        # # Afișarea detaliilor pentru toate echipele
        # for team, score in sorted(self.mainApp.totalScores.items(), key=lambda item: item[1], reverse=True):
        #     teamDetails = QLabel(f'Echipa: {team}\nScor: {score}\n{self.mainApp.correctAnswersCount[team]}/{self.mainApp.totalQuestionCount[team]} răspunsuri corecte\nÎntrebări de departajare: {self.mainApp.tieBreakerQuestions}')
        #     teamDetails.setAlignment(Qt.AlignCenter)
        #     layout.addWidget(teamDetails)

        # Buton de închidere
        closeButton = QPushButton('Închide', self)
        closeButton.setFixedWidth(300)
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton, 0, Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('Final de Joc')
        self.setGeometry(300, 300, 400, 300)

    def closeEvent(self, event):
        # Confirmare înainte de închidere
        reply = QMessageBox.question(self, 'Confirmare', 'Ești sigur că vrei să închizi jocul?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        self.mainApp.quit()  # Închide întreaga aplicație atunci când se închide fereastra