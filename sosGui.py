from PyQt5.QtWidgets import (QMainWindow, QPushButton, 
                             QGridLayout, QWidget, QVBoxLayout, QLabel, 
                             QRadioButton, QDialog,
                             QHBoxLayout, QSlider, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont
from sosGameLogic import SOSGameLogic

class SetupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Setup")
        self.setFixedSize(350, 280)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border-radius: 10px;
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Board size selection label
        self.label = QLabel("Select Board Size:")
        self.label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.label)

        # Slider for board size
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(3)
        self.size_slider.setMaximum(20)
        self.size_slider.setValue(10)
        self.size_slider.setTickInterval(1)
        self.size_slider.setTickPosition(QSlider.TicksBelow)
        self.size_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #ddd;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -5px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #45a049;
            }
        """)

        layout.addWidget(self.size_slider)

        # Dynamic Label to show selected board size
        self.size_label = QLabel("Board Size: 10")
        self.size_label.setFont(QFont("Arial", 12))
        self.size_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.size_label)

        # Connect slider change event
        self.size_slider.valueChanged.connect(self.update_size_label)

        # Game mode selection
        self.label_mode = QLabel("Select Game Mode:")
        self.label_mode.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.label_mode)

        self.radio_simple = QRadioButton("Simple Game")
        self.radio_general = QRadioButton("General Game")
        self.radio_simple.setChecked(True)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.radio_simple)
        mode_layout.addWidget(self.radio_general)
        layout.addLayout(mode_layout)

        # Start Game Button
        self.start_button = QPushButton("Start Game")
        self.start_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.center_window()

    def update_size_label(self):
        """Updates the label to show the selected board size from the slider."""
        self.size_label.setText(f"Board Size: {self.size_slider.value()}")

    def start_game(self):
        size = self.size_slider.value()
        mode = "simple" if self.radio_simple.isChecked() else "general"
        self.accept()  # Closes setup window
        self.game = SOSGame(size, mode)
        self.game.show()

    def center_window(self):
        """Centers the setup window on the screen."""
        screen_geometry = self.screen().availableGeometry()
        self.move(
            screen_geometry.center().x() - self.width() // 2,
            screen_geometry.center().y() - self.height() // 2
        )

class SOSGame(QMainWindow):
    def __init__(self, size=10, mode="simple"):
        super().__init__()
        self.logic = SOSGameLogic(size, mode)  # Game logic instance
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"SOS Game ({self.logic.mode.capitalize()} Mode) - {self.logic.size}x{self.logic.size}")
        self.setGeometry(400, 400, 600, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        
        # Game Mode Label
        self.mode_label = QLabel(f"<b>Game Mode: </b>{self.logic.mode.capitalize()}")
        self.mode_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.mode_label)

        # Player Turn Label
        self.label = QLabel()
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.update_label()
        self.layout.addWidget(self.label)
        
        # Scoreboard for tracking SOS counts
        self.scoreboard = QLabel("")
        self.scoreboard.setFont(QFont("Arial", 14, QFont.Bold))
        self.update_scoreboard()  # Initialize scoreboard display
        self.layout.addWidget(self.scoreboard)

        self.grid_layout = QGridLayout()
        self.buttons = [[None for _ in range(self.logic.size)] for _ in range(self.logic.size)]
        
        for row in range(self.logic.size):
            for col in range(self.logic.size):
                btn = QPushButton(" ")
                btn.setFixedSize(500 // self.logic.size, 500 // self.logic.size)
                btn.clicked.connect(lambda _, r=row, c=col: self.make_move(r, c))
                self.grid_layout.addWidget(btn, row, col)
                self.buttons[row][col] = btn
        
        self.layout.addLayout(self.grid_layout)
        self.central_widget.setLayout(self.layout)
    
    def update_label(self):
        piece = "S" if self.logic.current_player == "Blue" else "O"
        color = "Blue" if self.logic.current_player == "Blue" else "Red"
        self.label.setText(f"Current Player: <span style='color:{color};'>{self.logic.current_player} ({piece})</span>")

    def make_move(self, row, col):
        result = self.logic.make_move(row, col)
        # Ensure button reflects board changes
        self.buttons[row][col].setText(self.logic.board[row][col])
        self.update_label()
        self.update_scoreboard()
        self.update()

        if result == "blue_wins":
            self.show_game_over_message("Blue Wins!")
        elif result == "red_wins":
            self.show_game_over_message("Red Wins!")
        elif result == "draw":
            self.show_game_over_message("It's a draw!")
            
    def update_scoreboard(self):
        """Updates the scoreboard UI."""
        blue_score = self.logic.scores["Blue"]
        red_score = self.logic.scores["Red"]
        self.scoreboard.setText(f"Score - Blue: {blue_score} | Red: {red_score}")

    def show_game_over_message(self, message):
        """Displays a message box when the game ends."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        response = msg_box.exec_()

        if response == QMessageBox.Ok:
            self.restart_game()
        else:
            self.close()  # Close the game window

    def restart_game(self):
        """Restarts the game by resetting the board."""
        self.logic = SOSGameLogic(self.logic.size, self.logic.mode)
        self.update_label()
        
        # Reset button text
        for row in range(self.logic.size):
            for col in range(self.logic.size):
                self.buttons[row][col].setText(" ")
        
        self.update()  # Refreshes the UI