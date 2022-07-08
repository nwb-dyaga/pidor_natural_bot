import requests
from vk_api.bot_longpoll import VkBotEventType

from db import History, HistoryNatural
from services.chat_service import ChatService
from services.check_last import LastStart
from services.commands_service import Commands
from services.finder_service import Finder
from services.history import HistoryService
from services.other_messages import OtherMessages
from vk.vk_connect import VkConnect

vk = VkConnect()

while True:
    try:
        for event in vk.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    ChatService().check_new_chat(event.object.message)
                    peer_id = event.object.message['peer_id']
                    message_text = event.object.message['text']
                    if '[club214223885|@legion_pidor]' in message_text or '[club214223885|*legion_pidor]' in message_text:
                        if 'старт пидор' in message_text:
                            if LastStart(vk).check_last(event.chat_id, 'last_pidor', peer_id):
                                OtherMessages(vk).send_other(event.chat_id)
                                Finder(vk).search(event, 'пидор', 'last_pidor', History)
                        elif 'старт натурал' in message_text:
                            if LastStart(vk).check_last(event.chat_id, 'last_natural', peer_id):
                                OtherMessages(vk).send_other(event.chat_id)
                                Finder(vk).search(event, 'натурал', 'last_natural', HistoryNatural)
                        elif 'команды' in message_text:
                            Commands(vk).message(event.chat_id)
                        elif 'топ пидор' in message_text:
                            HistoryService(vk).history_message(event.chat_id, peer_id, History, 'Пидоров')
                        elif 'топ натурал' in message_text:
                            HistoryService(vk).history_message(event.chat_id, peer_id, HistoryNatural, 'Натуралов')
                        else:
                            Commands(vk).message(event.chat_id)
    except requests.exceptions.ReadTimeout:
        pass
