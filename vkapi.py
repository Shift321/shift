import vk_api
from vk_api.longpoll import VkLongPoll

token = "b8c6a001df422754d68584216162f2a7e2949db599397c6c88d3bbd27c48d95edaf0f75adf556f72c313a"   # noqa
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