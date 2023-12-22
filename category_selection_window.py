import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer

from question_window import QuestionWindow

class CategorySelectionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Afișarea echipei de rând
        currentTeamLabel = QLabel(f"Rândul echipei: {self.mainApp.currentTeamName}")
        layout.addWidget(currentTeamLabel)

        # TO DO: add categories from excell
        self.categories = ["Istorie", "Știință", "Artă", "Sport", "Geografie", "Aleator"]
        for category in self.categories:
            btn = QPushButton(category, self)
            btn.clicked.connect(lambda: self.onCategorySelected(category))
            layout.addWidget(btn)

        # Timer
        self.timer = QLabel("Timp rămas: 30 secunde", self)
        layout.addWidget(self.timer)
        if self.mainApp.categorySelectionTime > 0:
            self.startTimer()

        self.setLayout(layout)
        self.setWindowTitle("Selectează Categoria")
        self.setGeometry(300, 300, 400, 300)

    def startTimer(self):
        # Implementați logica pentru timer aici
        self.countdown = self.mainApp.categorySelectionTime
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
        self.onCategorySelected("Aleator")

    def onCategorySelected(self, category):
        # Implementați logica pentru atunci când o categorie este selectată
        print(f"Categoria selectată: {category}")
        
        if len(self.mainApp.questions) == 0:
            QMessageBox.warning(self, 'Eroare', 'Nu mai există întrebări!')
            return
        
        if category == "Aleator":
            self.mainApp.randomQuestion = True
            question = random.choice(self.mainApp.questions)
        else:
            possible_questions = [q for q in self.mainApp.questions if q['categorie'] == category]
            question = random.choice(possible_questions) if possible_questions else None
        
        self.mainApp.selectedQuestion = question
        self.mainApp.questions.remove(question)  # Eliminăm întrebarea selectată din listă

        # Afișăm fereastra cu întrebarea
        self.questionWindow = QuestionWindow(self.mainApp, question, teams=self.mainApp.teamNames)
        self.hide()  # Ascundem fereastra de selecție a categoriilor
        self.questionWindow.show()