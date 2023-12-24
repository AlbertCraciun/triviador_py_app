from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QMessageBox, QCheckBox, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt

from b_questions_loader import load_questions_from_excel

class StartWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.teamInputs = []  # Lista pentru a stoca câmpurile de intrare pentru echipe
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.initUI()

    def initUI(self):
        # Setăm lungimea dorită pentru butoane
        buttonWidth = 300
        layout = QVBoxLayout()
        
        # Adaugă un spațiu înainte de widgeturi pentru a le împinge în jos
        layout.addStretch()

        # Titlu
        titleLayout = QHBoxLayout()
        titleLayout.addStretch()
        title = QLabel('AMiCUS Triviador\naplicație creată de Albert Crăciun')
        title.setAlignment(Qt.AlignCenter)
        titleLayout.addWidget(title)
        titleLayout.addStretch()
        layout.addLayout(titleLayout)
        
        # Buton pentru selectarea fișierului de întrebări
        filePickerLayout = QHBoxLayout()
        filePickerLayout.addStretch()

        self.filePickerButton = QPushButton('Selectează fișierul de întrebări', self)
        self.filePickerButton.setFixedWidth(buttonWidth)
        self.filePickerButton.clicked.connect(self.openFileDialog)
        filePickerLayout.addWidget(self.filePickerButton)

        filePickerLayout.addStretch()
        layout.addLayout(filePickerLayout)

        # Adăugarea câmpurilor de introducere a echipelor
        for i in range(15):
            teamInputLayout = QHBoxLayout()
            teamInputLayout.addStretch()

            teamInput = QLineEdit(self)
            teamInput.setPlaceholderText(f'Numele echipei {i + 1}')
            teamInput.setFixedWidth(buttonWidth)
            teamInput.setVisible(False)
            teamInput.textChanged.connect(self.updateRoundSpinners)
            self.teamInputs.append(teamInput)
            teamInputLayout.addWidget(teamInput)

            teamInputLayout.addStretch()
            layout.addLayout(teamInputLayout)

        # Buton pentru adăugarea de noi echipe
        addTeamLayout = QHBoxLayout()
        addTeamLayout.addStretch()

        self.btnAddTeam = QPushButton('Adaugă echipă', self)
        self.btnAddTeam.setFixedWidth(buttonWidth)
        self.btnAddTeam.clicked.connect(self.addTeam)
        addTeamLayout.addWidget(self.btnAddTeam)

        addTeamLayout.addStretch()
        layout.addLayout(addTeamLayout)


        # Selector pentru timpul de răspuns
        responseTimeLayout = QHBoxLayout()
        responseTimeLayout.addStretch()

        # Adaugă eticheta (label)
        responseTimeLabel = QLabel('Timpul de răspuns (sec.):')
        responseTimeLayout.addWidget(responseTimeLabel)

        # Adaugă QSpinBox
        self.responseTime = QSpinBox(self)
        self.responseTime.setRange(10, 60)  # timpul între 10 și 60 de secunde
        self.responseTime.setValue(30)  # valoarea implicită
        responseTimeLayout.addWidget(self.responseTime)

        responseTimeLayout.addStretch()
        layout.addLayout(responseTimeLayout)

        # Selector pentru timpul de alegere categorie
        categoryTimeLayout = QHBoxLayout()
        categoryTimeLayout.addStretch()

        categoryTimeLabel = QLabel('Timp selecție categorii (sec.):')
        categoryTimeLayout.addWidget(categoryTimeLabel)

        self.categorySelectionTime = QSpinBox(self)
        self.categorySelectionTime.setRange(0, 30)
        self.categorySelectionTime.setValue(20)
        categoryTimeLayout.addWidget(self.categorySelectionTime)

        categoryTimeLayout.addStretch()
        layout.addLayout(categoryTimeLayout)

        # Selector pentru numărul de runde clasice
        classicRoundsLayout = QHBoxLayout()
        classicRoundsLayout.addStretch()

        classicRoundsLabel = QLabel('Numărul de runde clasice:')
        classicRoundsLayout.addWidget(classicRoundsLabel)

        self.numClassicRounds = QSpinBox(self)
        self.numClassicRounds.setRange(0, 30)
        self.numClassicRounds.setValue(0)
        classicRoundsLayout.addWidget(self.numClassicRounds)

        classicRoundsLayout.addStretch()
        layout.addLayout(classicRoundsLayout)

        # Selector pentru numărul de runde de tip "Duel"
        thiefRoundsLayout = QHBoxLayout()
        thiefRoundsLayout.addStretch()

        thiefRoundsLabel = QLabel('Numărul de runde duel:')
        thiefRoundsLayout.addWidget(thiefRoundsLabel)

        self.numThiefRounds = QSpinBox(self)
        self.numThiefRounds.setRange(0, 30)
        self.numThiefRounds.setValue(0)
        thiefRoundsLayout.addWidget(self.numThiefRounds)

        thiefRoundsLayout.addStretch()
        layout.addLayout(thiefRoundsLayout)

       # Checkbox pentru activarea rundelor campionilor
        championRoundsLayout = QHBoxLayout()
        championRoundsLayout.addStretch()

        self.championRoundsEnabled = QCheckBox('Activează rundele campionilor', self)
        self.championRoundsEnabled.stateChanged.connect(self.toggleChampionRounds)
        championRoundsLayout.addWidget(self.championRoundsEnabled)

        championRoundsLayout.addStretch()
        layout.addLayout(championRoundsLayout)

        # Selector pentru numărul de runde ale campionilor
        championRoundsSpinBoxLayout = QHBoxLayout()
        championRoundsSpinBoxLayout.addStretch()

        self.numChampionRounds = QSpinBox(self)
        self.numChampionRounds.setRange(1, 30)  # între 1 și 30 runde
        self.numChampionRounds.setValue(10)  # valoarea implicită
        self.qLabelChampionRounds = QLabel('Numărul de runde ale campionilor:')
        self.qLabelChampionRounds.setAlignment(Qt.AlignCenter)
        championRoundsSpinBoxLayout.addWidget(self.qLabelChampionRounds)
        self.qLabelChampionRounds.setVisible(False)  # Inițial, ascundem întrebarea
        championRoundsSpinBoxLayout.addWidget(self.numChampionRounds)
        self.numChampionRounds.setVisible(False)  # Inițial, ascundem selectorul

        championRoundsSpinBoxLayout.addStretch()
        layout.addLayout(championRoundsSpinBoxLayout)

        # Buton de start cu eveniment conectat
        startBtnLayout = QHBoxLayout()
        startBtnLayout.addStretch()

        startBtn = QPushButton('Start', self)
        startBtn.setFixedWidth(buttonWidth)
        startBtn.clicked.connect(self.onStart)
        startBtnLayout.addWidget(startBtn)

        startBtnLayout.addStretch()
        layout.addLayout(startBtnLayout)

        # Adaugă un spațiu după widgeturi pentru a le centra
        layout.addStretch()

        self.setLayout(layout)
        self.setWindowTitle('Joc de Cultură Generală')
        self.setGeometry(300, 300, 400, 300)
        
    def updateRoundSpinners(self):
        # Obținem numărul de echipe adăugate
        teamCount = len([input for input in self.teamInputs if input.isVisible() and input.text()])

        if teamCount > 0:
            # Setăm numărul minim de runde clasice ca fiind egal cu numărul de echipe
            self.numClassicRounds.setMinimum(teamCount)
            # Dacă valoarea curentă este mai mică decât numărul minim, o actualizăm
            if self.numClassicRounds.value() < teamCount:
                self.numClassicRounds.setValue(teamCount)

            # Actualizăm pasul de incrementare pentru spinbox-uri
            self.numClassicRounds.setSingleStep(teamCount)
            self.numThiefRounds.setSingleStep(teamCount)
        else:
            # Dacă nu există echipe, resetăm la valorile implicite
            self.numClassicRounds.setMinimum(0)
            self.numClassicRounds.setValue(0)
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
        self.close()
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
            for question in self.mainApp.questions:
                if question['categorie'] != "Departajare":
                    self.mainApp.categories.add(question['categorie'])
            self.mainApp.categories.add("Aleator")