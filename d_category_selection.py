import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt

from e_question_window import QuestionWindow

class CategorySelectionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Adaugă un spațiu înainte de widgeturi pentru a le împinge în jos
        layout.addStretch()

        # Afișarea echipei de rând
        currentTeamLabel = QLabel(f"Rândul echipei: {self.mainApp.currentTeamName}")
        currentTeamLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(currentTeamLabel)

        self.categories = set()
        for question in self.mainApp.questions:
            if question['categorie'] != "Departajare":
                self.categories.add(question['categorie'])
        self.categories.add("Aleator")

        # Creare QHBoxLayout pentru alinierea butoanelor pe orizontală
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()  # Adaugă un spațiu elastic înainte de buton pentru a-l împinge către centru

        # Adăugare butoane categorie în layout-ul orizontal
        for category in self.categories:
            btn = QPushButton(category, self)
            btn.setFixedWidth(300)  # Setează lățimea fixă a butonului
            buttonLayout.addWidget(btn, 0, Qt.AlignCenter)  # Aliniază butonul pe centrul orizontal
            btn.clicked.connect(lambda _, c=category: self.onCategorySelected(c))

        buttonLayout.addStretch()  # Adaugă un spațiu elastic după buton pentru a menține centrarea
        layout.addLayout(buttonLayout)  # Adaugă layout-ul orizontal în layout-ul vertical principal

        # Timer
        self.timer = QLabel("Timp rămas: 30 secunde", self)
        self.timer.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer)
        if self.mainApp.categorySelectionTime > 0:
            self.startTimer()

        # Adaugă un spațiu după widgeturi pentru a le centra
        layout.addStretch()

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
        self.timerQTimer.stop()
        # Implementați logica pentru atunci când o categorie este selectată
        print(f"Categoria selectată: {category}")
        
        if len(self.mainApp.questions) == 0:
            QMessageBox.warning(self, 'Eroare', 'Nu mai există întrebări!')
            return
        
        if category == "Aleator":
            # Excludem întrebările de departajare pentru selecția aleatorie
            nonTiebreakerQuestions = [q for q in self.mainApp.questions if q['categorie'] != "Departajare"]
            if len(nonTiebreakerQuestions) == 0:
                QMessageBox.warning(self, 'Eroare', 'Nu mai există întrebări disponibile!')
                return
            question = random.choice(nonTiebreakerQuestions)
            self.mainApp.randomQuestion = True
        else:
            # Excludem întrebările de departajare și pentru celelalte categorii
            possible_questions = [q for q in self.mainApp.questions if q['categorie'] == category and q['categorie'] != "Departajare"]
            question = random.choice(possible_questions) if possible_questions else None

        if question:
            self.mainApp.selectedQuestion = question
            self.mainApp.questions.remove(question)  # Eliminăm întrebarea selectată din listă

            # Afișăm fereastra cu întrebarea
            self.questionWindow = QuestionWindow(self.mainApp, question, teams=self.mainApp.teamNames)
            self.hide()  # Ascundem fereastra de selecție a categoriilor
            self.questionWindow.show()
        else:
            QMessageBox.warning(self, 'Eroare', 'Nu există întrebări pentru categoria selectată.')