#!/usr/bin/env python

# Uncomment next line if you are forking.
#import pip
#pip.main(["install", "chatexchange"])

import getpass
import logging
import logging.handlers
import sys

import chatexchange.client
import chatexchange.events
import os

logger = logging.getLogger(__name__)

email = sys.argv[1]
password = sys.argv[2]

room = None

def main():
	global wall, room
	setup_logging()

	host_id = 'stackexchange.com'
	room_id = '1'

	client = chatexchange.client.Client(host_id)
	client.login(email, password)

	room = client.get_room(room_id)
	room.join()
	room.watch(on_message)

	print("(You are now in room #%s on %s.)" % (room_id, host_id))

	room.send_message("testing python?")
	room.send_message("alive")

	while True:
		message = input("<< ")
		room.send_message(message)

	client.logout()


def on_message(message, client):
	if not isinstance(message, chatexchange.events.MessagePosted):
		# Ignore non-message_posted events.
		logger.debug("event: %r", message)
		return

	if message.content.startswith("alive"):
		message.message.reply("Yes, I'm still alive.")

def setup_logging():
	logging.basicConfig(level=logging.CRITICAL)
	logger.setLevel(logging.CRITICAL)

	# In addition to the basic stderr logging configured globally
	# above, we'll use a log file for chatexchange.client.
	wrapper_logger = logging.getLogger('chatexchange.client')
	wrapper_handler = logging.handlers.TimedRotatingFileHandler(
		filename='client.log',
		when='midnight', delay=True, utc=True, backupCount=7,
	)
	wrapper_handler.setFormatter(logging.Formatter(
		"%(asctime)s: %(levelname)s: %(threadName)s: %(message)s"
	))
	wrapper_logger.addHandler(wrapper_handler)


if __name__ == '__main__':
	main()
