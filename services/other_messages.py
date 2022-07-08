import random
import time

from services.messages import Messages


class OtherMessages(Messages):
    TIME_SLEEP = 1
    RANDOM_MESSAGES = ('Как же вы меня достали!', 'Лучше бы полезным чем-то занялись...', 'Опять за старое...',
                    'Ой, да все вы тут того самого')

    def random_message(self, chat_id: int) -> None:
        self.api.send_message(
            text=self.RANDOM_MESSAGES[random.randint(0, len(self.RANDOM_MESSAGES) - 1)],
            chat_id=chat_id
        )

    def search_message(self, chat_id: int) -> None:
        self.api.send_message(
            text="Ну ладно, сейчас найдем!",
            chat_id=chat_id
        )

    def send_other(self, chat_id: int) -> None:
        self.random_message(chat_id)
        time.sleep(self.TIME_SLEEP)
        self.search_message(chat_id)
        time.sleep(self.TIME_SLEEP)
