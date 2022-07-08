import datetime
import random
import time

from vk_api import ApiError

from db import Chat, History, HistoryNatural
from db.connect import connect_db
from services.messages import Messages


class Finder(Messages):
    COOLDOWN = 24

    def find_user(self, peer_id: str) -> dict:
        users = self.api.get_chat_users(peer_id)['profiles']
        pidor_user = users[random.randint(0, len(users) - 1)]
        return pidor_user

    def generate_str(self, user: dict, from_id: str, value: str) -> str:
        name = self.full_name(user)
        if user['id'] == from_id:
            return f'@{user["screen_name"]}({name}), вот ты и есть {value}'
        else:
            return f'Заявляю, что {value} дня - @{user["screen_name"]}({name})'

    def search(self, event, value: str, attr: str, model: History or HistoryNatural) -> None:
        peer_id = event.object.message['peer_id']
        try:
            user = self.find_user(peer_id)
            self.api.send_message(
                text=self.generate_str(user, event.object.message['from_id'], value),
                chat_id=event.chat_id
            )
            self.insert_to_db(attr, model, user_id=user['id'], chat_id=peer_id, name=self.full_name(user))
        except ApiError:
            self.api.send_message(
                text='Добавьте бота в администраторы беседы!',
                chat_id=event.chat_id
            )

    @staticmethod
    def insert_to_db(attr: str, model: History or HistoryNatural, **kwargs) -> None:
        session = connect_db()
        chat = session.query(Chat).filter_by(vk_id=str(kwargs['chat_id'])).first()
        session.add(model(vk_id=str(kwargs['user_id']), chat=chat.id, name=kwargs['name']))
        setattr(chat, attr, datetime.datetime.now())
        session.commit()

    @staticmethod
    def full_name(user: dict) -> str:
        return f'{user.get("first_name")} {user.get("last_name")}'