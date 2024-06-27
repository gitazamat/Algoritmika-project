import json
from PyQt5.QtWidgets import (
    QWidget, QApplication, QTextEdit, QHBoxLayout,
    QVBoxLayout, QListWidget, QPushButton, QLineEdit,
    QLabel, QInputDialog)


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
main_layout.addLayout(v_line)
# ФУНКЦИОНАЛ

def show_note():
    key = notes_list.selectedItems()[0].text()
    text_field.setText(notes[key]['текст'])
    tags_list.clear() # надо поигратся
    tags_list.addItems(notes[key]['теги'])

def add_note():
    note_name, ok = QInputDialog().getText(window,'Добавить заметку','Название заметки: ')
    if note_name != '':
        notes[note_name] = {"текст": "", "теги": []}
        with open('notes.json', 'w',encoding='UTF-8') as file:
            json.dump(notes,file,ensure_ascii=False)
        notes_list.addItem(note_name)

def safe_note():
     key = notes_list.selectedItems()[0].text()
     text = text_field.toPlainText()
     notes[key]['текст'] = text
     with open('notes.json', 'w',encoding='UTF-8') as file:
        json.dump(notes,file,ensure_ascii=False)
def del_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        del notes[key]
        with open('notes.json', 'w',encoding='UTF-8') as file:
            json.dump(notes,file,ensure_ascii=False)
        notes_list.clear()
        tags_list.clear()
        text_field.clear()
        notes_list.addItems(notes)
def add_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = search_field.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            tags_list.clear
            tags_list.addItems(notes[key]['теги'])
        with open('notes.json', 'w',encoding='UTF-8') as file:
            json.dump(notes,file,ensure_ascii=False)

def del_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()   
        tag = tags_list.selectedItems()[0].text() 
        if not tag in notes[key]['теги'] and tag != '': 
            notes[key]['теги'].remove(tag)
            tags_list.clear
            tags_list.addItems(notes[key]['теги'])
            with open('notes.json', 'w',encoding='UTF-8') as file:
                json.dump(notes,file,ensure_ascii=False)
def search():
    tag = search_field.text()
    if search_tag.text() == 'Поиск' and tag != ' ':
        notes_filtred = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtred[note] = notes[note]
        search_field.clear()
        notes_list.clear()
        tags_list.clear()

        notes_list.addItems(notes_filtred)                      
        search_tag.setText('Сбросить')

    elif search_tag.text() == 'Сбросить':
        search_field.clear()
        notes_list.clear()
        tags_list.clear()

        notes_list.addItems(notes)
        search_tag.setText('Поиск')   

# ПОДПИСКИ НА СОБЫТИЯ
notes_list.itemClicked.connect(show_note)
create_note.clicked.connect(add_note)
save_note.clicked.connect(safe_note)
delete_note.clicked.connect(del_note)
create_tag.clicked.connect(add_tag)
delete_tag.clicked.connect(del_tag)
search_tag.clicked.connect(search)
#ЗАПУСК ПРИЛОЖЕНИЯ
with open('notes.json','r',encoding='UTF-8') as file:
    notes = json.load(file)

notes_list.addItems(notes)


window.setLayout(main_layout) # установка главной линии
window.show() # отображение окна
app.exec() # не закрывать приложение пока не нажмем на крестик

