import win32api
import win32con
import time
while True:
	win32api.keybd_event(13,0,0,0)
	win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
	time.sleep(60)