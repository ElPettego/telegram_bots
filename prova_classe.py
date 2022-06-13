from telegram_user_adder import tg_user_adder as tua
import time


# SBIRULINO adder = tua(API_ID='13958087', API_HASH='03a1a4ac2fb742462eafb27ed9d346d6', PHONE='+393518054323')
# UOMO SUCCO 
adder = tua(API_ID='11901714', API_HASH='f71bf8974d74b1402b9a11bf224c6094', PHONE='+393922660869')

adder.AddToGroup(CSV_FILE='user_list_api.csv')