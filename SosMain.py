import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QGridLayout, QWidget, QVBoxLayout, QLabel, 
                             QCheckBox, QRadioButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont

class SOSGame(QMainWindow):
    # 'Size' determines the size of the play grid -> may change to customizable in the future
    def __init__(self, size=5):
        super().__init__()
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.current_player = "Blue"
        self.sos_lines = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SOS Game - v1.0")
        self.setGeometry(400, 400, 400, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        
        self.check_box = QCheckBox("Enable Hints")
        self.layout.addWidget(self.check_box)
        
        self.radio_simple = QRadioButton("Simple Game")
        self.radio_general = QRadioButton("General Game")
        self.radio_simple.setChecked(True)
        
        self.layout.addWidget(self.radio_simple)
        self.layout.addWidget(self.radio_general)
        
        self.label = QLabel()
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.update_label()
        self.layout.addWidget(self.label)
        
        self.grid_layout = QGridLayout()
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        for row in range(self.size):
            for col in range(self.size):
                btn = QPushButton(" ")
                btn.setFixedSize(50, 50)
                btn.clicked.connect(lambda _, r=row, c=col: self.make_move(r, c))
                self.grid_layout.addWidget(btn, row, col)
                self.buttons[row][col] = btn
        
        self.layout.addLayout(self.grid_layout)
        self.central_widget.setLayout(self.layout)
    
    def update_label(self):
        ''' Updates the color of the current play (blue/red). '''
        color = "blue" if self.current_player == "Blue" else "red"
        self.label.setText(f"Current Player: <span style='color:{color};'>{self.current_player}</span>")
    
    def make_move(self, row, col):
        ''' Sets the S/O based on player turn. '''
        if self.board[row][col] == "":
            letter = "S" if self.current_player == "Blue" else "O"
            self.board[row][col] = letter
            self.buttons[row][col].setText(letter)
            if self.check_sos(row, col):
                self.update()
            self.current_player = "Red" if self.current_player == "Blue" else "Blue"
            self.update_label()
    
    def check_sos(self, row, col):
        ''' checks whether any SOS sequence is present in any of the 
            four possible directions (horizontal, vertical, diagonal, and reverse diagonal). '''
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dr, dc in directions:
            if self.is_sos(row, col, dr, dc):
                self.sos_lines.append(((row, col), (row + 2*dr, col + 2*dc)))
                return True
        return False
    
    def is_sos(self, row, col, dr, dc):
        ''' Checks a specific direction from a given position to see if it forms an SOS sequence. '''
        try:
            if (self.board[row][col] == "S" and
                self.board[row + dr][col + dc] == "O" and
                self.board[row + 2*dr][col + 2*dc] == "S"):
                return True
        except IndexError:
            return False
        return False
    
    def paintEvent(self, event):
        ''' Draws the "hint" line. Work in progress, does not scale properly. '''
        painter = QPainter(self)
        painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        for (start, end) in self.sos_lines:
            x1, y1 = start[1] * 50 + 25, start[0] * 50 + 150
            x2, y2 = end[1] * 50 + 25, end[0] * 50 + 150
            painter.drawLine(x1, y1, x2, y2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SOSGame()
    game.show()
    sys.exit(app.exec_())