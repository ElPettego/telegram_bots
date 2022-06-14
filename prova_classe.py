from telegram_user_adder import tg_user_adder as tua
import time

# sbirulino
adder = tua(API_ID='13958087', API_HASH='03a1a4ac2fb742462eafb27ed9d346d6', PHONE='+393518054323')

adder.AddToGroup(CSV_FILE='user_list_api.csv')