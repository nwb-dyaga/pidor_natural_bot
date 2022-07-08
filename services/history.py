from functools import reduce

from sqlalchemy import func

from db import History, HistoryNatural, Chat
from db.connect import connect_db
from services.messages import Messages


class HistoryService(Messages):

    @staticmethod
    def get_history(chat_id: int, model: HistoryNatural or History) -> list:
        session = connect_db()
        chat = session.query(Chat).filter_by(vk_id=str(chat_id)).first()
        history = session.query(model.vk_id,
                                model.name,
                                model.chat,
                                func.count(model.name)) \
            .group_by(model.name, model.chat, model.vk_id).filter_by(
            chat=int(chat.id)).order_by(
            func.count(model.name).desc()).all()
        return history

    def history_message(self, chat_id: int, peer_id: int, model: HistoryNatural or History, top: str) -> None:
        history = self.get_history(peer_id, model)
        if len(history) > 1:
            hist_ids = reduce(lambda x, y: f'{x[0]},{y[0]}', history)
        elif len(history) == 1:
            hist_ids = history[0][0]
        else:
            hist_ids = None
        if hist_ids is not None:
            screen_names = self.api.get_users_screen(hist_ids)
            history_str = f'Топ {top}: \n'
            for i, h in enumerate(history):
                history_str += f'{i + 1}. @{list(filter(lambda x: int(x["id"]) == int(h[0]), screen_names))[0]["screen_name"]}({h[1]}) - {h[3]} раз(а)\n'
            self.api.send_message(
                text=history_str,
                chat_id=chat_id
            )
        else:
            self.api.send_message(
                text=f'{top} пока нет!',
                chat_id=chat_id
            )
