from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QHBoxLayout, QButtonGroup
from PyQt5.QtCore import QTimer, Qt

from f_score_window import ScoreWindow

class QuestionWindow(QWidget):
    def __init__(self, mainApp, question, teams):
        super().__init__()
        self.mainApp = mainApp
        self.question = question
        self.teams = teams  # Lista de echipe
        self.teamAnswersWidgets = []  # Pentru stocarea widgeturilor specifice fiecărei echipe
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Adaugă un spațiu înainte de widgeturi pentru a le împinge în jos
        layout.addStretch()

        # Afișarea echipei de rând
        currentTeamLabel = QLabel(f"Rândul echipei: {self.mainApp.currentTeamName}")
        currentTeamLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(currentTeamLabel)

        # Afișarea întrebării
        questionLabel = QLabel(self.question['întrebare'])
        questionLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(questionLabel)

        # Afișarea variantelor de răspuns cu litere
        self.labels = []
        self.answerMapping = {}
        letters = ['A', 'B', 'C', 'D']
        for i, answer in enumerate(self.question['răspunsuri']):
            label_text = f"{letters[i]}. {answer}"
            text = QLabel(label_text)
            text.setAlignment(Qt.AlignCenter)
            self.labels.append(text)
            layout.addWidget(text)
            self.answerMapping[letters[i]] = answer

        # Timer
        self.timer = QLabel(f"Timp rămas: {self.mainApp.timerDuration} secunde")
        self.timer.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer)
        self.startTimer()

        # Răspunsuri echipe
        for team in self.teams:
            teamLabel = QLabel(f"Răspunsuri echipa {team}")
            teamLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(teamLabel)

            teamAnswerLayout = QHBoxLayout()
            teamAnswerLayout.addStretch()
            teamRadioButtonGroup = QButtonGroup(self)
            for option in letters:
                radioButton = QRadioButton(option)
                teamAnswerLayout.addWidget(radioButton)
                teamRadioButtonGroup.addButton(radioButton)
            teamAnswerLayout.addStretch()

            self.teamAnswersWidgets.append((team, teamRadioButtonGroup))
            layout.addLayout(teamAnswerLayout)

       # Creare QHBoxLayout pentru alinierea butonului de verificare pe orizontală
        answerButtonLayout = QHBoxLayout()
        answerButtonLayout.addStretch()  # Adaugă un spațiu elastic înainte de buton pentru a-l împinge către centru

        # Adăugare buton de verificare răspunsuri în layout-ul orizontal
        self.answerButton = QPushButton("Verifică răspunsurile", self)
        self.answerButton.setFixedWidth(300)
        self.answerButton.clicked.connect(self.checkTeamAnswers)
        answerButtonLayout.addWidget(self.answerButton, 0, Qt.AlignCenter)  # Aliniază butonul pe centrul orizontal

        answerButtonLayout.addStretch()  # Adaugă un spațiu elastic după buton pentru a menține centrarea
        layout.addLayout(answerButtonLayout)  # Adaugă layout-ul orizontal în layout-ul vertical principal

        # Adaugă un spațiu după widgeturi pentru a le centra
        layout.addStretch()

        self.setLayout(layout)
        self.setWindowTitle("Întrebarea")
        self.setGeometry(300, 300, 400, 300)

    def startTimer(self):
        self.countdown = self.mainApp.timerDuration
        self.timerQTimer = QTimer(self)
        self.timerQTimer.timeout.connect(self.updateTimer)
        self.timerQTimer.start(1000)

    def updateTimer(self):
        self.countdown -= 1
        self.timer.setText(f"Timp rămas: {self.countdown} secunde")
        if self.countdown <= 0:
            self.timerQTimer.stop()
            self.hideInitialAnswers()
            
    def hideInitialAnswers(self):
        for label in self.labels:
            label.setVisible(False)

    def checkTeamAnswers(self):
        self.timerQTimer.stop()
        self.hideInitialAnswers()
        roundAns = {}
        for team, teamRadioButtonGroup in self.teamAnswersWidgets:
            selectedButton = teamRadioButtonGroup.checkedButton()
            if selectedButton:
                selectedLetter = selectedButton.text()
                selectedAnswer = self.answerMapping[selectedLetter]
                correct = selectedAnswer == self.question['răspuns corect']
                roundAns[team] = correct
        
        # Afișăm scorurile
        self.scoreWindow = ScoreWindow(self.mainApp, roundAns)
        self.hide()
        self.scoreWindow.show()
