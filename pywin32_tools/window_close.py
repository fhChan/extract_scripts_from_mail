import win32gui,win32con
import time
 
def handle_window(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd):
        if 'abcabc' in win32gui.GetWindowText(hwnd):
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
 
 
if __name__ == '__main__':
	while True:
		win32gui.EnumWindows(handle_window, None)
 		time.sleep(10)
    # TODO If app didn't close, force close.