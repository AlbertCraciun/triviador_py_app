import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QMessageBox, QRadioButton
from PyQt5.QtCore import QTimer

class StartWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.teamInputs = []  # Lista pentru a stoca câmpurile de intrare pentru echipe
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Titlu
        title = QLabel('Ecranul de Start')
        layout.addWidget(title)

        # Câmpuri pentru numele echipelor
        for i in range(15):
            teamInput = QLineEdit(self)
            teamInput.setPlaceholderText(f'Numele echipei {i + 1}')
            teamInput.setVisible(False)  # Inițial, ascundem toate câmpurile
            self.teamInputs.append(teamInput)
            layout.addWidget(teamInput)
        
        # Buton pentru adăugarea de noi echipe
        self.btnAddTeam = QPushButton('Adaugă Echipă', self)
        self.btnAddTeam.clicked.connect(self.addTeam)
        layout.addWidget(self.btnAddTeam)

        # Selector pentru timpul de răspuns
        self.responseTime = QSpinBox(self)
        self.responseTime.setRange(10, 60)  # timpul între 10 și 60 de secunde
        self.responseTime.setValue(30)  # valoarea implicită
        layout.addWidget(QLabel('Selectează timpul de răspuns (secunde)'))
        layout.addWidget(self.responseTime)

        # Selector pentru numărul de runde
        self.numRounds = QSpinBox(self)
        self.numRounds.setRange(1, 10)  # între 1 și 10 runde
        self.numRounds.setValue(3)  # valoarea implicită
        layout.addWidget(QLabel('Selectează numărul de runde'))
        layout.addWidget(self.numRounds)

        # Buton de start cu eveniment conectat
        startBtn = QPushButton('Start', self)
        startBtn.clicked.connect(self.onStart)
        layout.addWidget(startBtn)

        self.setLayout(layout)
        self.setWindowTitle('Joc de Cultură Generală')
        self.setGeometry(300, 300, 400, 300)
        
    def onStart(self):
        # Colectare și validare date
        teamNames = [input.text() for input in self.teamInputs if input.isVisible() and input.text()]
        if len(set(teamNames)) != len(teamNames):
            QMessageBox.warning(self, 'Eroare', 'Numele echipelor trebuie să fie unice!')
            return
        if len(teamNames) < 2:  # Presupunem că sunt necesare cel puțin 2 echipe
            QMessageBox.warning(self, 'Eroare', 'Introduceți cel puțin două echipe!')
            return

        # Salvăm datele și trecem la ecranul următor
        self.mainApp.teamNames = teamNames
        self.mainApp.timerDuration = self.responseTime.value()
        self.mainApp.numRounds = self.numRounds.value()
        self.mainApp.showNextScreen()  # Metodă pentru a afișa ecranul următor

    def addTeam(self):
        # Activăm câmpul următor pentru numele echipei
        for teamInput in self.teamInputs:
            if not teamInput.isVisible():
                teamInput.setVisible(True)
                break    

class CategorySelectionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Aici, adăugați cod pentru afișarea categoriilor
        # De exemplu, puteți folosi o listă de butoane pentru fiecare categorie
        self.categories = ["Istorie", "Știință", "Artă", "Sport", "Geografie", "Aleatorie"]
        for category in self.categories:
            btn = QPushButton(category, self)
            btn.clicked.connect(lambda: self.onCategorySelected(category))
            layout.addWidget(btn)

        # Timer
        self.timer = QLabel("Timp rămas: 30 secunde", self)
        layout.addWidget(self.timer)
        self.startTimer()

        self.setLayout(layout)
        self.setWindowTitle("Selectează Categoria")
        self.setGeometry(300, 300, 400, 300)

    def startTimer(self):
        # Implementați logica pentru timer aici
        self.countdown = self.mainApp.timerDuration
        self.timerQTimer = QTimer(self)
        self.timerQTimer.timeout.connect(self.updateTimer)
        self.timerQTimer.start(1000)

    def updateTimer(self):
        self.countdown -= 1
        self.timer.setText(f"Timp rămas: {self.countdown} secunde")
        if self.countdown <= 0:
            self.timerQTimer.stop()
            self.handleTimeExpired()  # Metodă nouă pentru gestionarea expirării timpului

    def handleTimeExpired(self):
        # Logica pentru când timpul expiră
        # De exemplu, putem selecta automat o categorie aleatorie
        self.onCategorySelected("Aleator")

    def onCategorySelected(self, category):
        # Implementați logica pentru atunci când o categorie este selectată
        print(f"Categoria selectată: {category}")
        # Trecerea la ecranul cu întrebarea propriu-zisă
        
        question = "Ce este capitala Franței?"
        answers = ["Paris", "Londra", "Berlin", "Madrid"]

        # Afișăm fereastra cu întrebarea
        self.questionWindow = QuestionWindow(self.mainApp, question, answers)
        self.hide()  # Ascundem fereastra de selecție a categoriilor
        self.questionWindow.show()

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

class MainApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.teamNames = []
        self.timerDuration = 30
        self.numRounds = 3
        self.startWindow = StartWindow(self)
        self.startWindow.show()

    def showNextScreen(self):
        self.categorySelectionWindow = CategorySelectionWindow(self)
        self.startWindow.hide()  # Ascundem fereastra de start
        self.categorySelectionWindow.show()  # Afișăm fereastra de selecție a categoriilor
        
    def showQuestionScreen(self, question, answers):
        self.questionWindow = QuestionWindow(self, question, answers)
        self.questionWindow.show()

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
