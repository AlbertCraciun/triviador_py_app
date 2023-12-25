import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout, QComboBox, QGridLayout, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt

from e_question import QuestionWindow

class CategorySelectionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Adaugă un spațiu înainte de widgeturi pentru a le împinge în jos
        layout.addStretch()

        if self.mainApp.roundType != 'champion':
            # Afișarea echipei de rând
            currentTeamLabel = QLabel(f"Rândul echipei: {self.mainApp.currentTeamName}")
            currentTeamLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(currentTeamLabel)

        if self.mainApp.roundType == 'thief':
            titleLabel = QLabel("Selectează echipa adversă și categoria")
            titleLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(titleLabel)

            # Selector pentru echipa adversă
            self.opponentTeamSelector = QComboBox(self)
            for team in self.mainApp.teamNames:
                if team != self.mainApp.currentTeamName:
                    self.opponentTeamSelector.addItem(team)
            self.opponentTeamSelector.setCurrentIndex(0)
            self.opponentTeamSelector.setFixedWidth(300)
            layout.addWidget(self.opponentTeamSelector, 0, Qt.AlignCenter)
        
        if self.mainApp.roundType != 'champion':
            # Creare QHBoxLayout pentru alinierea butoanelor pe orizontală
            buttonLayout = QVBoxLayout()
            buttonLayout.addStretch()  # Adaugă un spațiu elastic înainte de buton pentru a-l împinge către centru

            # Adăugare butoane categorie în layout-ul orizontal
            for category in self.mainApp.categories:
                possible_questions = [q for q in self.mainApp.questions if q['categorie'] == category and q['categorie'] != "Departajare"]
                if possible_questions or category == "Aleator":
                    btn = QPushButton(category, self)
                    btn.setFixedWidth(300)  # Setează lățimea fixă a butonului
                    buttonLayout.addWidget(btn, 0, Qt.AlignCenter)  # Aliniază butonul pe centrul orizontal
                    btn.clicked.connect(lambda _, c=category: self.onCategorySelected(c))

            buttonLayout.addStretch()  # Adaugă un spațiu elastic după buton pentru a menține centrarea
            layout.addLayout(buttonLayout)  # Adaugă layout-ul orizontal în layout-ul vertical principal
         
        # Timer
        self.timer = QLabel(f"Timp rămas: {self.mainApp.selectionTime} secunde")
        self.timer.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer)
        self.startTimer()

        # Adaugă un spațiu după widgeturi pentru a le centra
        layout.addStretch()

        self.setLayout(layout)
        self.setWindowTitle("Selectează Categoria")
        self.setGeometry(300, 300, 400, 300)

    def startTimer(self):
        # Implementați logica pentru timer aici
        self.countdown = self.mainApp.selectionTime
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
        self.mainApp.selectedCategory = category
        
        if len(self.mainApp.questions) == 0:
            QMessageBox.warning(self, 'Eroare', 'Nu mai există întrebări!')
            return
        
        if category == "Aleator" or self.mainApp.roundType == 'champion':
            # Excludem întrebările de departajare pentru selecția aleatorie
            nonTiebreakerQuestions = [q for q in self.mainApp.questions if q['categorie'] != "Departajare"]
            if len(nonTiebreakerQuestions) == 0:
                QMessageBox.warning(self, 'Eroare', 'Nu mai există întrebări disponibile!')
                return
            question = random.choice(nonTiebreakerQuestions)
            self.mainApp.randomQuestion = True
        else:
            # cautam o intrebare din categoria selectata
            possible_questions = [q for q in self.mainApp.questions if q['categorie'] == category and q['categorie'] != "Departajare"]
            question = random.choice(possible_questions) if possible_questions else None

        if question:
            self.mainApp.selectedQuestion = question
            self.mainApp.questions.remove(question)  # Eliminăm întrebarea selectată din listă

            if self.mainApp.roundType == 'thief':
                self.mainApp.selectedOpponent = self.opponentTeamSelector.currentText()
            
            # Afișăm fereastra cu întrebarea
            self.mainApp.selectedCategory = category
            self.questionWindow = QuestionWindow(self.mainApp, question)
            self.close()
            self.questionWindow.show()
        else:
            QMessageBox.warning(self, 'Eroare', 'Nu există întrebări pentru categoria selectată.')