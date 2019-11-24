import os
import sys
import csv
import traceback
import time
import random
import re
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, UserBannedInChannelError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import errors
from telethon.errors import SessionPasswordNeededError
from colorama import Fore, init as color_ama
from datetime import datetime
import configparser
import io

color_ama(autoreset=True)
os.system('cls' if os.name=='nt' else 'clear')

config = configparser.RawConfigParser(allow_no_value=True)
# Just a small function to write the file
def write_file():
    config.write(open('config.ini', 'w'))
	
if not os.path.exists('config.ini'):
    config['SETTING'] = {'invite_interval': '120', 'pax_size': '50', 'pax_rest': '1080', 'flood_rest': '1800', 'target_group': 'jombuymuslimfirst', 'api_id': '1009439', 'api_hash': 'f2e00541628bff3be9e9e99c58fc1feb', '#____________________________TeleInviter________________________________': '', '#Invite a new member every 120 seconds.': '', '#When invited 50 new member, rest for 1080 seconds.': '', '#When got flooding warning from Telegram, rest for 1800 seconds.': '', '#When got flooding warning from Telegram, rest for 1800 seconds.': '', '#Invite group username without @': '',}

    write_file()
else:
	# Load the configuration file
	with open("config.ini") as f:
		sample_config = f.read()
	config = configparser.RawConfigParser(allow_no_value=True)
	config.read_file(io.StringIO(sample_config))
# If it doesn't i.e. An exception was raised
	try:
			config.get('SETTING', 'target_group')

		# If it doesn't i.e. An exception was raised
	except configparser.NoOptionError:
		print("Config error! No option called target_group.")
	try:
			config.get('SETTING', 'pax_size')

		# If it doesn't i.e. An exception was raised
	except configparser.NoOptionError:
		print("Config error! No option called pax_size.")
	try:
			config.get('SETTING', 'pax_rest')

		# If it doesn't i.e. An exception was raised
	except configparser.NoOptionError:
		print("Config error! No option called pax_rest.")
	try:
			config.get('SETTING', 'invite_interval')

		# If it doesn't i.e. An exception was raised
	except configparser.NoOptionError:
		print("Config error! No option called invite_interval.")
	try:
			config.get('SETTING', 'flood_rest')

		# If it doesn't i.e. An exception was raised
	except configparser.NoOptionError:
		print("Config error! No option called flood_rest.")
	try:
			config.get('SETTING', 'api_id')

		# If it doesn't i.e. An exception was raised
	except configparser.NoOptionError:
		print("Config error! No option called api_id.\n")
	try:
			config.get('SETTING', 'api_hash')

		# If it doesn't i.e. An exception was raised
	except configparser.NoOptionError:
		print("Config error! No option called api_hash.\n")
		
#CONVERT CONFIGURATION START!	__EDIT HERE__		__EDIT HERE__		__EDIT HERE__		__EDIT HERE__		__EDIT HERE__		__EDIT HERE__	
target_group = str(config['SETTING']['target_group']) # group username without @
pax_size = int(config['SETTING']['pax_size']) # How many person after x member invited (integer only)
pax_rest = int(config['SETTING']['pax_rest']) # How much {pax_rest} seconds after invited {pax_size} member
invite_interval = int(config['SETTING']['invite_interval']) # Invite 1 member every {invite_interval} seconds
flood_rest = int(config['SETTING']['flood_rest']) # Anti flood time in seconds. Pause script for {flood_rest} seconds to Prevent account from spam punishment.
api_id = int(config['SETTING']['api_id']) # api id for Telegram API
api_hash = str(config['SETTING']['api_hash']) # Api Hash for Telegram API

#CONVERT CONFIGURATION END!	__EDIT HERE__		__EDIT HERE__		__EDIT HERE__		__EDIT HERE__		__EDIT HERE__		__EDIT HERE__	

# WELCOME BLOCK
print(Fore.MAGENTA + '		__      _____ _    ___ ___  __  __ ___ ')
print(Fore.MAGENTA + '		\ \    / / __| |  / __/ _ \|  \/  | __|')
print(Fore.MAGENTA + '		 \ \/\/ /| _|| |_| (_| (_) | |\/| | _| ')
print(Fore.MAGENTA + '		  \_/\_/ |___|____\___\___/|_|  |_|___|\n' + Fore.RESET)
print(Fore.CYAN + '		       -   TeleInviter Script   -    ' + Fore.RESET)
#if len(sys.argv) > 3:
#print(Fore.CYAN + '		         -    ' + Fore.BLUE + 'Telegram' Fore.WHITE + '\\' + Fore.RED + 'Jom' + Fore.YELLOW + 'Donator' + Fore.CYAN + '    -    \n' + Fore.RESET)
#elif len(sys.argv) <= 3:
print(Fore.CYAN + '		   -    ' + Fore.WHITE + 'youtube.com' + Fore.WHITE + '//' + Fore.RED + 'Zizi' + Fore.WHITE + 'Works' + Fore.CYAN + '    -   \n' + Fore.RESET)

try:
    sys.argv[1]
except IndexError:
	print('\n' + Fore.CYAN + 'What is your telegram number?')
	phone = input('Input number in international format (example: +60123456789) :')
else:
    phone = sys.argv[1]
try:
    sys.argv[2]
