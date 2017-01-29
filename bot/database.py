from pymongo import MongoClient
import datetime, logging

client = MongoClient('localhost', 27017)
db = client.timelog
col = db.timelog

tz = datetime.timedelta(hours=6)

def addEvent(eventType, duration):
	doc = col.find_one({'finished': False})
	if doc:
		return 'Надо закончить предыдущее действие коммандой /finish'

	duration = int(duration)
	finishTime = datetime.datetime.utcnow()
	startTime = finishTime - datetime.timedelta(minutes=duration)

	event = {
		'type': eventType,
		'start': startTime,
		'finish': finishTime,
		'duration': duration
	}
	col.insert(event)
	logging.info('Added new event. [{}], {} minutes'.format(eventType, duration))
	return 'Добавленно действие *{}* которое длилось *{}* минут с *{}* по *{}*'.format(
			eventType,
			duration,
			(startTime + tz).strftime('%H:%M:%S'),
			(finishTime + tz).strftime('%H:%M:%S')
		)

def startEvent(eventType):
	doc = col.find_one({'finished': False})
	if doc:
		return 'Надо закончить предыдущее действие коммандой /finish'
	startTime = datetime.datetime.utcnow()
	event = {
		'type': eventType,
		'start': startTime,
		'duration': 0,
		'finish': 0,
		'finished': False
	}
	col.insert(event)
	logging.info('Started new event. [{}]'.format(eventType))
	return 'Начато новое действие *{}*'.format(eventType)

def finishEvent():
	finishTime = datetime.datetime.utcnow()
	doc = col.find_one({'finished': False})
	if not doc:
		return 'Надо начать действие коммандой /start'
	eventType = doc['type']
	startTime = doc['start']
	duration = int((finishTime-startTime).seconds/60)
	event = {
		'$set': {
			'finish': finishTime,
			'duration': duration
		},
		'$unset': {
			'finished': 1
		}
	}
	col.update_one({'finished': False}, event)
	logging.info('Finished event. [{}], {} minutes'.format(eventType, duration))
	return 'Законченно действие *{}*, которое длилось *{}* минут с *{}*'.format(
			eventType,
			duration,
			(startTime+tz).strftime('%H:%M:%S')
		)

def info():
	doc = col.find_one({'finished': False})
	if not doc:
		return 'Текущих действий нет'

	eventType = doc['type']
	startTime = doc['start']
	duration = int((datetime.datetime.utcnow()-startTime).seconds/60)
	return 'Текущее действие *{}*, которое длится *{}* минут с *{}*'.format(
			eventType,
			duration,
			(startTime+tz).strftime('%H:%M:%S')
		)

__all__ = ['addEvent', 'startEvent', 'finishEvent', 'info']