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

room_pet_den = None
room_unfroze = None
room_priv_fh = None
room_the_den = None
room_sandbox = None

def main():
	global wall, room_pet_den, room_unfroze, room_priv_fh, room_the_den, room_sandbox
	setup_logging()

	host_id = 'stackexchange.com'
	pet_den = '146039'
	unfroze = '146791'
	priv_fh = '148132'
	the_den = '148152'
	sandbox = '1'
	

	client = chatexchange.client.Client(host_id)
	client.login(email, password)

	room_pet_den = client.get_room(pet_den)
	room_unfroze = client.get_room(unfroze)
	room_priv_fh = client.get_room(priv_fh)
	room_the_den = client.get_room(the_den)
	room_sandbox = client.get_room(sandbox)
	
	rooms = [
		room_pet_den,
		room_unfroze,
		room_priv_fh,
		room_the_den,
		room_sandbox,
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
			if int(message.user.id) in [573201, 578513]:
				result = subprocess.check_output(array).decode()
				return_result = f"""    @{message.user.name.replace(' ', '')}\n    \n"""
				temp_result = []
				for line in result.split("\n"):
					temp_result.append("    " + line)
				return_result += "\n".join(temp_result)
				#print(return_result)
				#with open("result.txt", "w") as f:
				#	f.write(return_result)
				message.room.send_message(return_result)
			else:
				message.message.reply("You don't have the powers to run this. If you feel you should be able to, go ahead and ping @Petəíŕd.")
		except:
			message.message.reply("Something went wrong. Ping Petəíŕd if you think they should look at this.")

	if "🐟" in message.content and "The Linux Wizard" in message.content and "quivers" in message.content and int(message.user.id) == 375672:
		message.room.send_message("/fish")
		message.room.send_message("Argh, I can auto-fish too!")
		message.room.send_message("/fish")

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
