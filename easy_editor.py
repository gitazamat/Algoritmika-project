import os
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,
    QFileDialog)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter

app = QApplication([])

# Создание основного окна
window = QWidget()
window.resize(700, 500)
window.setWindowTitle('Фотошоп на минималках')

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
# Нужные переменные 

workdir = ''
current_image = None
current_filename = None
save_dir = 'Modified/'

# Функционал
def show_files():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    filenames = os.listdir(workdir)
    files.clear()
    for file in filenames:
        if file.endswith('.jpeg') or file.endswith('.png'):
            files.addItem(file)
  
def show_chosen_image():
    filename = files.currentItem().text()
    load_image(filename)
    show_image(os.path.join(workdir, filename))

def load_image(filename):
    global current_image, current_filename
    current_filename = filename
    fullname = os.path.join(workdir, filename)
    current_image = Image.open(fullname)

def show_image(path):
    pixmapimage = QPixmap(path)
    w, h = image.width(), image.height()
    pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
    image.setPixmap(pixmapimage)

def save_image():
    global current_image
    path = os.path.join(workdir,save_dir)
    if not (os.path.exists(path) or os.path.isdir(path)):
        os.mkdir(path)
    fullname = os.path.join(path,current_filename)
    current_image.save(fullname)
def do_left():
    global current_image
    current_image = current_image.transpose(Image.ROTATE_90)
    save_image()
    image_path = os.path.join(workdir,save_dir,current_filename)
    show_image(image_path)

def do_right():
    global current_image
    current_image = current_image.transpose(Image.ROTATE_270)
    save_image()
    image_path = os.path.join(workdir,save_dir,current_filename)
    show_image(image_path)

def do_flip():
    global current_image
    current_image = current_image.transpose(Image.FLIP_LEFT_RIGHT)
    save_image()
    image_path = os.path.join(workdir,save_dir,current_filename)
    show_image(image_path)    

def do_sharp():
    global current_image
    current_image = current_image.filter(ImageFilter.SHARPEN)
    save_image()
    image_path = os.path.join(workdir,save_dir,current_filename)
    show_image(image_path)

def do_gray():
    global current_image
    current_image = current_image.convert('L')
    save_image()
    image_path = os.path.join(workdir,save_dir,current_filename)
    show_image(image_path)

# Подписки
files.currentRowChanged.connect(show_chosen_image)
folder.clicked.connect(show_files)
left.clicked.connect(do_left)
right.clicked.connect(do_right)
flip.clicked.connect(do_flip)
sharp.clicked.connect(do_sharp)
gray.clicked.connect(do_gray)
# Применение стилей к главному окну
window.setStyleSheet(style)

# Установка основного layout для окна и отображение окна
window.setLayout(main_layout)
window.show()

# Запуск приложения
app.exec()
