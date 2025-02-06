import unittest
from SosMain import SOSGame
from PyQt5.QtWidgets import QApplication

class TestSOSGame(unittest.TestCase):

    def setUp(self):
        """Set up a small 5x5 game instance for testing."""
        # Initialize QApplication before creating any QWidget
        self.app = QApplication([])
        
        self.game = SOSGame(size=5)
        
    def test_is_sos(self):
        """Test if the is_sos function correctly detects an SOS sequence."""
        # SOS sequence in a row
        self.game.board[2][1] = 'S'
        self.game.board[2][2] = 'O'
        self.game.board[2][3] = 'S'
        
        self.assertTrue(self.game.is_sos(2, 1, 0, 1))  # Horizontal SOS
        self.assertTrue(self.game.is_sos(2, 3, 0, -1))  # Reverse check
        
        # No SOS is present
        self.assertFalse(self.game.is_sos(1, 1, 0, 1))

    def test_check_sos(self):
        """Test if the check_sos function correctly identifies SOS patterns."""
        # SOS sequence in a row
        self.game.board[1][1] = 'S'
        self.game.board[1][2] = 'O'
        self.game.board[1][3] = 'S'
        
        self.assertTrue(self.game.check_sos(1, 1))  # Should detect an SOS
        self.assertTrue(self.game.check_sos(1, 2))  # Middle 'O' should also detect
        self.assertTrue(self.game.check_sos(1, 3))  # Right 'S' should detect
        
        # No SOS is present
        self.assertFalse(self.game.check_sos(0, 0))

if __name__ == '__main__':
    unittest.main()