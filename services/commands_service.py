from services.messages import Messages


class Commands(Messages):
    COMMANDS = """
    СПИСОК КОМАНД:\n
    @legion_pidor, старт пидор - начать поиск пидора;\n
    @legion_pidor, старт натурал - начать поиск натурала;\n
    @legion_pidor, команды - показать список команд;\n
    @legion_pidor, топ натурал - показать топ натуралов;\n
    @legion_pidor, топ пидор - показать топ пидоров;\n
    """

    def message(self, chat_id: int) -> None:
        self.api.send_message(
            text=self.COMMANDS,
            chat_id=chat_id
        )
