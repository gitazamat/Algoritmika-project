import os
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,QFileDialog)

app = QApplication([])

# Создание основного окна
window = QWidget()
window.resize(700, 500)
window.setWindowTitle('Типо фотошоп')

# Создание виджетов
folder = QPushButton('Папка')
files = QListWidget()

image = QLabel('Картинка')
left = QPushButton('Лево')
right = QPushButton('Право')
flip = QPushButton('Зеркало')
sharp = QPushButton('Резкость')
gray = QPushButton('Ч\Б')

# Размещение виджетов
main_layout = QHBoxLayout()

# Левая часть
col1 = QVBoxLayout()
col1.addWidget(folder)
col1.addWidget(files)
main_layout.addLayout(col1)

# Правая часть
col2 = QVBoxLayout()
col2.addWidget(image)

# Линия кнопок
btn_layout = QHBoxLayout()
btn_layout.addWidget(left)
btn_layout.addWidget(right)
btn_layout.addWidget(flip)
btn_layout.addWidget(sharp)
btn_layout.addWidget(gray)
col2.addLayout(btn_layout)

# Добавление правой части в основной layout
main_layout.addLayout(col2)

# Применение стилей с помощью QSS (Qt Style Sheets)
style = """
QWidget {
    background-color: #f0f0f0; /* Цвет фона для всех виджетов */
    font-family: Arial, sans-serif; /* Шрифт */
}

QPushButton {
    background-color: #4CAF50; /* Цвет фона */
    color: white; /* Цвет текста */
    border: 1px solid #4CAF50; /* Граница */
    border-radius: 4px; /* Закругление углов */
    padding: 5px 10px; /* Отступы внутри кнопки */
    min-width: 80px; /* Минимальная ширина кнопки */
}

QPushButton:hover {
    background-color: #45a049; /* Цвет фона при наведении */
    border-color: #45a049; /* Цвет границы при наведении */
}

QListWidget {
    background-color: white; /* Цвет фона для QListWidget */
    border: 1px solid #ddd; /* Граница */
}

QLabel {
    font-size: 18px; /* Размер шрифта */
    font-weight: bold; /* Жирный шрифт */
    margin-bottom: 10px; /* Отступ снизу */
}
"""
#Функционал
def show_files():
    workdir = QFileDialog.getExistingDirectory()
    print(workdir)
    filenames = os.listdir(workdir)
    files.clear()
    for file in filenames:
        for ext in ['.jpg','.jpeg','.png']:
            if file.endswith(ext):
                files.addItem(file)

    #files.addItems(filenames)

#Подписки
folder.clicked.connect(show_files)
# Применение стилей к главному окну
window.setStyleSheet(style)

# Установка основного layout для окна и отображение окна
window.setLayout(main_layout)
window.show()

# Запуск приложения
app.exec()


#my teacher's git hub  https://github.com/AlgoClassWork/python_start_classwork/tree/main
