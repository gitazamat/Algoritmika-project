from PyQt5.QtWidgets import (
    QWidget, QApplication, QTextEdit, QHBoxLayout,
    QVBoxLayout, QListWidget, QPushButton, QLineEdit,
    QLabel)

style = """
QListWidget, QTextEdit, QLineEdit {
    border: 1px solid black;
    border-radius: 5px;
    padding: 5px;
}

QPushButton {
    background-color: gray;
    color: black;
    border-radius: 5px;
    padding: 10px;
}

QPushButton:hover {
    background-color: skyblue;
}

QLabel, QPushButton {
    font-weight: bold;
}"""

#ИНТЕРФЕЙС ПРИЛОЖЕНИЯ
app = QApplication([]) # создаем приложение
window = QWidget()     # создаем главное окно
window.setWindowTitle('Гениальные заметки') #меняем заголовок окна
window.resize(900,600)
window.setStyleSheet(style)
text_field = QTextEdit() # поле для ввода текста
#часть интерфейса для управления заметками
notes_info = QLabel('Список заметок:')
notes_list = QListWidget() # создаем список с заметками
create_note = QPushButton('Создать заметку')
delete_note = QPushButton('Удалить заметку')
save_note = QPushButton('Сохранить заметку')
#часть интерфейса для управления тегами
tags_info = QLabel('Список тегов:')
tags_list = QListWidget() # создаем список с заметками
create_tag = QPushButton('Создать тег')
delete_tag = QPushButton('Удалить тег')
search_tag = QPushButton('Поиск')
search_field = QLineEdit('')
#РАЗМЕЩЕНИЕ ИНТЕРФЕЙСА
main_layout = QHBoxLayout() # создаем главную линию
main_layout.addWidget(text_field) # добавляем виджет
v_line = QVBoxLayout() # создаем линию для правой части экрана
h1_line = QHBoxLayout() # new
h2_line = QHBoxLayout() #new
#добовляем все что связано с заметками
v_line.addWidget(notes_info)
v_line.addWidget(notes_list)
h1_line.addWidget(create_note) # new
h1_line.addWidget(delete_note) # new
v_line.addLayout(h1_line) # new
v_line.addWidget(save_note)
#добовляем все что связано с тегами
v_line.addWidget(tags_info)
v_line.addWidget(tags_list)
v_line.addWidget(search_field)
h2_line.addWidget(create_tag) # new
h2_line.addWidget(delete_tag) # new
v_line.addLayout(h2_line) # new
v_line.addWidget(search_tag)
#размещение второстепенных линий
main_layout.addLayout(v_line)

#ЗАПУСК ПРИЛОЖЕНИЯ
window.setLayout(main_layout) # установка главной линии
window.show() # отображение окна
app.exec() # не закрывать приложение пока не нажмем на крестик