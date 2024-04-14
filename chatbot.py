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

#with open("result.txt", "w") as f:
#	f.write("Result is curently empty.")

letters = "qwertyzxcv"
numbers = "0123456789"

def numenc(ns):
        return ''.join([letters[int(n)] if n in numbers else n for n in ns])

def numdec(ls):
        return ''.join([str(letters.index(l.lower())) if l.lower() in letters else l for l in ls])

room_pet_den = None

def main():
	global wall, room_pet_den, room_unfroze, room_priv_fh, room_the_den, room_sandbox
	setup_logging()

	host_id = 'stackexchange.com'
	pet_den = '152450' #'146039'
	priv_fh = '148132'

	client = chatexchange.client.Client(host_id)
	client.login(email, password)

	room_pet_den = client.get_room(pet_den)
	
	rooms = [
		room_pet_den,
	]

	for room in rooms:
		room.join()
		room.watch(on_message)
		#room.send_message("Bot has started using Actions.")
		#print("(You are now in room #%s on %s.)" % (room_id, host_id))


	#while True:
	#	message = input("<< ")
	#	room.send_message(message)

	count = 1
	while True:
		print("running, " + str(count))
		count += 1
		time.sleep(60)

	client.logout()


def on_message(message, client):
	if not isinstance(message, chatexchange.events.MessagePosted):
		# Ignore non-message_posted events.
		logger.debug("event: %r", message)
		return

	if message.content.startswith("alive"):
		message.message.reply("Yes, I'm still alive.")

	if message.content.startswith("shell "):
		try:
			array = message.content.split(" ")[1:]
			if int(message.user.id) in [595292, 580308]:
				result = subprocess.check_output(array).decode()
				return_result = f"""    @{message.user.name.replace(' ', '')}\n    \n"""
				temp_result = []
				#print(temp_result)
				for line in result.split("\n"):
					temp_result.append("    " + line)
				return_result += "\n".join(temp_result)
				#print(return_result)
				#with open("result.txt", "w") as f:
				#	f.write(return_result)
				message.room.send_message(return_result)
			else:
				message.message.reply("You don't have the powers to execute shell commands ;). If you feel like you should be able to, go ahead and ping @Petəíŕd.")
		except Exception as e:
			message.message.reply("Something went wrong. Ping Petəíŕd if you think they should look at this.\n\n" + str(e))
		
	if message.content.startswith("num"):
		try:
			cmd = message.content.split(" ")[0][3:]
			msg = message.content
			res = "No input provided."
			answered_already = False
			content = msg[len(msg.split(" ")[0]) + 1:]
			if content == "":
				answered_already = True
				message.message.reply(res)
			if cmd == "enc": res = numenc(content)
			elif cmd == "dec": res = numdec(content)
			if not answered_already: message.message.reply(res)
		except Exception as e:
			message.message.reply("Something went wrong while running the crypto computer:\n\n" + str(e))

	if "🐟" in message.content and "The Spring Wizard" in message.content and "quivers" in message.content and int(message.user.id) == 375672:
		message.room.send_message("/fish again")

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
