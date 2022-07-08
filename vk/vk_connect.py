import os

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id


class VkConnect:

    def __init__(self) -> None:
        self.group_id = os.getenv('VK_GROUP_ID')
        self.vk_session = vk_api.VkApi(token=os.getenv('VK_TOKEN'))
        self.longpoll = VkBotLongPoll(self.vk_session)
        self.api = self.vk_session.get_api()

    def send_message(self, text: str, chat_id: int) -> None:
        self.api.messages.send(
            random_id=get_random_id(),
            message=text,
            chat_id=chat_id
        )

    def get_chat_users(self, id: str) -> list:
        return self.api.messages.getConversationMembers(peer_id=id)

    def get_chat_name(self, peer_id: str) -> dict:
        return self.api.messages.getChat(chat_id=peer_id)

    def get_users_screen(self, ids: str) -> list:
        return self.api.users.get(user_ids=ids, fields=['screen_name'])
