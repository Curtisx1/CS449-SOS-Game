class SOSGameLogic:
    def __init__(self, size=10, mode="simple"):
        self.size = size
        self.mode = mode
        self.board = [['-' for _ in range(size)] for _ in range(size)]
        self.current_player = "Blue"
        self.sos_lines = []

    def switch_player(self):
        """Switches the current player."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"

    def is_valid_move(self, row, col):
        """Checks if a move is valid."""
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == '-'

    def make_move(self, row, col):
        """Handles a move on the board."""
        if not self.is_valid_move(row, col):
            return False  # Invalid move (out of bounds or already occupied)

        letter = "S" if self.current_player == "Blue" else "O"
        self.board[row][col] = letter

        found_sos = self.check_sos(row, col)

        # In "general" mode, the player continues playing if they form an SOS
        if self.mode == "general" and found_sos:
            return True

        self.switch_player()
        return found_sos

    def check_sos(self, row, col):
        """Checks if the move creates an SOS sequence from any of its parts."""
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Horizontal, vertical, diagonal, anti-diagonal
        found_sos = False

        for dr, dc in directions:
            if self.is_sos(row, col, dr, dc):
                self.sos_lines.append(((row, col), (row + 2*dr, col + 2*dc)))
                found_sos = True
            if self.is_sos(row, col, -dr, -dc):  # Check reverse direction
                self.sos_lines.append(((row - 2*dr, col - 2*dc), (row, col)))
                found_sos = True

        return found_sos

    def is_sos(self, row, col, dr, dc):
        """Checks for an SOS sequence in a given direction."""
        # Forward check: S-O-S pattern
        if (0 <= row + 2*dr < self.size and 0 <= col + 2*dc < self.size and
            self.board[row][col] == "S" and
            self.board[row + dr][col + dc] == "O" and
            self.board[row + 2*dr][col + 2*dc] == "S"):
            return True

        # Reverse check: S-O-S pattern in the opposite direction
        if (0 <= row - dr < self.size and 0 <= col - dc < self.size and
            0 <= row + dr < self.size and 0 <= col + dc < self.size and
            self.board[row][col] == "O" and
            self.board[row - dr][col - dc] == "S" and
            self.board[row + dr][col + dc] == "S"):
            return True

        return False