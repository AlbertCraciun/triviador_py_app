from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton

class DuelSelectionWindow(QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.mainApp = mainApp
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        titleLabel = QLabel("Selectează Echipa Adversă și Categoria")
        layout.addWidget(titleLabel)

        # Selector pentru echipa adversă
        self.opponentTeamSelector = QComboBox(self)
        for team in self.mainApp.teamNames:
            if team != self.mainApp.currentTeamName:
                self.opponentTeamSelector.addItem(team)
        layout.addWidget(self.opponentTeamSelector)

        # Selector pentru categorie
        self.categorySelector = QComboBox(self)
        self.categorySelector.addItems(["Istorie", "Știință", "Artă", "Sport", "Geografie"])
        layout.addWidget(self.categorySelector)

        # Buton pentru confirmare
        confirmButton = QPushButton("Confirmă și Începe Duelul")
        confirmButton.clicked.connect(self.confirmDuel)
        layout.addWidget(confirmButton)

        self.setLayout(layout)
        self.setWindowTitle("Selecție Duel")
        self.setGeometry(300, 300, 400, 300)

    def confirmDuel(self):
        # Logica pentru confirmarea duelului și trecerea la întrebare
        selectedOpponent = self.opponentTeamSelector.currentText()
        selectedCategory = self.categorySelector.currentText()
        self.mainApp.initiateDuel(selectedOpponent, selectedCategory)
        self.hide()

    # ... restul codului necesar ...
