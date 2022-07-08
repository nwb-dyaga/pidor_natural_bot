import datetime
import time

from db import Chat
from db.connect import connect_db
from services.messages import Messages


class LastStart(Messages):
    COOLDOWN = 24

    def check_last(self, chat_id: int, attr: str, peer_id: str) -> bool or time:
        session = connect_db()
        chat = session.query(Chat).filter_by(vk_id=str(peer_id)).first()
        last_time = getattr(chat, attr)
        if last_time is None:
            return True
        if last_time.timestamp() + datetime.timedelta(
                hours=self.COOLDOWN).total_seconds() < datetime.datetime.now().timestamp():
            return True
        self.api.send_message(
            text=f'Следующий запуск доступен через {self.get_next_time(last_time)}',
            chat_id=chat_id
        )
        return False

    def get_next_time(self, last: datetime) -> str:
        return time.strftime('%H:%M', time.gmtime(
            int(datetime.timedelta(hours=self.COOLDOWN).total_seconds() - (datetime.datetime.now().timestamp() -
                                                                           last.timestamp()))))
