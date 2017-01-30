import logging
from .database import *

def check(msg, bot):
	text = msg['text']
	if not text[0] == '/':
		return

	args = text.split()
	command = args[0][1:]

	if command == "add":
		res = addEvent(args[1], args[2])

	elif command == "start":
		res = startEvent(args[1])

	elif command == "finish":
		res = finishEvent()

	elif command == "info":
		res = info()

	elif command == "last":
		if len(args) < 2:
			args += [5]
		res = getLast(args[1])

	elif command == "ping":
		res = "Pong"

	return res