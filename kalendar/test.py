from PyQt5.QtWidgets import *
import sys

clicks = 0

def on_button_click():
    global clicks
    clicks += 1
    label.setText(f"Clicks - {clicks}")
    if clicks in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                  2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                  11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                  30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 1000000]:
        QMessageBox.information(window, f'Нажатие на кнопку {clicks} раз',
                                f'Поздравляю! \nВы нажали на кнопку {clicks} раз!')

def reset_button():
    global clicks
    clicks = 0
    label.setText(f"Clicks - {clicks}")
    QMessageBox.information(window, 'Сброс', "Сброс прогресса завершен!")

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Счётчик кликов")

button = QPushButton("Нажми на меня!", window)
button.clicked.connect(on_button_click)
button.show()

button2 = QPushButton('Сброс', window)
button2.move(200, 0)
button2.clicked.connect(reset_button)
button2.show()

label = QLabel(f"Clicks - {clicks}", window)
label.move(130, 0)
label.show()

window.show()
sys.exit(app.exec_())
