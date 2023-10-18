import time
import pywhatkit as kit
from urllib.parse import quote
import webbrowser as web
import pyautogui as pg



GROUP_ID = 'KVjQ5SWfCXS3gkClilMIyq'

def send_test_msg():
    web.open('https://web.whatsapp.com/accept?code=' + GROUP_ID)

    time.sleep(5)
    width, height = pg.size()
    pg.click(width / 2, height - height / 10)
    pg.typewrite('test4' + "\n")
    pg.press('enter')

    pg.typewrite('test5' + "\n")
    pg.press('enter')


def read_msg():
    time.sleep(5)
    width, height = pg.size()
    pg.click(width / 2, height -  20)

    pg.hotkey('command', 'a')
    print(pg.hotkey('command', 'c'))

read_msg()

