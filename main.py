import sys
from PyQt5.QtWidgets import QApplication
from sosGui import SetupWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setup = SetupWindow()
    if setup.exec_():  # Show setup window and wait for user input
        sys.exit(app.exec_())