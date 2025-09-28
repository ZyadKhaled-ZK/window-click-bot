
import ctypes
import sys
import pygetwindow as gw
import win32gui
import win32con
import win32api
import keyboard
import time

# ===== MAIN SCRIPT =====
def get_window_rect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    return rect

def list_open_windows():
    windows = {win32gui.GetWindowText(win._hWnd): win._hWnd for win in gw.getAllWindows() if win32gui.IsWindowVisible(win._hWnd)}
    print("\nOpen Applications:")
    for i, (title, hwnd) in enumerate(windows.items(), 1):
        print(f"{i}. {title}")
    choice = int(input("\nEnter the number of the application: "))
    return list(windows.values())[choice - 1] if 0 < choice <= len(windows) else None

def get_click_position(hwnd):
    print("Click inside the application and press SPACE to confirm...")
    keyboard.wait("space")
    rect = get_window_rect(hwnd)
    x, y = win32gui.GetCursorPos()
    return (x - rect[0], y - rect[1])

def send_click(hwnd, x, y):
    l_param = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    time.sleep(0.05)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, l_param)

def bot_loop(hwnd, x, y):
    print(f"\n🔍 Clicking at ({x}, {y}). Press Q to stop.")
    while not keyboard.is_pressed("q"):
        send_click(hwnd, x, y)
        time.sleep(1)
    print("Bot stopped.")

if __name__ == "__main__":
    target_hwnd = list_open_windows()
    if target_hwnd:
        click_x, click_y = get_click_position(target_hwnd)
        bot_loop(target_hwnd, click_x, click_y)
    else:
        print("❌ No window selected.")
