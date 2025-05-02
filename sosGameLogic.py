from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Optional
class SOSGameLogic:
    def __init__(self, size=3, mode="simple", computer_player=None):
        self.computer = computer_player
        self.size = size
        self.mode = mode
        self.board = [['-' for _ in range(size)] for _ in range(size)]
        self.current_player = "Blue"
        self.sos_lines = set()
        self.scores = {"Blue": 0, "Red": 0}
        self.size: int = size
        self.mode: str = mode

        # live-log attributes
        self._record_path: Optional[Path] = None
        self._record_dict: Optional[Dict] = None

        # initialise board + open first log
        self.reset_board()

    def reset_board(self, start_logging = True):
        # clear in-memory state
        self.board  = [["-" for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = "Blue"
        self.sos_lines.clear()
        self.scores = {"Blue": 0, "Red": 0}

    def start_recording(self, path: str | Path):
        """Begin writing moves to <path> (JSON). Overwrites if it exists."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)   # make sure folder exists
        self._init_live_log(path)                       # reuse the existing helper

    def stop_recording(self):
        """Flush and close the current log (called automatically at game end)."""
        if self._record_path:
            self._flush_log()
            self._record_path = None
            self._record_dict = None

    def _init_live_log(self, path: Path) -> None:
        self._record_path = path
        self._record_dict = {
            "format": "sos-log-json-v1",
            "size": self.size,
            "mode": self.mode,
            "moves": []
        }
        self._flush_log()

    def _append_move(self, row: int, col: int, letter: str) -> None:
        if self._record_dict is not None:
            self._record_dict["moves"].append({
                "row": row,
                "col": col,
                "letter": letter,
                "player": self.current_player
            })
            self._flush_log()

    def _flush_log(self) -> None:
        if self._record_path and self._record_dict is not None:
            with self._record_path.open("w", encoding="utf-8") as fp:
                json.dump(self._record_dict, fp, indent=2)

    def _finalize_if_over(self, result: str) -> str:
        """Close the log if the game is no longer running."""
        if result != "continue" and self._record_path:
            self._flush_log()
            self._record_path = None
            self._record_dict = None
        return result

    def switch_player(self):
        """Switches the current player."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"

    def is_valid_move(self, row, col):
        """Checks if a move is valid."""
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == '-'

    def make_move(self, row, col, letter=None):
        if not self.is_valid_move(row, col):
            raise ValueError(f"Invalid move at ({row}, {col})")

        if letter is None:
            letter = "S" if self.current_player == "Blue" else "O"

        self.board[row][col] = letter
        found_sos = self.check_sos(row, col)

        self._append_move(row, col, letter)

        if self.mode == "simple":
            if found_sos:
                return self._finalize_if_over(
                    f"{self.current_player.lower()}_wins"
                )
            if self.is_board_full():
                return self._finalize_if_over("draw")

        if not found_sos:
            self.switch_player()

        if self.is_board_full():
            return self._finalize_if_over(self.determine_winner())
        return "continue"

    def check_sos(self, row, col):
        """Checks if an SOS sequence is formed at the given position."""
        directions = [
            (0, 1), 
            (1, 0),
            (1, 1), 
            (-1, 1),
            (0, -1),
            (-1, 0),
            (-1, -1),
            (1, -1),
        ]

        found_sos = False

        for dr, dc in directions:
            sos_line = self.find_sos_line(row, col, dr, dc)
            if sos_line:
                found_sos = True
                line_key = tuple(sorted(sos_line))
                if line_key not in self.sos_lines:
                    self.sos_lines.add(line_key)
                    if self.mode == "general":
                        self.scores[self.current_player] += 1
                    found_sos = True

        return found_sos

    def find_sos_line(self, row, col, dr, dc):
        """Find a valid SOS sequence with (row,col) anywhere in the triplet."""
        positions = [
            (row - 2*dr, col - 2*dc),  # check if (row,col) is last S
            (row - dr, col - dc),      # check if (row,col) is middle O
            (row, col),                # check if (row,col) is first S
        ]

        for start_row, start_col in positions:
            mid_row = start_row + dr
            mid_col = start_col + dc
            end_row = start_row + 2*dr
            end_col = start_col + 2*dc

            if not all(0 <= r < self.size and 0 <= c < self.size for r, c in [(start_row, start_col), (mid_row, mid_col), (end_row, end_col)]):
                continue

            first = self.board[start_row][start_col]
            middle = self.board[mid_row][mid_col]
            last = self.board[end_row][end_col]

            if first == "S" and middle == "O" and last == "S":
                return [(start_row, start_col), (mid_row, mid_col), (end_row, end_col)]

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
    def __init__(self, size=3):
        super().__init__(size, mode="simple")

class GeneralSOSGame(SOSGameLogic):
    def __init__(self, size=3):
        super().__init__(size, mode="general")

    def make_move(self, row, col):
        """Overrides make_move to properly check for the winner in General mode."""
        result = super().make_move(row, col)

        if self.is_board_full():
            return self.determine_winner()

        return result
class ComputerPlayer:
    def __init__(self, player_color="Red", strategy="minimax"):
        self.player_color = player_color
        self.strategy = strategy

    def minimax(self, game_logic, depth, is_maximizing, alpha, beta):
        if depth == 0 or game_logic.is_board_full():
            return self.evaluate_board(game_logic, self.player_color), None

        best_move = None
        max_eval = float('-inf')
        min_eval = float('inf')

        for r in range(game_logic.size):
            for c in range(game_logic.size):
                if game_logic.is_valid_move(r, c):
                    for letter in ["S", "O"]:
                        # Simulate move
                        original = game_logic.board[r][c]
                        game_logic.board[r][c] = letter

                        # Evaluate resulting board
                        score = self.evaluate_board(
                            game_logic,
                            self.player_color if is_maximizing else self.get_opponent(self.player_color)
                        )

                        # Undo move
                        game_logic.board[r][c] = original

                        if is_maximizing:
                            if score > max_eval:
                                max_eval = score
                                best_move = (r, c, letter)
                            alpha = max(alpha, score)
                            if beta <= alpha:
                                break
                        else:
                            if score < min_eval:
                                min_eval = score
                                best_move = (r, c, letter)
                            beta = min(beta, score)
                            if beta <= alpha:
                                break

        return (max_eval if is_maximizing else min_eval), best_move

    def evaluate_board(self, game_logic, player):
        opponent = self.get_opponent(player)
        player_score = self.simulate_score(game_logic, player)
        opponent_score = self.simulate_score(game_logic, opponent)
        return player_score - opponent_score

    def simulate_score(self, game_logic, player):
        temp_score = 0
        letter = "S" if player == "Blue" else "O"
        for r in range(game_logic.size):
            for c in range(game_logic.size):
                if game_logic.is_valid_move(r, c):
                    game_logic.board[r][c] = letter
                    if game_logic.check_sos(r, c):
                        temp_score += 1
                    game_logic.board[r][c] = '-'
        return temp_score

    def get_opponent(self, player):
        return "Red" if player == "Blue" else "Blue"   

    def choose_move(self, game_logic):
        # Use 'S' if it's Blue's turn, 'O' if Red's turn
        current_player = game_logic.current_player
        valid_letter = "S" if current_player == "Blue" else "O"

        _, move = self.minimax(
            game_logic,
            depth=2,
            is_maximizing=True,
            alpha=float('-inf'),
            beta=float('inf')
        )

        if move:
            return (move[0], move[1], valid_letter)
        
        return None