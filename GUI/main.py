import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from yoloV5.custom_detect import main

def on_button_click():
    diameter,sticks=main()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create a main window
    window = QWidget()
    window.setWindowTitle("Simple Button Example")
    window.setGeometry(100, 100, 300, 200)  # Set window position (x, y) and size (width, height)

    # Create a button
    button = QPushButton("Click Me!", window)
    button.setGeometry(100, 50, 100, 30)  # Set button position (x, y) and size (width, height)
    
    # Connect button's clicked signal to the callback function
    button.clicked.connect(on_button_click)
    
    # Show the window
    window.show()
    
    # Start the event loop
    sys.exit(app.exec_())
