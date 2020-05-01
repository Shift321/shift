from vkapi import longpoll
from functions import *
from vk_api.longpoll import VkEventType

while True:                                                                                                    # Основной цикл
    for event in longpoll.listen():
        if event.from_user and not event.from_me:
            if event.type == VkEventType.MESSAGE_NEW:
                response = event.text.lower()
                if event.user_id not in states:
                    states[event.user_id] = "menu"
                if response == "отмена":
                    states[event.user_id] = "menu"
                    send_message(event.user_id, "handle_admin")
                elif states[event.user_id] == "menu":
                    handle_menu(response, event)
                elif states[event.user_id] == "write":
                    handle_write(event)
                elif states[event.user_id] == "edit":
                    handle_edit(event)
                elif states[event.user_id] == "edition":                                                # изменение
                    handle_edittion(event)
                elif states[event.user_id] == "search_as":                                              # функция для поиска по активному веществу
                    handle_search_as(event)
                elif states[event.user_id] == "search":                                                 # функция для поиска по названию препарата
                    handle_search(event)
                elif states[event.user_id] == "delete":                                                 # функция для удаления препарата по названию
                    handle_delete(event)
