import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer

from f_score import ScoreWindow

class TiebreakerWindow(QWidget):
    def __init__(self, mainApp, roundAnswers):
        super().__init__()
        self.mainApp = mainApp
        self.roundAnswers = roundAnswers
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Adaugă un spațiu înainte de widgeturi pentru a le împinge în jos
        layout.addStretch()
        
        # Afișarea echipei de rând
        currentTeamLabel = QLabel(f"{self.mainApp.currentTeamName} x {self.mainApp.selectedOpponent}")
        currentTeamLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(currentTeamLabel)

        attackingTeam = self.mainApp.currentTeamName
        defendingTeam = self.mainApp.selectedOpponent
        
        possible_questions = [q for q in self.mainApp.questions if q['categorie'] == "Departajare"]
        question = random.choice(possible_questions) if possible_questions else None
        
        if question is None:
            QMessageBox.warning(self, 'Eroare', 'Nu există întrebări de departajare.')
        
        # Afișarea întrebării
        questionLabel = QLabel(question['întrebare'])
        questionLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(questionLabel)
        
        # Câmpuri de introducere a răspunsurilor
        self.answerInputs = {}
        for team in [attackingTeam, defendingTeam]:
            teamLabel = QLabel(f"Răspuns echipa {team}")
            teamLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(teamLabel)

            answerInput = QLineEdit(self)
            answerInput.setPlaceholderText("Introdu răspunsul aici")
            layout.addWidget(answerInput)
            self.answerInputs[team] = answerInput
            
        # Timer
        self.timer = QLabel(f"Timp rămas: {self.mainApp.timerDuration} secunde")
        self.timer.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer)
        self.startTimer()

        # Buton pentru confirmarea răspunsurilor
        confirmButton = QPushButton("Confirmă răspunsurile", self)
        confirmButton.clicked.connect(self.confirmAnswers)
        layout.addWidget(confirmButton, 0, Qt.AlignCenter)

        # Adaugă un spațiu după widgeturi pentru a le centra
        layout.addStretch()

        self.setLayout(layout)
        self.setWindowTitle("Departajare")
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
            self.questionLabel.hide()
    
    def resetForNewTiebreaker(self):
        
        # Selectați o nouă întrebare de departajare
        possible_questions = [q for q in self.mainApp.questions if q['categorie'] == "Departajare"]
        self.question = random.choice(possible_questions) if possible_questions else None

        if self.question is None:
            QMessageBox.warning(self, 'Eroare', 'Nu există întrebări de departajare disponibile.')
            # Închideți fereastra de departajare sau gestionați lipsa întrebărilor
            return

        # Actualizați textul întrebării
        self.questionLabel.setText(self.question['întrebare'])

        # Curățați câmpurile de răspuns existente
        for input in self.answerInputs.values():
            input.clear()
            
        # Timer
        self.startTimer()

    def confirmAnswers(self):
        self.timerQTimer.stop()
        
        # Extragerea și verificarea răspunsurilor
        answers = {team: float(input.text()) for team, input in self.answerInputs.items() if input.text()}
        # Presupunem că avem acces la răspunsul corect al întrebării de departajare
        correctAnswer = self.question['răspuns corect']
        
        # Distanțele de la răspunsul fiecărei echipe la răspunsul corect
        distances = {team: abs(answer - correctAnswer) for team, answer in answers.items()}

        # Calculăm care echipă este mai aproape de răspunsul corect
        closestTeams = [team for team, distance in distances.items() if distance == min(distances.values())]

        # Dacă avem mai mult de o echipă la egalitate, apare informare si se reia departajarea
        if len(closestTeams) > 1:
            QMessageBox.information(self, 'Egalitate', 'Ambele echipe sunt la egalitate. Se va repeta departajarea.')
            self.resetForNewTiebreaker()
        else:
            # Echipa câștigătoare este cea mai aproape de răspunsul corect
            winningTeam = closestTeams[0]
            defeatedTeam = [team for team in distances.keys() if team != winningTeam][0]
            self.roundAnswers[winningTeam] = True
            self.roundAnswers[defeatedTeam] = False
            
            # Închiderea ferestrei
            self.scoreWindow = ScoreWindow(self.mainApp, self.roundAnswers)
            self.hide()
            self.scoreWindow.show()
        

