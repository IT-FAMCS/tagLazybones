import telebot

TOKEN = ''
GROUP_CHAT_ID = ''
bot = telebot.TeleBot(TOKEN)


class PollManager:
    def __init__(self):
        self.people = []
        self.voted_people = []

    def get_all_users(self):
        members = bot.get_chat_members(GROUP_CHAT_ID)
        for member in members:
            self.people.append(member.username)

    def get_poll_answers(self, poll_id):
        poll_answers = bot.get_poll_answer(poll_id)
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

    def get_all_users(self):
        members = bot.get_chat_members(GROUP_CHAT_ID)
        for member in members:
            self.people.append(member.user.id)

    def get_reactions(self, message_id):
        message = bot.get_message(GROUP_CHAT_ID, message_id)
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


@bot.message_handler(commands=['get_poll_answers'])
def get_poll_answers(message):
    poll_id = message.text.split()[1]
    poll_manager.get_poll_answers(poll_id)
    poll_manager.print_non_voters()


@bot.message_handler(commands=['get_reactions'])
def get_reactions(message):
    message_id = message.text.split()[1]
    reaction_manager.get_reactions(message_id)
    reaction_manager.print_non_reactors()