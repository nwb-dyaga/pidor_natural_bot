from db import Chat
from db.connect import connect_db
from db.utils import get_or_create


class ChatService:

    def check_new_chat(self, message: dict) -> None:
        if message.get('action') is not None:
            if message['action'].get('type') == 'chat_invite_user' and \
                    message['action'].get('member_id') == -214223885:
                self.new_chat(message['peer_id'])

    @staticmethod
    def new_chat(peer_id: str) -> None:
        session = connect_db()
        get_or_create(session, Chat, vk_id=str(peer_id))
        session.commit()
