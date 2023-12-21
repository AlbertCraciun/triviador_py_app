from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QRadioButton, QPushButton, QHBoxLayout, QButtonGroup
from PyQt5.QtCore import QTimer

from score_window import ScoreWindow

class QuestionWindow(QWidget):
    def __init__(self, mainApp, question, answers, teams):
        super().__init__()
        self.mainApp = mainApp
        self.question = question
        self.answers = answers
        self.teams = teams  # Lista de echipe
        self.teamAnswersWidgets = []  # Pentru stocarea widgeturilor specifice fiecărei echipe
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Afișarea întrebării
        questionLabel = QLabel(self.question)
        layout.addWidget(questionLabel)

        # Afișarea variantelor de răspuns
        self.radioButtons = []
        for answer in self.answers:
            radioButton = QRadioButton(answer)
            self.radioButtons.append(radioButton)
            layout.addWidget(radioButton)

        # Timer
        self.timer = QLabel("Timp rămas: " + str(self.mainApp.timerDuration) + " secunde", self)
        layout.addWidget(self.timer)
        self.startTimer()
        
        self.answerButton = QPushButton("Verifică Răspunsurile", self)
        self.answerButton.clicked.connect(self.checkTeamAnswers)
        self.answerButton.hide()  # Inițial butonul este ascuns
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
            self.showTeamAnswerOptions()
            
    def hideInitialAnswers(self):
        for radioButton in self.radioButtons:
            radioButton.hide()  # Ascunde răspunsurile inițiale

    def showTeamAnswerOptions(self):
        layout = self.layout()

        for team in self.teams:
            teamLabel = QLabel(f"Răspunsuri pentru echipa {team}")
            layout.addWidget(teamLabel)

            teamAnswerLayout = QHBoxLayout()
            teamRadioButtonGroup = QButtonGroup(self)
            for option in ['A', 'B', 'C', 'D']:
                radioButton = QRadioButton(option)
                teamAnswerLayout.addWidget(radioButton)
                teamRadioButtonGroup.addButton(radioButton)

            self.teamAnswersWidgets.append((team, teamRadioButtonGroup))
            layout.addLayout(teamAnswerLayout)

        self.answerButton.show()  # Afișează butonul pentru verificarea răspunsurilor

    def checkTeamAnswers(self):
        for team, radioButtonGroup in self.teamAnswersWidgets:
            selectedButton = radioButtonGroup.checkedButton()
            if selectedButton:
                selectedAnswer = selectedButton.text()
                # Aici poți adăuga logica pentru evaluarea răspunsurilor fiecărei echipe
                print(f"Echipa {team} a ales răspunsul {selectedAnswer}")
        
        # Afișăm scorurile
        self.scoreWindow = ScoreWindow(self.mainApp, roundScores={"Echipa 1": 10, "Echipa 2": 20}, totalScores={"Echipa 1": 10, "Echipa 2": 20})
        self.hide()
        self.scoreWindow.show()
