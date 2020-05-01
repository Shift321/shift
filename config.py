from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vkapi import vk_session, longpoll,VkEventType
import re
from sql import cursor, conn
from constants import text_for_admins, text_for_users, format_of_write, exist, no_aids_with_this_name, states, admins_id, aids_message


def send_message(user_id, message):              #функция , которая отвечает за отправление сообщения
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard': keyboard})


def create_keyboard():                           #функция создания клавиатуры
    keyboard = VkKeyboard(one_time=True)
    if states[event.user_id] == "menu":
        keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Поиск по ав', color=VkKeyboardColor.PRIMARY)
        if event.user_id in admins_id:
                keyboard.add_button('Запись', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('Изменить', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('удалить', color=VkKeyboardColor.PRIMARY)
    else:
        keyboard.add_button('Отмена', color=VkKeyboardColor.PRIMARY)
    keyboard = keyboard.get_keyboard()
    return keyboard


while True:
    for event in longpoll.listen():
        if event.from_user and not event.from_me:
            if event.type == VkEventType.MESSAGE_NEW:
                response = event.text.lower()
                if event.user_id not in states:
                    states[event.user_id] = "menu"
                
                if response == "отмена":
                    states[event.user_id] = "menu"
                    keyboard = create_keyboard()
                    if event.user_id in admins_id:
                        send_message(event.user_id, text_for_admins)
                    else:
                        send_message(event.user_id, text_for_users)
                elif states[event.user_id] == "menu":
                    if response == "меню":
                        states[event.user_id] = "menu"
                        keyboard = create_keyboard()
                        if event.user_id in admins_id:
                            send_message(event.user_id, text_for_admins)
                        else:
                            send_message(event.user_id, text_for_users)
                    elif response == "запись":
                        states[event.user_id] = "write"
                        keyboard = create_keyboard()
                        if event.user_id in admins_id:
                            send_message(event.user_id, format_of_write)
                        else:
                            send_message(event.user_id, exist)
                    elif response == "изменить":
                        states[event.user_id] = "edit"
                        keyboard = create_keyboard()
                        if event.user_id in admins_id:
                            send_message(event.user_id, "Введите название препарата, который хотите изменить.")
                        else:
                            send_message(event.user_id, exist)
                    elif response == "поиск по ав":
                        states[event.user_id] = "search_as"
                        keyboard = create_keyboard()
                        send_message(event.user_id, "Введите название действующего вещества,которое хотите посмотреть.")
                    elif response == "поиск":
                        states[event.user_id] = "search"
                        keyboard = create_keyboard()
                        send_message(event.user_id, "Введите название препарата ,которое хотите посмотреть.")
                    elif response == "удалить":
                        states[event.user_id] = "delete"
                        keyboard = create_keyboard()
                        if event.user_id in admins_id:
                            send_message(event.user_id, "Введите название препарата ,которое хотите удалить.")    
                        else:
                            send_message(event.user_id, exist)
                    else:
                        send_message(event.user_id, exist)
                elif states[event.user_id] == "write":                                        # Цикл для записи нового препарата
                    regular = re.findall(r"(.+?)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)",event.text) 
                    if len(list(regular)) == 0:                                                        # проверка правильности ввода.
                        send_message(event.user_id, "Не правильный формат.")
                        continue
                    sql_write = "SELECT * FROM aids WHERE aids_name =?"
                    cursor.execute(sql_write, [(regular[0][1])])
                    cursor_fetchall = cursor.fetchall()
                    if cursor_fetchall == []:
                        for i in range(len(list(regular))):
                            cursor.execute(f"""INSERT INTO aids VALUES ("{regular[i][0]}",
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
                            send_message(event.user_id, "Записано.")
                            states[event.user_id] = "menu"
                    else:
                        send_message(event.user_id, "Такое лекарство уже есть.")
                elif states[event.user_id] == "edit":                                                    # Цикл для изменения параметров припарата
                        cursor.execute(f"SELECT * FROM aids WHERE aids_name LIKE '%{event.text}%'")
                        cursor_fetchall_edit = cursor.fetchall()
                        if cursor_fetchall_edit == []:                                                                  # Проверка есть ли такой препарат в базе
                            send_message(event.user_id, "Нет такого препарата попробуйте еще раз.")
                            continue
                        aids_message[event.user_id] = cursor_fetchall_edit[0][1]
                        states[event.user_id] = "edition"
                        send_message(event.user_id, format_of_write)
                elif states[event.user_id] == "edition":                                                 # изменение
                    regular = re.findall(r"(.+?)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)",event.text)
                    for i in range(len(list(regular))):
                        cursor.execute(f"""UPDATE aids SET
                                        active_substance = "{regular[i][0]}",
                                        aids_name = "{regular[i][1]}",
                                        farm_group = "{regular[i][2]}",
                                        release_form = "{regular[i][3]}",
                                        target = "{regular[i][4]}",
                                        animal = "{regular[i][5]}",
                                        dosage = "{regular[i][6]}",
                                        ways_to_use = "{regular[i][7]}",
                                        how_often = "{regular[i][8]}",
                                        source = "{regular[i][9]}",
                                        WHERE aids_name ="{aids_message[event.user_id]}" """
                                       )
                        conn.commit()
                        send_message(event.user_id, "Изменено")
                        states[event.user_id] = "menu"
                elif states[event.user_id] == "search_as":                                 # Цикл для поиска по активному веществу
                    cursor.execute(f"SELECT * FROM aids WHERE active_substance LIKE '%{event.text}%'")
                    text = cursor.fetchall()
                    if text == []:                                                                 # проверка есть ли препарат с таким активным веществом в базе
                        send_message(event.user_id, no_aids_with_this_name)
                        states[event.user_id] = "search_as"
                        continue
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
                        
                        send_message(event.user_id, message_of_search_as)
                    states[event.user_id] = "menu"    
                elif states[event.user_id] == "search":                                  # Цикл для поиска по названию препарата
                    search_as_sql = f"SELECT * FROM aids WHERE aids_name LIKE '{event.text}%'COLLATE NOCASE"
                    cursor.execute(search_as_sql)
                    text = cursor.fetchall()
                    if text == []:
                        send_message(event.user_id, no_aids_with_this_name)                        # проверка есть ли такой препарат в базе
                        states[event.user_id] = "search"
                        continue
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
                        
                elif states[event.user_id] == "delete":                               # Цикл для удаления препарата по названию
                    sql_delete = "SELECT * FROM aids WHERE aids_name =?"
                    cursor.execute(sql_delete, [(event.text)])
                    cursor_fetchall_delte = cursor.fetchall()
                    if cursor_fetchall_delte == []:                                           # проверка есть ли такой препарат в базе
                        send_message(event.user_id, "Нет такого препарата попробуйте еще раз.")
                        states[event.user_id] = "menu"
                        continue
                    sql_delete = "DELETE FROM aids WHERE aids_name =?"
                    cursor.execute(sql_delete, ([event.text]))
                    conn.commit()
                    states[event.user_id] = "menu"
                    send_message(event.user_id, "Удалено")
