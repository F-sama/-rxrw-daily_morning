from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']

birthday = os.environ['BIRTHDAY']

engage_date = os.environ['ENGAGE_DATE']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id_fly = os.environ["USER_ID_FLY"]
user_id_baby = os.environ["USER_ID_BABY"]
template_id = os.environ["TEMPLATE_ID"]




def get_count_love():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_count_engage():
  delta = today - datetime.strptime(engage_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_loveday():
  next = datetime.strptime(str(date.today().year) + "-" +start_date[5:], "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_engageday():
  next = datetime.strptime(str(date.today().year) + "-" + engage_date[5:], "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
data = {"love_days":{"value":get_count_love()},"loveAnniversary_left":{"value":get_loveday()},"engage_days":{"value":get_count_engage()},"engageAnniversary_left":{"value":get_engageday()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res_baby = wm.send_template(user_id_baby, template_id, data)
res_fly = wm.send_template(user_id_fly, template_id, data)
print(res_baby)
print(res_fly)
