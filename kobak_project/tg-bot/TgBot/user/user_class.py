class User:

    """
    Вспомогательный класс для юзера, описывающий id чата и юзера
    """

    def __init__(self, chat_id, user_id):
        self.__chat_id = chat_id
        self.__user_id = user_id

    def get_chat(self):
        return self.__chat_id

    def get_user(self):
        return self.__user_id