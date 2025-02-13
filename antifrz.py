#!/usr/bin/env python

# Uncomment next lines if you are forking.
#import pip
#pip.main(["install", "chatexchange"])

import getpass
import logging
import logging.handlers
import sys
import time

import chatexchange.client
import chatexchange.events
import os
import subprocess

logger = logging.getLogger(__name__)

email = sys.argv[1]
password = sys.argv[2]

def numenc(ns):
        return ''.join([letters[int(n)] if n in numbers else n for n in ns])

def numdec(ls):
        return ''.join([str(letters.index(l.lower())) if l.lower() in letters else l for l in ls])

room_pet_den = None

def main():
	global wall, room_priv_fh, room_priv_f1
	setup_logging()

	host_id = 'stackexchange.com'
	priv_fh = '157651'
	priv_f1 = '157666'

	client = chatexchange.client.Client(host_id)
	client.login(email, password)

	room_priv_fh = client.get_room(priv_fh)
	room_priv_f1 = client.get_room(priv_f1)

	rooms = [
		room_priv_fh,
		room_priv_f1,
	]

	for room in rooms:
		room.join()
		room.send_message("/fish again")

	client.logout()

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
	#room.send_message("Bot stopped.")
