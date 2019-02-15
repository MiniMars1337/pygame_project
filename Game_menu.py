import sys
from Life import Life
from secondgame import Game_2048
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Main_menu(QMainWindow):  # главное меню
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)  # дизайн меню
        self.game = '"Жизнь"'
        # импорт текстов (описание игр)
        self.text_1 = open('data/Описание игры Жизнь.txt').read()
        self.text_2 = open('data/Описание игры 2048.txt').read()
        self.game_rules.setText(self.text_1)
        self.game_edit.activated.connect(self.handleActivated)
        self.start_button.clicked.connect(self.StartGame)

    def handleActivated(self, index):
        # вставить текст в экран
        self.game = self.game_edit.itemText(index)
        if self.game == '"Жизнь"':
            self.game_rules.setText(self.text_1)
        elif self.game == '"2048" (изменённая)':
            self.game_rules.setText(self.text_2)

    def StartGame(self):
        # запуск игры
        if self.game == '"Жизнь"':
            life = Life((self.n_col.value(), self.n_row.value()))
            life.set_viev((0, 0, self.cell_size.value()))
            life.start_life()
        elif self.game == '"2048" (изменённая)':
            g = Game_2048((self.n_col.value(), self.n_row.value()))
            g.set_viev((0, 0, self.cell_size.value()))
            g.start_game()


app = QApplication(sys.argv)
ex = Main_menu()
ex.show()
sys.exit(app.exec_())
