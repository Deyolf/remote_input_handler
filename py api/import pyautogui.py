import pyautogui 
import time

x=960
y=540

pyautogui.moveTo(x,y)

i=0

time.sleep(8)

while i<1000000:
    pyautogui.leftClick()
    i=i+1
    time.sleep(5)

#pyautogui.moveTo(x+10,y)
#x,y=pyautogui.position()
#print(x,y)
#x,y=pyautogui.position()
#pyautogui.moveTo(x-10,y)