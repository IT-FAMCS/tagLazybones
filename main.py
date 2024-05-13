import pyrogram
import datetime
import time

app = pyrogram.Client("my_account")

GROUP_CHAT_ID = "chat_id_here"


@app.on_message(pyrogram.filters.command("start"))
def start_command(client, message):
    message.reply_text("Привет! Я бот, который будет проверять, что все участники группы проголосовали в опросе")


class PollManager:
    def __init__(self):
        self.poll_message = None
        self.poll_voters = []
        self.members = []

    def create_poll(self, question, options):
        self.poll_message = app.send_poll(
            chat_id=GROUP_CHAT_ID,
            question=question,
            options=options
        )

    def get_poll_voters(self):
        if self.poll_message is not None:
            poll_message_id = self.poll_message.message_id
            self.poll_voters = app.get_poll_voters(chat_id=GROUP_CHAT_ID, message_id=poll_message_id)

    def get_members(self):
        self.members = app.get_chat_members(GROUP_CHAT_ID)

    def check_voters(self):
        self.get_poll_voters()
        self.get_members()

        member_ids = [member.user.id for member in self.members]
        voter_ids = [voter.user.id for voter in self.poll_voters]

        for member_id in member_ids:
            if member_id not in voter_ids:
                app.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=f"Пользователь {member_id} не проголосовал в опросе",
                )


class ReactionsManager:
    def __init__(self):
        self.message = None
        self.reactions = []
        self.members = []

    def create_message(self, text):
        self.message = app.send_message(
            chat_id=GROUP_CHAT_ID,
            text=text
        )

    def get_reactions(self):
        if self.message is not None:
            message_id = self.message.message_id
            self.reactions = app.get_reactions(GROUP_CHAT_ID, message_id)

    def get_members(self):
        self.members = app.get_chat_members(GROUP_CHAT_ID)

    def check_reactions(self):
        self.get_reactions()
        self.get_members()

        member_ids = [member.user.id for member in self.members]
        reaction_ids = [reaction.user.id for reaction in self.reactions]

        for member_id in member_ids:
            if member_id not in reaction_ids:
                app.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=f"Пользователь {member_id} не поставил реакцию",
                )


poll_manager = PollManager()
reactions_manager = ReactionsManager()


@app.on_message(pyrogram.filters.command("create_poll"))
def create_poll_command(client, message):
    poll_manager.create_poll("Вопрос", ["Ответ 1", "Ответ 2", "Ответ 3"])
    message.reply_text("Опрос создан")


@app.on_message(pyrogram.filters.command("create_message"))
def create_message_command(client, message):
    reactions_manager.create_message("Текст сообщения")
    message.reply_text("Сообщение создано")


def main():
    while True:
        now = datetime.datetime.now()
        if now.hour == 14 and now.minute == 15:
            poll_manager.check_voters()
            reactions_manager.check_reactions()
            time.sleep(86400 - now.second)


if __name__ == '__main__':
    main()
    app.run()