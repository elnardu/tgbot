import logging, os, time
dir_name = os.path.dirname(os.path.abspath(__file__))

from config import config
if config['logToFile']:
	logging.basicConfig(filename=dir_name+'/bot.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
else:
	logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')


from bot.bot import start_update_loop

start_update_loop()

while 1:
	time.sleep(10)
