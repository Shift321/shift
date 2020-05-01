from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vkapi import vk_session, longpoll,VkEventType
import re
from sql import cursor, conn
from constants import text_for_admins, text_for_users, format_of_write, exist, no_medicines_with_this_name, states, admins_id, medicines_message

def send_message(user_id,message):                                                                            #функция , которая отвечает за отправление сообщения
    keyboard = create_keyboard(user_id)
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard': keyboard})


def create_keyboard(user_id):                                                                                         # функция создания клавиатуры
    keyboard = VkKeyboard(one_time=False)
    if states[user_id] == "menu":
        keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Поиск по ав', color=VkKeyboardColor.PRIMARY)
        if user_id in admins_id:
                keyboard.add_button('Запись', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('Изменить', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('удалить', color=VkKeyboardColor.PRIMARY)
    else:
        keyboard.add_button('Отмена', color=VkKeyboardColor.PRIMARY)
    keyboard = keyboard.get_keyboard()
    return keyboard

def handle_write():                                                                                            # функция для записи нового препарата
    regular = re.findall(r"(.+?)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)",event.text) 
    if len(list(regular)) == 0:                                                                                # проверка правильности ввода.
        send_message(event.user_id, "Не правильный формат.")
        return
    sql_write = "SELECT * FROM medicines WHERE medicines_name =?"
    cursor.execute(sql_write, [(regular[0][1])])
    cursor_fetchall = cursor.fetchall()
    if cursor_fetchall == []:
        for i in range(len(list(regular))):
            cursor.execute(f"""INSERT INTO medicines VALUES ("{regular[i][0]}",
                                                        "{regular[i][1]}",
                                                        "{regular[i][2]}",
                                                        "{regular[i][3]}",
                                                        "{regular[i][4]}",
                                                        "{regular[i][5]}",
                                                        "{regular[i][6]}",
                                                        "{regular[i][7]}",
                                                        "{regular[i][8]}",
                                                        "{regular[i][9]}")""")
            conn.commit()
            states[event.user_id] = "menu"
            send_message(event.user_id, "Записано.")
            
            
    else:
        
        send_message(event.user_id, "Такое лекарство уже есть.")   

def handle_edit():                                                                                             # функция для изменения параметров припарата
    cursor.execute(f"SELECT * FROM medicines WHERE medicines_name LIKE '%{event.text}%'")
    cursor_fetchall_edit = cursor.fetchall()
    if cursor_fetchall_edit == []:                                                   # Проверка есть ли такой препарат в базе
        send_message(event.user_id, "Нет такого препарата попробуйте еще раз.")
        return
    medicines_message[event.user_id] = cursor_fetchall_edit[0][1]
    states[event.user_id] = "edition"
    send_message(event.user_id, format_of_write)

def handle_edittion():                                                                                         # изменение
    regular = re.findall(r"(.+?)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)",event.text)
    for i in range(len(list(regular))):
        cursor.execute(f"""UPDATE medicines SET
                        active_substance = "{regular[i][0]}",
                        medicines_name = "{regular[i][1]}",
                        farm_group = "{regular[i][2]}",
                        release_form = "{regular[i][3]}",
                        target = "{regular[i][4]}",
                        animal = "{regular[i][5]}",
                        dosage = "{regular[i][6]}",
                        ways_to_use = "{regular[i][7]}",
                        how_often = "{regular[i][8]}",
                        source = "{regular[i][9]}",
                        WHERE medicines_name ="{medicines_message[event.user_id]}" """
                        )
    conn.commit()
    states[event.user_id] = "menu"
    send_message(event.user_id, "Изменено")
    
def handle_search_as():                                                                                        # функция для поиска по активному веществу
    cursor.execute(f"SELECT * FROM medicines WHERE active_substance LIKE '%{event.text}%'")
    text = cursor.fetchall()
    if event.text == '':
        send_message(event.user_id, exist)
        return
    else:
        if text == []:                                                                       # проверка есть ли препарат с таким активным веществом в базе
            send_message(event.user_id, no_medicines_with_this_name)
            states[event.user_id] = "search_as"
            return
        for x in range(len(list(text))):
            message_of_search_as = f"""Действущее вещество: {text[x][0]}
                                        Название препарата: {text[x][1]}
                                        Форма выпуска: {text[x][2]}
                                        Фарм группа: {text[x][3]}
                                        Цель использования: {text[x][4]}
                                        Вид животного: {text[x][5]}
                                        Доза: {text[x][6]}
                                        Путь введения: {text[x][7]}
                                        Кратность: {text[x][8]}
                                        Источник: {text[x][9]}"""
    states[event.user_id] = "menu"
    send_message(event.user_id, message_of_search_as)
    
    

def handle_search():                                                                                           # функция для поиска по названию
    search_as_sql = f"SELECT * FROM medicines WHERE medicines_name LIKE '{event.text}%'COLLATE NOCASE"
    cursor.execute(search_as_sql)
    text = cursor.fetchall()
    if event.text == '':
        send_message(event.user_id, exist)
        return
    else:
        if text == []:
            send_message(event.user_id, no_medicines_with_this_name)                        # проверка есть ли такой препарат в базе
            states[event.user_id] = "search"
            return
        for x in range(len(list(text))):
            message_of_search_as = f"""Действущее вещество: {text[x][0]}
                                        Название препарата: {text[x][1]}
                                        Форма выпуска: {text[x][2]}
                                        Фарм группа: {text[x][3]}
                                        Цель использования: {text[x][4]}
                                        Вид животного: {text[x][5]}
                                        Доза: {text[x][6]}
                                        Путь введения: {text[x][7]}
                                        Кратность: {text[x][8]}
                                        Источник: {text[x][9]}"""
    states[event.user_id] = "menu"
    send_message(event.user_id, message_of_search_as)

def handle_delete():                                                                                           #функция для удаления 
    sql_delete = "SELECT * FROM medicines WHERE medicines_name =?"
    cursor.execute(sql_delete, [(event.text)])
    cursor_fetchall_delte = cursor.fetchall()
    if cursor_fetchall_delte == []:                                                        # проверка есть ли такой препарат в базе
        send_message(event.user_id, "Нет такого препарата попробуйте еще раз.")
        states[event.user_id] = "menu"
        return
    sql_delete = "DELETE FROM medicines WHERE medicines_name =?"
    cursor.execute(sql_delete, ([event.text]))
    conn.commit()
    states[event.user_id] = "menu"
    send_message(event.user_id, "Удалено")


while True:
    for event in longpoll.listen():
        if event.from_user and not event.from_me:
            if event.type == VkEventType.MESSAGE_NEW:
                response = event.text.lower()
                if event.user_id not in states:
                    states[event.user_id] = "menu"
                if response == "отмена":
                    states[event.user_id] = "menu"
                    keyboard = create_keyboard(event.user_id)
                    if event.user_id in admins_id:
                        send_message(event.user_id, text_for_admins)
                    else:
                        send_message(event.user_id, text_for_users)
                elif states[event.user_id] == "menu":
                    if response == "меню":
                        states[event.user_id] = "menu"
                        keyboard = create_keyboard(event.user_id)
                        if event.user_id in admins_id:
                            send_message(event.user_id, text_for_admins)
                        else:
                            send_message(event.user_id, text_for_users)
                    elif response == "запись":
                        states[event.user_id] = "write"
                        keyboard = create_keyboard(event.user_id)
                        if event.user_id in admins_id:
                            send_message(event.user_id, format_of_write)
                        else:
                            send_message(event.user_id, exist)
                    elif response == "изменить":
                        states[event.user_id] = "edit"
                        keyboard = create_keyboard(event.user_id)
                        if event.user_id in admins_id:
                            send_message(event.user_id, "Введите название препарата, который хотите изменить.")
                        else:
                            send_message(event.user_id, exist)
                    elif response == "поиск по ав":
                        states[event.user_id] = "search_as"
                        keyboard = create_keyboard(event.user_id)
                        send_message(event.user_id, "Введите название действующего вещества,которое хотите посмотреть.")
                    elif response == "поиск":
                        states[event.user_id] = "search"
                        keyboard = create_keyboard(event.user_id)
                        send_message(event.user_id, "Введите название препарата ,которое хотите посмотреть.")
                    elif response == "удалить":
                        states[event.user_id] = "delete"
                        keyboard = create_keyboard(event.user_id)
                        if event.user_id in admins_id:
                            send_message(event.user_id, "Введите название препарата ,которое хотите удалить.")    
                        else:
                            send_message(event.user_id, exist)
                    else:
                        send_message(event.user_id, exist)
                elif states[event.user_id] == "write":                                                  
                    handle_write()                                                                       
                elif states[event.user_id] == "edit":                                                   
                    handle_edit()
                elif states[event.user_id] == "edition":                                                # изменение
                    handle_edittion()
                elif states[event.user_id] == "search_as":                                              # функция для поиска по активному веществу
                    handle_search_as()    
                elif states[event.user_id] == "search":                                                 # функция для поиска по названию препарата
                    handle_search()   
                elif states[event.user_id] == "delete":                                                 # функция для удаления препарата по названию
                    handle_delete()
