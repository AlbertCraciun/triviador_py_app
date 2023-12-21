from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer

from question_screen import QuestionWindow

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