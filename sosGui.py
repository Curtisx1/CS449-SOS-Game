from PyQt5.QtWidgets import (QMainWindow, QPushButton, 
                             QGridLayout, QWidget, QVBoxLayout, QLabel, 
                             QRadioButton, QDialog,
                             QHBoxLayout, QSlider, QMessageBox, QButtonGroup)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from sosGameLogic import SOSGameLogic, ComputerPlayer

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
        self.size_slider.setValue(3)
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
        self.size_label = QLabel("Board Size: 3")
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

        # Player selection label
        player_label = QLabel("Select Player Types:")
        player_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(player_label)

       # Blue Player selection
        blue_layout = QHBoxLayout()
        blue_label = QLabel("Blue Player:")
        blue_label.setFont(QFont("Arial", 11))
        self.blue_human = QRadioButton("Human")
        self.blue_computer = QRadioButton("Computer")
        self.blue_human.setChecked(True)  # Default selection

        # Blue button group
        self.blue_group = QButtonGroup(self)
        self.blue_group.addButton(self.blue_human)
        self.blue_group.addButton(self.blue_computer)

        blue_layout.addWidget(blue_label)
        blue_layout.addWidget(self.blue_human)
        blue_layout.addWidget(self.blue_computer)
        layout.addLayout(blue_layout)


        # Red Player selection
        red_layout = QHBoxLayout()
        red_label = QLabel("Red Player:")
        red_label.setFont(QFont("Arial", 11))
        self.red_human = QRadioButton("Human")
        self.red_computer = QRadioButton("Computer")
        self.red_human.setChecked(True)  # Default selection

        # Red button group
        self.red_group = QButtonGroup(self)
        self.red_group.addButton(self.red_human)
        self.red_group.addButton(self.red_computer)

        red_layout.addWidget(red_label)
        red_layout.addWidget(self.red_human)
        red_layout.addWidget(self.red_computer)
        layout.addLayout(red_layout)

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

        blue_type = "computer" if self.blue_computer.isChecked() else "human"
        red_type = "computer" if self.red_computer.isChecked() else "human"

        self.accept()  # Closes setup window
        self.game = SOSGame(size, mode, blue_type, red_type)
        self.game.show()

    def center_window(self):
        """Centers the setup window on the screen."""
        screen_geometry = self.screen().availableGeometry()
        self.move(
            screen_geometry.center().x() - self.width() // 2,
            screen_geometry.center().y() - self.height() // 2
        )

class SOSGame(QMainWindow):
    def __init__(self, size=3, mode="simple", blue_type="human", red_type="human"):
        super().__init__()

        self.blue_type = blue_type
        self.red_type = red_type

        # Create game logic
        self.logic = SOSGameLogic(size, mode)

        # Assign computer player if selected
        if blue_type == "computer":
            self.logic.computer = ComputerPlayer(player_color="Blue")
        elif red_type == "computer":
            self.logic.computer = ComputerPlayer(player_color="Red")

        self.initUI()

        if self.logic.computer and self.logic.current_player == self.logic.computer.player_color:
            QTimer.singleShot(250, self.handle_computer_turn)

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
        self.buttons[row][col].setText(self.logic.board[row][col])
        self.update_label()
        self.update_scoreboard()

        if result in ("blue_wins", "red_wins", "draw"):
            self.show_game_over_message(self.get_result_message(result))
            return

        if self.logic.computer and self.logic.current_player == self.logic.computer.player_color:
            QTimer.singleShot(500, self.handle_computer_turn)

    def handle_computer_turn(self):
        move = self.logic.computer.choose_move(self.logic)
        if move:
            row, col, letter = move
            # Pass explicit letter chosen by the AI
            result = self.logic.make_move(row, col, letter)

            self.buttons[row][col].setText(self.logic.board[row][col])
            self.update_label()
            self.update_scoreboard()
            self.update()

            # Show result if game is over
            if result in ("blue_wins", "red_wins", "draw"):
                self.show_game_over_message(self.get_result_message(result))
            else:
                # If next player is also computer, keep going
                if self.logic.current_player == "Blue" and self.blue_type == "computer":
                    QTimer.singleShot(250, self.handle_computer_turn)
                elif self.logic.current_player == "Red" and self.red_type == "computer":
                    QTimer.singleShot(250, self.handle_computer_turn)

    def get_result_message(self, result):
        if result == "blue_wins":
            return "Blue Wins!"
        elif result == "red_wins":
            return "Red Wins!"
        return "It's a draw!"
            
    def update_scoreboard(self):
        if self.logic.mode == "simple":
            self.scoreboard.setText("")
        else:
            blue = self.logic.scores["Blue"]
            red = self.logic.scores["Red"]
            self.scoreboard.setText(f"Score - Blue: {blue} | Red: {red}")


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