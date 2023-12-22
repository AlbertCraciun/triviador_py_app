from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QMessageBox, QCheckBox, QFileDialog
from PyQt5.QtCore import Qt

from questions_loader import load_questions_from_excel

class StartWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.teamInputs = []  # Lista pentru a stoca câmpurile de intrare pentru echipe
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Titlu
        title = QLabel('AMiCUS Trivia')
        subtitle = QLabel('aplicație creată de Albert C.')
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        self.filePickerButton = QPushButton('Selectează fișierul de întrebări', self)
        self.filePickerButton.clicked.connect(self.openFileDialog)
        layout.addWidget(self.filePickerButton)

        # Conectăm fiecare câmp de introducere a echipelor la un nou slot
        for i in range(15):
            teamInput = QLineEdit(self)
            teamInput.setPlaceholderText(f'Numele echipei {i + 1}')
            teamInput.setVisible(False)  # Inițial, ascundem toate câmpurile
            teamInput.textChanged.connect(self.updateRoundSpinners)  # Noua conexiune
            self.teamInputs.append(teamInput)
            layout.addWidget(teamInput)
        
        # Buton pentru adăugarea de noi echipe
        self.btnAddTeam = QPushButton('Adaugă echipă', self)
        self.btnAddTeam.clicked.connect(self.addTeam)
        layout.addWidget(self.btnAddTeam)

        # Selector pentru timpul de răspuns
        self.responseTime = QSpinBox(self)
        self.responseTime.setRange(10, 60)  # timpul între 10 și 60 de secunde
        self.responseTime.setValue(30)  # valoarea implicită
        layout.addWidget(QLabel('Selectează timpul de răspuns (secunde)'))
        layout.addWidget(self.responseTime)
        
        # Selector pentru timpul de alegere categorie
        self.categorySelectionTime = QSpinBox(self)
        self.categorySelectionTime.setRange(0, 30)  # timpul între 10 și 60 de secunde
        self.categorySelectionTime.setValue(20)  # valoarea implicită
        layout.addWidget(QLabel('Selectează timpul de alegere pentru categorie (secunde)'))
        layout.addWidget(self.categorySelectionTime)

        # Selector pentru numărul de runde clasice
        self.numClassicRounds = QSpinBox(self)
        self.numClassicRounds.setRange(0, 30)
        self.numClassicRounds.setValue(0)  # valoarea implicită
        layout.addWidget(QLabel('Selectează numărul de runde clasice'))
        layout.addWidget(self.numClassicRounds)
        
        # Selector pentru numărul de runde de tip "Duel"
        self.numThiefRounds = QSpinBox(self)
        self.numThiefRounds.setRange(0, 30)
        self.numThiefRounds.setValue(0)
        layout.addWidget(QLabel('Selectează numărul de runde duel'))
        layout.addWidget(self.numThiefRounds)
        
        # Adăugăm un checkbox pentru activarea rundelor campionilor
        self.championRoundsEnabled = QCheckBox('Activează rundele campionilor', self)
        self.championRoundsEnabled.stateChanged.connect(self.toggleChampionRounds)
        layout.addWidget(self.championRoundsEnabled)
        
        # Selector pentru numărul de runde ale campionilor
        self.numChampionRounds = QSpinBox(self)
        self.numChampionRounds.setRange(1, 30)  # între 1 și 30 runde
        self.numChampionRounds.setValue(10)  # valoarea implicită
        self.qLabelChampionRounds = QLabel('Selectează numărul de runde ale campionilor')
        layout.addWidget(self.qLabelChampionRounds)
        self.qLabelChampionRounds.setVisible(False)  # Inițial, ascundem întrebarea
        layout.addWidget(self.numChampionRounds)
        self.numChampionRounds.setVisible(False)  # Inițial, ascundem selectorul

        # Buton de start cu eveniment conectat
        startBtn = QPushButton('Start', self)
        startBtn.clicked.connect(self.onStart)
        layout.addWidget(startBtn)

        self.setLayout(layout)
        self.setWindowTitle('Joc de Cultură Generală')
        self.setGeometry(300, 300, 400, 300)
        
    def updateRoundSpinners(self):
        # Actualizăm pasul de incrementare pentru spinbox-uri
        teamCount = len([input for input in self.teamInputs if input.isVisible() and input.text()])
        if teamCount > 0:
            self.numClassicRounds.setSingleStep(teamCount)
            self.numThiefRounds.setSingleStep(teamCount)
        else:
            self.numClassicRounds.setSingleStep(1)
            self.numThiefRounds.setSingleStep(1)
        
    def onStart(self):
        # Colectare și validare date
        teamNames = [input.text() for input in self.teamInputs if input.isVisible() and input.text()]
        if len(set(teamNames)) != len(teamNames):
            QMessageBox.warning(self, 'Eroare', 'Numele echipelor trebuie să fie unice!')
            return
        if len(teamNames) < 2:  # Presupunem că sunt necesare cel puțin 2 echipe
            QMessageBox.warning(self, 'Eroare', 'Introduceți cel puțin două echipe!')
            return
        if self.numClassicRounds.value() < len(teamNames) or self.numClassicRounds.value() % len(teamNames) != 0:
            QMessageBox.warning(self, 'Eroare', 'Introduceți un număr de runde multiplu de numărul de echipe!')
            return
        if self.numThiefRounds.value() % 2 != 0:
            QMessageBox.warning(self, 'Eroare', 'Introduceți un număr par de runde!')
            return
        if len(self.mainApp.questions) == 0:
            QMessageBox.warning(self, 'Eroare', 'Nu ați selectat fișierul de întrebări!')
            return
        
        for teamName in teamNames:
            self.mainApp.totalScores[teamName] = 0

        # Salvăm datele și trecem la ecranul următor
        self.mainApp.teamNames = teamNames
        self.mainApp.timerDuration = self.responseTime.value()
        self.mainApp.categorySelectionTime = self.categorySelectionTime.value()
        self.mainApp.numClassicRounds = self.numClassicRounds.value()
        self.mainApp.numThiefRounds = self.numThiefRounds.value()
        self.mainApp.numChampionRounds = self.numChampionRounds.value()
        self.mainApp.showNextScreen()  # Metodă pentru a afișa ecranul următor
        

    def addTeam(self):
        # Activăm câmpul următor pentru numele echipei
        for teamInput in self.teamInputs:
            if not teamInput.isVisible():
                teamInput.setVisible(True)
                break    
    
    def toggleChampionRounds(self, state):
        # Activăm sau dezactivăm selectorul pentru rundele campionilor
        isEnabled = state == Qt.Checked
        self.qLabelChampionRounds.setVisible(isEnabled)
        self.numChampionRounds.setVisible(isEnabled)
        
    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selectează fișierul excel", "", "Excel Files (*.xlsx)")
        if fileName:
            self.mainApp.questions = load_questions_from_excel(fileName)
            self.filePickerButton.setText(fileName.split('/')[-1])