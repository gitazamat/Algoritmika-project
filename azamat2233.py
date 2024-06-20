from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, 
        QGroupBox, QRadioButton,  
        QPushButton, QLabel)
from random import randint, shuffle

#БАЗА ДАННЫХ
class  Question(): 
    def __init__(self,question, right_answer ,wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

question_list = [
    Question('Когда была основана Москва?', '1147', '1485', '1703', '1836'),
    Question('Кто написал "Война и мир"?', 'Лев Толстой', 'Фёдор Достоевский', 'Александр Пушкин', 'Иван Тургенев'),
    Question('Какой самый высокий город в мире?', 'Ла-Пас', 'Кузко', 'Лхаса', 'Эль-Альто'),
    Question('Какая самая длинная река в мире?', 'Амазонка', 'Нил', 'Янцзы', 'Миссисипи'),
    Question('Какой металл самый легкий?', 'Литий', 'Магний', 'Алюминий', 'Титан'),
    Question('Какой самый крупный материк на планете?', 'Евразия', 'Африка', 'Северная Америка', 'Южная Америка'),
    Question('Какой самый древний город на Земле?', 'Дамаск', 'Иерусалим', 'Афины', 'Кайро'),
    Question('Какая самая большая пустыня в мире?', 'Сахара', 'Гоби', 'Атакама', 'Калима'),
    Question('Какой самый маленький океан?', 'Северный Ледовитый', 'Индийский', 'Южный', 'Атлантический'),
    Question('Когда была Великая французская революция?', '1789-1799', '1812', '1848', '1905'),
    Question('Какой химический элемент обозначается как Fe?', 'Железо', 'Свинец', 'Медь', 'Цинк'),
    Question('Какой самый глубокий океан на планете?', 'Тихий', 'Атлантический', 'Индийский', 'Северный Ледовитый'),
    Question('Как называется химический элемент с символом Hg?', 'Ртуть', 'Серебро', 'Свинец', 'Золото'),
    Question('Какой самый высокий водопад в мире?', 'Анхель', 'Ниагара', 'Виктория', 'Игуасу'),
    Question('Какая самая длинная гора на Земле?', 'Анды', 'Гималаи', 'Рокки', 'Альпы'),
    Question('Какой самый большой остров в мире?', 'Гренландия', 'Мадагаскар', 'Борнео', 'Калимантан'),
    Question('Какой самый длинный мост в мире?', 'Даншань', 'Гёльт', 'Шанхай', 'Ванчжоу'),
    Question('Когда произошло открытие Америки Колумбом?', '1492', '1521', '1555', '1607'),
    Question('Какая самая населённая страна в мире?', 'Китай', 'Индия', 'США', 'Индонезия'),
    Question('Какой самый высокий горный хребет на планете?', 'Гималаи', 'Альпы', 'Анды', 'Кавказ')
]


#ИНТЕРФЕЙС
app = QApplication([])
window = QWidget()
window.setWindowTitle('Memo Card')
window.resize(400, 300)

btn_OK = QPushButton('Ответить') # кнопка ответа
lb_Question = QLabel('Самый сложный вопрос в мире!') # текст вопроса
#ФОРМА С ВАРИАНТАМИ ОТВЕТОВ
RadioGroupBox = QGroupBox("Варианты ответов") # группа на экране для переключателей с ответами

rbtn_1 = QRadioButton('Вариант 1')
rbtn_2 = QRadioButton('Вариант 2')
rbtn_3 = QRadioButton('Вариант 3')
rbtn_4 = QRadioButton('Вариант 4')

layout_ans2 = QVBoxLayout() # вертикальные будут внутри горизонтального
layout_ans2.addWidget(rbtn_1) # два ответа в первый столбец
layout_ans2.addWidget(rbtn_2)
layout_ans2.addWidget(rbtn_3) # два ответа во второй столбец
layout_ans2.addWidget(rbtn_4)

RadioGroupBox.setLayout(layout_ans2) # готова "панель" с вариантами ответов 

#ФОРМА С РЕЗУЛЬТАТОМ
AnsGroupBox = QGroupBox("Варианты ответов")
lb_Result = QLabel('прав ты или нет узанешь чуть чуть позже ')
lb_Correct = QLabel('жди')


layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result)
layout_res.addWidget(lb_Correct)
AnsGroupBox.setLayout(layout_res)
AnsGroupBox.hide()

#РАЗМЕЩЕНИЕ ВИДЖЕТОВ
layout_card = QVBoxLayout()
layout_card.addWidget(lb_Question)
layout_card.addWidget(RadioGroupBox)
layout_card.addWidget(AnsGroupBox)
layout_card.addWidget(btn_OK)
#ФУНКЦИОНАЛ
buttons = [rbtn_1,rbtn_2,rbtn_3,rbtn_4]
shuffle(buttons)
print(buttons) 

def ask(quest: Question):
    shuffle(buttons)
    buttons[0].setText(quest.right_answer)
    buttons[1].setText(quest.wrong1)
    buttons[2].setText(quest.wrong2)
    buttons[3].setText(quest.wrong3)
    lb_Question.setText(quest.question)
    lb_Correct.setText(quest.right_answer)

def check_answer():
    if buttons[0].isChecked():
        lb_Result.setText('Красавчик ты угадал')
    else:
        lb_Result.setText('лох ты не угадал')

    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Следуйщий вопрос')

def next_qestion():
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Ответить')

    cur_question = randint(0, len(question_list)-1)
    quest = question_list[cur_question]
    ask(quest)


def click_OK():
    if btn_OK.text() == 'Ответить':
        check_answer()#проверка ответа
    else:
        next_qestion() #следуйщий вопрос

#ПОДПИСКИ
btn_OK.clicked.connect(click_OK)
next_qestion()


#ЗАПУСК
next_qestion()

window.setLayout(layout_card)
window.show()
app.exec()

