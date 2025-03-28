class SOSGameLogic:
    def __init__(self, size=10, mode="simple"):
        self.size = size
        self.mode = mode
        self.board = [['-' for _ in range(size)] for _ in range(size)]
        self.current_player = "Blue"
        self.sos_lines = set()
        self.scores = {"Blue": 0, "Red": 0}

    def switch_player(self):
        """Switches the current player."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"

    def is_valid_move(self, row, col):
        """Checks if a move is valid."""
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == '-'

    def make_move(self, row, col):
        """Processes a move and updates the game state."""
        letter = "S" if self.current_player == "Blue" else "O"
        self.board[row][col] = letter

        found_sos = self.check_sos(row, col)

        # **Simple Mode: First SOS wins immediately**
        if self.mode == "simple" and found_sos:
            return self.current_player.lower() + "_wins"  # "blue_wins" or "red_wins"

        if not found_sos:
            self.switch_player()  # Only switch if no SOS found

        # **Check for a draw in Simple Mode**
        if self.mode == "simple" and self.is_board_full():
            return "draw"

        # **General Mode: Continue the game**
        if self.is_board_full():
            return self.determine_winner()

        return "continue"

    def check_sos(self, row, col):
        """Checks if an SOS sequence is formed at the given position."""
        directions = [
            (0, 1), (1, 0), (1, 1), (-1, 1),  # Forward directions
            (0, -1), (-1, 0), (-1, -1), (1, -1)  # Backward directions
        ]

        found_sos = False

        for dr, dc in directions:
            sos_line = self.find_sos_line(row, col, dr, dc)
            if sos_line:
                line_key = tuple(sorted(sos_line))
                if line_key not in self.sos_lines:
                    self.sos_lines.add(line_key)
                    self.scores[self.current_player] += 1
                    found_sos = True

        return found_sos

    def find_sos_line(self, row, col, dr, dc):
        """Finds a complete SOS line in a given direction."""
        for start_offset in range(-1, 2):
            start_row = row + start_offset * dr
            start_col = col + start_offset * dc
            end_row = start_row + 2 * dr
            end_col = start_col + 2 * dc

            if not (0 <= start_row < self.size and 0 <= start_col < self.size and
                    0 <= end_row < self.size and 0 <= end_col < self.size):
                continue

            first_letter = self.board[start_row][start_col]
            middle_letter = self.board[start_row + dr][start_col + dc]
            last_letter = self.board[end_row][end_col]

            if first_letter == "S" and middle_letter == "O" and last_letter == "S":
                return [(start_row, start_col), (start_row + dr, start_col + dc), (end_row, end_col)]
        
        return None

    def is_board_full(self):
        """Checks if the board is completely filled."""
        return all(cell != '-' for row in self.board for cell in row)

    def determine_winner(self):
        """Determines the winner based on scores (for General mode)."""
        blue_score = self.scores["Blue"]
        red_score = self.scores["Red"]

        if blue_score > red_score:
            return "blue_wins"
        elif red_score > blue_score:
            return "red_wins"
        return "draw"

class SimpleSOSGame(SOSGameLogic):
    def __init__(self, size=10):
        super().__init__(size, mode="simple")

class GeneralSOSGame(SOSGameLogic):
    def __init__(self, size=10):
        super().__init__(size, mode="general")

    def make_move(self, row, col):
        """Overrides make_move to properly check for the winner in General mode."""
        result = super().make_move(row, col)

        if self.is_board_full():
            return self.determine_winner()

        return result