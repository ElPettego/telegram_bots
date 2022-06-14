import sys
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import UserNotMutualContactError, PeerFloodError, UserPrivacyRestrictedError, UserChannelsTooMuchError, FloodWaitError
import csv
import random
import traceback 
import time
import datetime
from random import randrange

class tg_user_adder():

    def __init__(self, API_ID, API_HASH, PHONE):
        self.API_ID = API_ID #'11901714'
        self.API_HASH = API_HASH #'f71bf8974d74b1402b9a11bf224c6094'
        self.PHONE = PHONE #'+393922660869'
        global client

        client = TelegramClient(PHONE, API_ID, API_HASH)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(PHONE)
            client.sign_in(PHONE, input('CODE: '))
        #client.disconnect()        

    def AddToGroup(self, CSV_FILE):

        input_file = CSV_FILE
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                try:
#                    user['user_id'] = int(row[1])
                    user['access_hash'] = row[2]
                except IndexError:
                    print ('users without id or access_hash')
                users.append(user)

        random.shuffle(users)
        chats = []
        last_date = None
        chunk_size = 10
        groups=[]

        result = client(GetDialogsRequest(
                    offset_date=last_date,
                    offset_id=0,
                    offset_peer=InputPeerEmpty(),
                    limit=chunk_size,
                    hash = 0
                ))
        chats.extend(result.chats)

        for chat in chats:
            groups.append(chat)            

        print('Choose a group to add members:')
        i=0
        for group in groups:
            print(str(i) + ' - ' + group.title)
            i+=1

        g_index = input("Enter a Number: ")
        target_group=groups[int(g_index)]
        print('\n\nChosen Group:\t' + groups[int(g_index)].title)

        target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

        mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

        #error_count = 0
        success_count = 0

        for user in users:
            print('============================================================================= ACCOUNT AGGIUNTI: '+ str(success_count) + ' !!! ' + str(datetime.datetime.now()))
            try:
                if user['username'][len(user['username'])-3:len (user['username'])].upper() == 'BOT':
                    break
                print ("Adding {}".format(user['username']))
                if mode == 1:
                    if user['username'] == "":
                        continue
                    user_to_add = client.get_input_entity(user['username'])
                elif mode == 2:
                    user_to_add = InputPeerUser(user['id'], user['access_hash'])
                else:
                    sys.exit("Invalid Mode Selected. Please Try Again.")
                client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                sleep_time = randrange(120, 180)
                print("Waiting " + str(sleep_time) + " Seconds...")
                time.sleep(sleep_time)
                success_count = success_count + 1
                if success_count % 10 == 0:
                    time_to_sleep = randrange(300, 500)
                    print(str(datetime.datetime.now()) + ' --- time to sleep: ' + str(time_to_sleep))
                    time.sleep(time_to_sleep)
            except (PeerFloodError, FloodWaitError):
                traceback.print_exc()
                print("Getting Flood Error from Telegram. You should stop script now.Please try again after some time. 30 min cooldown started at: " + str(datetime.datetime.now()))
                print('=============================================================================')
                time.sleep(1800)
            except (UserPrivacyRestrictedError, UserNotMutualContactError):
                print("The user's privacy settings do not allow you to do this. Skipping.")
                print('=============================================================================')
            except UserChannelsTooMuchError:
                print("User is in too many channels")
                print('=============================================================================')
            except:
                traceback.print_exc()
                print("Unexpected Error")                
                print('=============================================================================')
                continue

        client.disconnect()