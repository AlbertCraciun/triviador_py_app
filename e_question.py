from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QHBoxLayout, QButtonGroup, QMessageBox, QScrollArea
from PyQt5.QtCore import QTimer, Qt

from f_score import ScoreWindow
from h_duel_tiebreaker import TiebreakerWindow

class QuestionWindow(QWidget):
    def __init__(self, mainApp, question):
        super().__init__()
        self.mainApp = mainApp
        self.question = question
        self.teamAnswersWidgets = []  # Pentru stocarea widgeturilor specifice fiecărei echipe
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.initUI()

    def initUI(self):
        butonWidth = 700
        layout = QVBoxLayout()

        # Adaugă un spațiu înainte de widgeturi pentru a le împinge în jos
        layout.addStretch()

        if self.mainApp.roundType == 'classic':
            # Afișarea echipei de rând
            currentTeamLabel = QLabel(f"Rândul echipei: {self.mainApp.currentTeamName}")
            currentTeamLabel.setStyleSheet("color: green")
            currentTeamLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(currentTeamLabel)
        elif self.mainApp.roundType == 'thief':
            # Afișarea echipei de rând
            currentTeamLabel = QLabel(f"{self.mainApp.currentTeamName}  >>>  {self.mainApp.selectedOpponent}")
            currentTeamLabel.setStyleSheet("color: green")
            currentTeamLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(currentTeamLabel)
        elif self.mainApp.roundType == 'champion':
            # Afișarea echipei de rând
            currentTeamLabel = QLabel(f"{self.mainApp.championTeams[0]}  x  {self.mainApp.championTeams[1]}")
            currentTeamLabel.setStyleSheet("color: green")
            currentTeamLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(currentTeamLabel)
        else:
            QMessageBox.warning(self, 'Eroare', 'Tipul rundei nu este găsit.')
        
        # Afișarea categoriei
        currentTeamLabel = QLabel(f"Categoria întrebării: {self.question['categorie']}")
        currentTeamLabel.setStyleSheet("color: blue")
        currentTeamLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(currentTeamLabel)

        # Afișarea întrebării
        questionLabel = QLabel(self.question['întrebare'])
        questionLabel.setWordWrap(True)  # Activează împărțirea textului pe mai multe linii
        questionLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(questionLabel)

        # Afișarea variantelor de răspuns cu litere
        self.labels = []
        self.answerMapping = {}
        letters = ['A', 'B', 'C', 'D']
        for i, answer in enumerate(self.question['răspunsuri']):
            label_text = f"{letters[i]}. {answer}"
            text = QLabel(label_text)
            text.setWordWrap(True)  # Activează împărțirea textului pe mai multe linii
            text.setAlignment(Qt.AlignCenter)
            self.labels.append(text)
            layout.addWidget(text)
            self.answerMapping[letters[i]] = answer

        # Timer
        self.timer = QLabel(f"Timp rămas: {self.mainApp.timerDuration} secunde")
        self.timer.setStyleSheet("color: red")
        self.timer.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer)
        self.startTimer()

        if self.mainApp.roundType != 'champion':
            # Răspunsuri echipe
            for team in self.mainApp.teamNames:
                teamLabel = QLabel(f"Răspunsuri echipa {team}")
                # teamLabel.setStyleSheet("color: green")
                teamLabel.setAlignment(Qt.AlignCenter)
                layout.addWidget(teamLabel)

                teamAnswerLayout = QHBoxLayout()
                teamAnswerLayout.addStretch()
                teamRadioButtonGroup = QButtonGroup(self)
                for option in letters:
                    radioButton = QRadioButton(option)
                    # radioButton.setStyleSheet("color: green")
                    teamAnswerLayout.addWidget(radioButton)
                    teamRadioButtonGroup.addButton(radioButton)
                teamAnswerLayout.addStretch()

                self.teamAnswersWidgets.append((team, teamRadioButtonGroup))
                layout.addLayout(teamAnswerLayout)
        elif self.mainApp.roundType == 'champion':
            # Răspunsuri echipe
            for team in self.mainApp.championTeams:
                teamLabel = QLabel(f"Răspunsuri echipa {team}")
                # teamLabel.setStyleSheet("color: green")
                teamLabel.setAlignment(Qt.AlignCenter)
                layout.addWidget(teamLabel)

                teamAnswerLayout = QHBoxLayout()
                teamAnswerLayout.addStretch()
                teamRadioButtonGroup = QButtonGroup(self)
                for option in letters:
                    radioButton = QRadioButton(option)
                    # radioButton.setStyleSheet("color: green")
                    teamAnswerLayout.addWidget(radioButton)
                    teamRadioButtonGroup.addButton(radioButton)
                teamAnswerLayout.addStretch()

                self.teamAnswersWidgets.append((team, teamRadioButtonGroup))
                layout.addLayout(teamAnswerLayout)
        else:
            QMessageBox.warning(self, 'Eroare (question)', 'Tipul rundei nu este găsit.')

        # Creare QHBoxLayout pentru alinierea butonului de verificare pe orizontală
        answerButtonLayout = QHBoxLayout()
        answerButtonLayout.addStretch()  # Adaugă un spațiu elastic înainte de buton pentru a-l împinge către centru

        # Adăugare buton de verificare răspunsuri în layout-ul orizontal
        self.answerButton = QPushButton("Verifică răspunsurile", self)
        #self.answerButton.setStyleSheet("color: green")
        self.answerButton.setFixedWidth(butonWidth)
        self.answerButton.clicked.connect(self.checkTeamAnswers)
        answerButtonLayout.addWidget(self.answerButton, 0, Qt.AlignCenter)  # Aliniază butonul pe centrul orizontal

        answerButtonLayout.addStretch()  # Adaugă un spațiu elastic după buton pentru a menține centrarea
        layout.addLayout(answerButtonLayout)  # Adaugă layout-ul orizontal în layout-ul vertical principal

        # Adaugă un spațiu după widgeturi pentru a le centra
        layout.addStretch()

        # self.setLayout(layout)
        
        # Create a scroll area
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)  # Allow the content widget to resize with the scroll area
        scrollArea.setAlignment(Qt.AlignCenter)
        scrollArea.setFixedWidth(1680)
        scrollArea.setFixedHeight(1050)

        # Set the layout as the content of the scroll area
        scrollWidget = QWidget()
        scrollWidget.setLayout(layout)
        scrollArea.setWidget(scrollWidget)
        
        self.setWindowTitle("Întrebare")
        self.showFullScreen()

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
        
        # Actualizăm numărul total de întrebări pentru fiecare echipă
        if self.mainApp.roundType != 'champion':
            for team in self.mainApp.teamNames:
                if self.question['categorie'] != "Departajare":
                    self.mainApp.totalQuestionCount[team] += 1
        else: 
            for team in self.mainApp.championTeams:
                if self.question['categorie'] != "Departajare":
                    self.mainApp.totalQuestionCount[team] += 1
        
        if self.mainApp.roundType == 'classic':
            roundAnswers = {}
            for team, teamRadioButtonGroup in self.teamAnswersWidgets:
                selectedButton = teamRadioButtonGroup.checkedButton()
                if selectedButton:
                    selectedLetter = selectedButton.text()
                    selectedAnswer = self.answerMapping[selectedLetter]
                    correct = selectedAnswer == self.question['răspuns corect']
                    roundAnswers[team] = correct
                # Actualizăm numărul de răspunsuri corecte pentru fiecare echipă
                if correct:
                    self.mainApp.correctAnswersCount[team] += 1
            
            # Afișăm scorurile
            self.scoreWindow = ScoreWindow(self.mainApp, roundAnswers, self.question['răspuns corect'])
            self.close()
            self.scoreWindow.show()
            
        elif self.mainApp.roundType == 'thief':
            roundAnswers = {}
            for team, teamRadioButtonGroup in self.teamAnswersWidgets:
                selectedButton = teamRadioButtonGroup.checkedButton()
                if selectedButton:
                    selectedLetter = selectedButton.text()
                    selectedAnswer = self.answerMapping[selectedLetter]
                    correct = selectedAnswer == self.question['răspuns corect']
                    roundAnswers[team] = correct
                # Actualizăm numărul de răspunsuri corecte pentru fiecare echipă
                if correct:
                    self.mainApp.correctAnswersCount[team] += 1
            
            if self.mainApp.selectedOpponent in roundAnswers and self.mainApp.currentTeamName in roundAnswers:
                if roundAnswers[self.mainApp.selectedOpponent] is True and roundAnswers[self.mainApp.currentTeamName] is True:
                    # Ambii participanți au răspuns corect, deci se inițiază departajarea
                    self.tiebreakerWindow = TiebreakerWindow(self.mainApp, roundAnswers)
                    self.close()
                    self.tiebreakerWindow.show()            
                else:
                    self.scoreWindow = ScoreWindow(self.mainApp, roundAnswers, self.question['răspuns corect'])
                    self.close()
                    self.scoreWindow.show()
            
            else:
                print("Nu s-a găsit răspunsul echipei.")
                QMessageBox.warning(self, 'Eroare', 'Nu s-a găsit răspunsul echipei.')
        
        elif self.mainApp.roundType == 'champion':
            roundAnswers = {}
            for team, teamRadioButtonGroup in self.teamAnswersWidgets:
                selectedButton = teamRadioButtonGroup.checkedButton()
                if selectedButton:
                    selectedLetter = selectedButton.text()
                    selectedAnswer = self.answerMapping[selectedLetter]
                    correct = selectedAnswer == self.question['răspuns corect']
                    roundAnswers[team] = correct
                # Actualizăm numărul de răspunsuri corecte pentru fiecare echipă
                if correct:
                    self.mainApp.correctAnswersCount[team] += 1
            
            if self.mainApp.championTeams[0] in roundAnswers and self.mainApp.championTeams[1] in roundAnswers:
                if roundAnswers[self.mainApp.championTeams[0]] is True and roundAnswers[self.mainApp.championTeams[1]] is True:
                    # Ambii participanți au răspuns corect, deci se inițiază departajarea
                    QMessageBox.information(self, 'Info', 'Ambele echipe au răspuns corect.')
                    self.tiebreakerWindow = TiebreakerWindow(self.mainApp, roundAnswers)
                    self.close()
                    self.tiebreakerWindow.show()            
                else:
                    self.scoreWindow = ScoreWindow(self.mainApp, roundAnswers, self.question['răspuns corect'])
                    self.close()
                    self.scoreWindow.show()
            
            else:
                print("Nu s-a găsit răspunsul echipei.")
                QMessageBox.warning(self, 'Eroare', 'Nu s-a găsit răspunsul echipei.')
