import unittest
from sosGameLogic import SOSGameLogic
from sosGui import SetupWindow
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication
class TestSOSGame(unittest.TestCase):

    def setUp(self):
        """Set up a small 5x5 game instance for testing."""
        # Initialize QApplication before creating any QWidget
        self.app = QApplication([])  # QApplication is needed for PyQt widgets
        self.game = SOSGameLogic(5, "simple")

    def test_is_sos(self):
        """Test if the is_sos function correctly detects an SOS sequence."""
        # SOS sequence in a row
        self.game.board[2][1] = 'S'
        self.game.board[2][2] = 'O'
        self.game.board[2][3] = 'S'

        # Print board to inspect
        print("Board state before checking SOS (test_is_sos):")
        for row in self.game.board:
            print(row)

        # Check horizontal SOS detection
        self.assertTrue(self.game.is_sos(2, 1, 0, 1))  # Left 'S'
        self.assertTrue(self.game.is_sos(2, 2, 0, 1))  # Middle 'O'
        self.assertTrue(self.game.is_sos(2, 3, 0, -1))  # Right 'S'

        # No SOS should be detected at an empty spot
        self.assertFalse(self.game.is_sos(1, 1, 0, 1))  # No valid SOS here

    def test_check_sos(self):
        """Test if the check_sos function correctly identifies SOS patterns."""
        
        # Set up a valid SOS sequence (in a row)
        self.game.board[1][1] = 'S'
        self.game.board[1][2] = 'O'
        self.game.board[1][3] = 'S'

        print("Board state before checking SOS (test_check_sos):")
        for row in self.game.board:
            print(row)

        # Test all parts of the SOS sequence
        self.assertTrue(self.game.check_sos(1, 1))  # Left 'S'
        self.assertTrue(self.game.check_sos(1, 2))  # Middle 'O'
        self.assertTrue(self.game.check_sos(1, 3))  # Right 'S'

        # No SOS should be detected in an empty position
        self.assertFalse(self.game.check_sos(0, 0))  # Top-left empty space

        # Test another case where no SOS is present (incorrect pattern)
        self.game.board[0][0] = 'S'
        self.game.board[0][1] = 'O'
        self.game.board[0][2] = 'O'  # Wrong pattern
        self.assertFalse(self.game.check_sos(0, 1))  # Should NOT detect SOS
    def test_make_move_valid(self):
        """Test if a valid move updates the board and switches players correctly."""
        row, col = 2, 2  # Choose a valid position

        # Blue makes a move (should place 'S')
        result = self.game.make_move(row, col)
        self.assertTrue(result or result is False)  # Should return True (SOS) or False (valid move)

        # Verify board update
        self.assertEqual(self.game.board[row][col], "S")  # Blue's turn places 'S'

        # Verify player switch
        self.assertEqual(self.game.current_player, "Red")  # Turn should switch to Red

    def test_make_move_invalid(self):
        """Test that an invalid move (occupied space) is rejected."""
        row, col = 1, 1

        # Blue makes a valid move
        self.game.make_move(row, col)

        # Red tries to move in the same spot
        result = self.game.make_move(row, col)
        self.assertFalse(result)  # Move should be rejected

        # Ensure board is unchanged
        self.assertEqual(self.game.board[row][col], "S")  # Still 'S' from Blue's turn

        # Ensure turn does not switch
        self.assertEqual(self.game.current_player, "Red")  # Red's turn should not proceed

    def test_make_move_sos(self):
        """Test if a move that forms SOS is detected correctly."""
        # Set up an SOS pattern manually
        self.game.board[2][1] = "S"
        self.game.board[2][2] = "O"

        # Blue places 'S' at (2,3) to form "S-O-S"
        result = self.game.make_move(2, 3)
        self.assertTrue(result)  # Should return True (SOS detected)

        # Ensure board update
        self.assertEqual(self.game.board[2][3], "S")

    def test_make_move_out_of_bounds(self):
        """Test that moves outside the board are rejected."""
        result = self.game.make_move(-1, 2)  # Negative index
        self.assertFalse(result)

        result = self.game.make_move(5, 2)  # Out of range
        self.assertFalse(result)
class TestSetupWindow(unittest.TestCase):
    def setUp(self):
        """Initialize QApplication and SetupWindow."""
        self.app = QApplication([])  # QApplication is needed for PyQt widgets
        self.window = SetupWindow()

    @patch("sosGui.SOSGame")  # Mock the SOSGame class to track calls
    def test_start_game(self, MockSOSGame):
        """Test that start_game() initializes the game correctly."""
        
        # Mock UI interactions
        self.window.size_slider.setValue(8)  # Simulate user selecting board size 8
        self.window.radio_simple.setChecked(True)  # Simulate choosing "simple" mode
        
        # Mock accept() to prevent actual closing
        self.window.accept = MagicMock()
        
        # Call start_game()
        self.window.start_game()

        # Assertions
        MockSOSGame.assert_called_once_with(8, "simple")  # Ensure game initialized with correct values
        game_instance = MockSOSGame.return_value
        game_instance.show.assert_called_once()  # Ensure show() was called
        self.window.accept.assert_called_once()  # Ensure accept() was called (closing window)

    @patch("sosGui.SOSGame")
    def test_start_game_general_mode(self, MockSOSGame):
        """Test start_game() with 'general' mode selection."""
        
        # Mock UI interactions
        self.window.size_slider.setValue(12)  # Set size to 12
        self.window.radio_general.setChecked(True)  # Choose "general" mode
        
        self.window.accept = MagicMock()  # Mock accept()
        
        self.window.start_game()

        # Assertions
        MockSOSGame.assert_called_once_with(12, "general")  # Correct game settings
        MockSOSGame.return_value.show.assert_called_once()  # Ensure game UI is shown
        self.window.accept.assert_called_once()  # Ensure setup window closes

if __name__ == '__main__':
    unittest.main(verbosity=2)