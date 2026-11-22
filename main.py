import sys
from PyQt6.QtWidgets import QApplication
from controllers.task_controller import TaskController
from views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    controller = TaskController()
    window = MainWindow(controller)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()