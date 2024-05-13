import telebot
import datetime
import time

TOKEN = ''
GROUP_CHAT_ID = ''
bot = telebot.TeleBot(TOKEN)


class PollManager:
    def __init__(self):
        self.people = []
        self.voted_people = []
        self.poll_id = None

    def create_poll(self, question, options):
        poll = bot.send_poll(GROUP_CHAT_ID, question, options)
        self.poll_id = poll.poll.id

    def get_all_users(self):
        members = bot.get_chat_members(GROUP_CHAT_ID)
        for member in members:
            self.people.append(member.username)

    def get_poll_answers(self):
        if self.poll_id is not None:
            poll_answers = bot.get_poll_answer(self.poll_id)
            for answer in poll_answers:
                self.voted_people.append(answer.user.username)

    def print_non_voters(self):
        non_voters = [person for person in self.people if person not in self.voted_people]
        for non_voter in non_voters:
            bot.send_message(chat_id=GROUP_CHAT_ID, text=f'{non_voter}')
        bot.send_message(chat_id=GROUP_CHAT_ID, text='Люди, которые не проголосовали, были отправлены в чате')


class ReactionManager:
    def __init__(self):
        self.people = []
        self.reacted_people = []
        self.message = None

    def get_all_users(self):
        members = bot.get_chat_members(GROUP_CHAT_ID)
        for member in members:
            self.people.append(member.user.id)

    def create_message(self, message):
        message = bot.send_message(GROUP_CHAT_ID, message)
        self.message = message

    def get_reactions(self):
        for reaction in message.reactions:
            self.reacted_people.append(reaction.user.id)

    def print_non_reactors(self):
        non_reactors = [person for person in self.people if person not in self.reacted_people]
        for non_reactor in non_reactors:
            bot.send_message(chat_id=GROUP_CHAT_ID, text=f'{non_reactor}')
        bot.send_message(chat_id=GROUP_CHAT_ID, text='Люди, которые не поставили реакцию, были отправлены в чате')


reaction_manager = ReactionManager()
poll_manager = PollManager()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Здравствуйте, я бот, который поможет вам узнать, кто не проголосовал в опросе')


@bot.message_handler(commands=['create_poll'])
def create_poll(message):
    question = message.text.split()[1]
    options = message.text.split()[2:]
    poll_manager.create_poll(question, options)


@bot.message_handler(commands=['create_message'])
def create_message(message):
    message_text = message.text.split()[1]
    reaction_manager.create_message(message_text)


def main():
    while True:
        now = datetime.datetime.now()
        if now.hour == 14 and now.minute == 15:
            poll_manager.get_poll_answers()
            poll_manager.print_non_voters()

            reaction_manager.get_reactions()
            reaction_manager.print_non_reactors()

            time.sleep(86400 - now.second)


if __name__ == '__main__':
    main()


bot.polling(none_stop=True, interval=0)