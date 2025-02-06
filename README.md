# CS449-SOS-Game

Problem Description
Your customer asks you to develop the software that allows a blue player to play the SOS game against a red player. Either player can be human or computer.    

The game board is a grid of nxn (n>2) squares. The two players take turns to add either an "S" or an "O" to an unoccupied square, with no requirement to use the same letter each turn. Each player attempts to create the straight sequence S-O-S among connected squares (diagonally, horizontally, or vertically). To keep track of who made which SOSs, a line in the player’s color (i.e., blue or red) is drawn for each SOS sequence, as shown in the following figure.

![image](https://github.com/user-attachments/assets/68fc682f-aeb9-48ad-8b51-de21cdc8ce7f)



			Figure 1. Sample GUI layout of the final product
The instructions of each assignment may include a sample graphical user interface (GUI). As GUI is a topic in CS 101, you are strongly encouraged to implement a GUI for the SOS game.  The use of an interactive console interface is strongly discouraged. The TicTacToe case study to be introduced in class is an excellent example to follow. 
The SOS game can be played in one of the following modes: 
(a)	Simple game: The player who creates the first SOS is the winner. If no SOS is created when the board has been filled up, then the game is a draw. Turns alternate between players after each move.
(b)	General game: The game continues until the board has been filled up. The winner is the player who made the most SOSs. If both players made the same number of SOSs, then the game is a draw. When a player succeeds in creating an SOS, that player immediately takes another turn and continues to do so until no SOS is created on their turn. Otherwise, turns alternate between players after each move.


## Test Command (UnitTest)

- **SosMain.py**: Main program (GUI + Game Logic)
- **SosUnitTest.py**: Contains unit tests

To run the unit tests, use the following command:

python -m unittest -v SosUnitTest