except IndexError:
	print('\n' + Fore.CYAN + 'What is your username file named?')
	while True:
		filename = input('Username file ? (example: filename.txt or filename.csv)  :')
		try:
			file=open(filename, 'r').read()
			if file:
				break
		except IOError:
			print (Fore.RED + "\nThere is no such a file, please try again\n")
else:
    filename = sys.argv[2]
	
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
	client.send_code_request(phone)
	try:
		client.sign_in(phone, input('Enter the code: '))
	except SessionPasswordNeededError:
		pword = input('Enter the 2FA Password: ')
		client.sign_in(password=pword)
me = client.get_me()

print(Fore.CYAN + 'Configuration: \n' + Fore.RESET + '	Invite a new member every ' + Fore.RED + str(invite_interval) + Fore.RESET + ' seconds.')
print(Fore.RESET + '	When invited ' + Fore.RED + str(pax_size) + Fore.RESET + ' new member, rest for ' + Fore.RED + str(pax_rest) + Fore.RESET + ' seconds.')
print(Fore.RESET + '	When got flooding warning from Telegram, rest for ' + Fore.RED + str(flood_rest) + Fore.RESET + ' seconds.\n')
print(Fore.CYAN + 'Targeted group: '+ Fore.RESET + '@' + target_group)
#print(Fore.CYAN + 'App api_id: '+ Fore.RESET + api_id)
#print(Fore.CYAN + 'App api_hash: '+ Fore.RESET + api_hash)
print(Fore.CYAN + 'Current account: ' + Fore.RESET + f'{me.first_name}({me.username})')
print(Fore.CYAN + 'Phone Number : ' + Fore.RESET + phone)
print(Fore.CYAN + 'Username file : ' + Fore.RESET + filename)
print('	')
#if len(sys.argv) > 3:
	#print(Fore.RESET + '	Hi' + Fore.GREEN + ' Donator' + Fore.RED + '!!	' + Fore.RESET + 'Hi' + Fore.GREEN + ' Donator' + Fore.RED + '!!	' + Fore.RESET + 'Hi' + Fore.GREEN + ' Donator' + Fore.RED + '!!	' + Fore.RESET + 'Hi' + Fore.GREEN + ' Donator' + Fore.RED + '!!	' + Fore.RESET + 'Hi' + Fore.GREEN + ' Donator' + Fore.RED + '!!	' + Fore.RESET + 'Hi' + Fore.GREEN + ' Donator' + Fore.RED + '!!\n' + Fore.RESET)

#0#filename = sys.argv[2]
# JOIN CHANNEL START
client(JoinChannelRequest(target_group))
# JOIN CHANNEL END
users = []
with open(filename) as f:
	rows = f.readlines()
	print('-----------------')
	total_username = (len(rows))
	print(Fore.CYAN + 'Total username loaded:' + Fore.RESET + str(total_username))
	print('-----------------\n')
for row in rows:
	cusername = row.rstrip()
	#next(rows, None)
	#print(users.rstrip())
	user = {}
	user['username'] = cusername
	users.append(user)
n = 0
for user in users:
    n += 1
    print(Fore.GREEN + "Username number : " + Fore.RESET + str(n))
    #if n % 50 == 0:
    if n % pax_size == 0:
	    print(Fore.YELLOW + "Invited " + Fore.RED + str(n) + Fore.YELLOW + " members to " + Fore.WHITE + target_group)
	    print(Fore.YELLOW + "Hold for " + str(pax_rest) + " seconds." + Fore.RESET)
	    time.sleep(pax_rest)
    try:
        if user['username'] == "":
                continue
        user_to_add = client.get_input_entity(user['username'])
        client(InviteToChannelRequest(target_group,[user_to_add]))
        print(Fore.GREEN + "Username : " + Fore.RESET + (user['username']))
        print(Fore.YELLOW + "Inviting interval, wait for " + str(invite_interval) + " seconds..\n" + Fore.RESET)
        time.sleep(invite_interval)
        continue
    except PeerFloodError:
        print(Fore.RED + "Getting Flood Error from telegram. Script is stopping now. Please try again after some time." + Fore.RESET)
        #time.sleep(flood_rest)
        exx = input('Press any key to exit...')
        wait = 0
        if exx == wait:
            print(Fore.YELLOW + "Waiting for " + str(flood_rest) + " seconds..\n" + Fore.RESET)
            time.sleep(flood_rest)
        else: exit(1)
    except UserPrivacyRestrictedError:
        print(Fore.RED + "The user's privacy settings do not allow you to invite. Skipping..\n" + Fore.RESET)
        continue
    except UserNotMutualContactError:
        print(Fore.RED + "The user's is not a mutual contact and do not allow you to invite. Skipping..\n" + Fore.RESET)
        continue
    except errors.FloodWaitError as floodwait:
        print(Fore.RED + "Login locked.  fail to login around 5 times consider using another account." + Fore.RESET)
        print(Fore.RED + 'Login Locked!' + Fore.YELLOW + ' Have to sleep', floodwait.seconds, 'seconds..' + Fore.RESET)
        e = input('Press any key to exit...')
        exit(1)
    except UserBannedInChannelError:
        print(Fore.RED + "You're banned from sending messages in supergroups/channels." + Fore.RESET)
        e = input('Press any key to exit...')
        exit(1)
    except:
        traceback.print_exc()
        print(Fore.RED + "Unexpected Error" + Fore.RESET)
        continue