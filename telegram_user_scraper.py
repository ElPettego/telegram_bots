from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

API_ID = '11901714' #'13958087' #'11901714'
API_HASH = 'f71bf8974d74b1402b9a11bf224c6094' # '03a1a4ac2fb742462eafb27ed9d346d6' #
PHONE = '+393922660869' #'+393518054323' #

client = TelegramClient(PHONE, API_ID, API_HASH)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(PHONE)
    client.sign_in(PHONE, input('CODE: '))

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))

chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except:
        continue

print('CHOOSE GROUP TO SCRAPE')
i=0
for g in groups:
    print(str(i) + ' - ' + g.title)
    i+=1

g_index = input('group number: ')
target_group = groups[int(g_index)]

all_participants = []
all_participants = client.get_participants(target_group)
with open('user_list_api.csv', 'a', encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    writer.writerow(['username', 'user_id', 'access_hash', 'name', 'group', 'group_id'])
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ''
        if user.first_name:
            first_name = user.first_name
        else:
            first_name=''
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ''
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title,target_group.id])
    print('File written succesfully')


