import vk_api
from vk_api.longpoll import VkLongPoll

token = "1c84a6073e222a3c465f52a424418bb7b15d1b54254dee96fa0e3330dc9c9aa696c6ce990e2cd2f568085"   # noqa
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
session_api = vk_session.get_api()


def get_full_name(event):
    id = event.user_id
    user_get=session_api.users.get(user_ids = (id))
    user_get=user_get[0]
    first_name=user_get['first_name']
    last_name=user_get['last_name']
    full_name=first_name+" "+last_name
    print (full_name)