import sys
from PyQt5.QtWidgets import QApplication
from modules.visualization import MemoryWindow

def main():
    app = QApplication(sys.argv)
    window = MemoryWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()