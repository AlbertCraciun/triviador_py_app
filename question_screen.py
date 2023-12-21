from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QRadioButton
from PyQt5.QtCore import QTimer

class QuestionWindow(QWidget):
    def __init__(self, mainApp, question, answers):
        super().__init__()
        self.mainApp = mainApp
        self.question = question
        self.answers = answers
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
            self.validateAnswer()

    def validateAnswer(self):
        selectedAnswer = None
        for radioButton in self.radioButtons:
            if radioButton.isChecked():
                selectedAnswer = radioButton.text()
                break
        
        if selectedAnswer == "Paris":  # Presupunând că "Paris" este răspunsul corect
            # Logica pentru răspunsul corect
            QMessageBox.information(self, "Răspuns Corect", "Felicitări! Ați selectat răspunsul corect.")
        else:
            # Logica pentru răspunsul greșit
            QMessageBox.warning(self, "Răspuns Greșit", "Din păcate, acesta nu este răspunsul corect.")

        # Trecerea la următorul ecran (de exemplu, ecranul de scor sau următoarea întrebare)
        # self.mainApp.showScoreScreen() sau self.mainApp.showNextQuestion()
