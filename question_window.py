from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QHBoxLayout, QButtonGroup
from PyQt5.QtCore import QTimer

from score_window import ScoreWindow

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
        
        # Afișarea echipei de rând
        currentTeamLabel = QLabel(f"Rândul echipei: {self.mainApp.currentTeamName}")
        layout.addWidget(currentTeamLabel)

        # Afișarea întrebării
        questionLabel = QLabel(self.question['întrebare'])  # Folosim textul întrebării
        layout.addWidget(questionLabel)

        # Afișarea variantelor de răspuns cu litere
        self.labels = []
        self.answerMapping = {}  # Dicționar pentru a asocia răspunsurile cu litere
        letters = ['A', 'B', 'C', 'D']
        for i, answer in enumerate(self.question['răspunsuri']):
            label_text = f"{letters[i]}. {answer}"
            text = QLabel(label_text)
            self.labels.append(text)
            layout.addWidget(text)
            self.answerMapping[letters[i]] = answer
        
        # Timer
        self.timer = QLabel("Timp rămas: " + str(self.mainApp.timerDuration) + " secunde", self)
        layout.addWidget(self.timer)
        self.startTimer()
        
        for team in self.teams:
            teamLabel = QLabel(f"Răspunsuri pentru echipa {team}")
            layout.addWidget(teamLabel)

            teamAnswerLayout = QHBoxLayout()
            teamRadioButtonGroup = QButtonGroup(self)
            for option in letters:
                radioButton = QRadioButton(option)
                teamAnswerLayout.addWidget(radioButton)
                teamRadioButtonGroup.addButton(radioButton)

            self.teamAnswersWidgets.append((team, teamRadioButtonGroup))
            layout.addLayout(teamAnswerLayout)
        
        self.answerButton = QPushButton("Verifică Răspunsurile", self)
        self.answerButton.clicked.connect(self.checkTeamAnswers)
        layout.addWidget(self.answerButton)

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
