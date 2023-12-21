## not functional yet

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpinBox, QCheckBox
from PyQt5.QtCore import Qt

class GameConfigWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

         # Selector pentru timpul de răspuns
        self.responseTime = QSpinBox(self)
        self.responseTime.setRange(10, 60)  # timpul între 10 și 60 de secunde
        self.responseTime.setValue(30)  # valoarea implicită
        layout.addWidget(QLabel('Selectează timpul de răspuns (secunde)'))
        layout.addWidget(self.responseTime)
        
        # Selector pentru timpul de alegere categorie
        self.categorySelectionTime = QSpinBox(self)
        self.categorySelectionTime.setRange(0, 30)  # timpul între 10 și 60 de secunde
        self.categorySelectionTime.setValue(30)  # valoarea implicită
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
        backBtn = QPushButton('Înapoi', self)
        backBtn.clicked.connect(self.onBack)
        layout.addWidget(backBtn)

        self.setLayout(layout)
        self.setWindowTitle('Configurare Joc')
        self.setGeometry(300, 300, 400, 300)
        
    def onBack(self):
        # save values
        self.mainApp.timerDuration = self.responseTime.value()
        self.mainApp.categorySelectionTime = self.categorySelectionTime.value()
        self.mainApp.numClassicRounds = self.numClassicRounds.value()
        self.mainApp.numThiefRounds = self.numThiefRounds.value()
        self.mainApp.numChampionRounds = self.numChampionRounds.value()
        self.mainApp.championRoundsEnabled = self.championRoundsEnabled.isChecked()
        
        # Închidem fereastra curentă și revenim la fereastra de start
        self.close()
        
    def toggleChampionRounds(self, state):
        # Activăm sau dezactivăm selectorul pentru rundele campionilor
        isEnabled = state == Qt.Checked
        self.qLabelChampionRounds.setVisible(isEnabled)
        self.numChampionRounds.setVisible(isEnabled)
        
        