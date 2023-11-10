import pyautogui
import time
from main import get_members_of_chat



with pyautogui.hold('alt'):
    pyautogui.press(['tab'])
    pyautogui.press(['tab'])


members = get_members_of_chat(-1001778892228)
for member in members:
    pyautogui.click(825, 1001)
    pyautogui.typewrite(f'@usinfobot {member}')
    pyautogui.moveTo(883, 888, duration=1.5)
    pyautogui.click()
    pyautogui.moveTo(1545, 1005)
    pyautogui.dragTo(700,1005)
