from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

class DuelSelectionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch()  # Adaugă spațiu pentru centrare verticală

        titleLabel = QLabel("Selectează Echipa Adversă și Categoria")
        titleLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titleLabel)

        # Selector pentru echipa adversă
        self.opponentTeamSelector = QComboBox(self)
        for team in self.mainApp.teamNames:
            if team != self.mainApp.currentTeamName:
                self.opponentTeamSelector.addItem(team)
        layout.addWidget(self.opponentTeamSelector, 0, Qt.AlignCenter)

        # Selector pentru categorie
        self.categorySelector = QComboBox(self)
        self.categorySelector.addItems(self.mainApp.getCategories())  # Presupunând că există o metodă getCategories
        layout.addWidget(self.categorySelector, 0, Qt.AlignCenter)

        # Buton pentru confirmare
        confirmButton = QPushButton("Confirmă și Începe Duelul")
        confirmButton.clicked.connect(self.confirmDuel)
        layout.addWidget(confirmButton, 0, Qt.AlignCenter)

        layout.addStretch()  # Adaugă spațiu pentru centrare verticală
        self.setLayout(layout)
        self.setWindowTitle("Selecție Duel")
        self.setGeometry(300, 300, 400, 300)

    def confirmDuel(self):
        # Logica pentru confirmarea duelului și trecerea la întrebare
        selectedOpponent = self.opponentTeamSelector.currentText()
        selectedCategory = self.categorySelector.currentText()
        self.mainApp.initiateDuel(selectedOpponent, selectedCategory)
        self.hide()
