import logging, telepot, datetime
from config import config
from .commands import check

chats = config['chats']

def on_chat_message(msg):
	flavor = telepot.flavor(msg)
	content_type, chat_type, chat_id = telepot.glance(msg, flavor=flavor)

	if not content_type == 'text':
		return

	if str(chat_id) in chats:
		logging.info(msg)
		# bot.sendMessage(chat_id, 'Hi!')

	res = check(msg, bot)
	if res:
		bot.sendMessage(chat_id, res, parse_mode='markdown')


def start_update_loop():
	bot.message_loop({'chat': on_chat_message})
	logging.info('Listening...')

bot = telepot.Bot(config['apiKey'])