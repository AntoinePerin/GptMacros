import pyautogui
import time
from tkinter import messagebox

def run_macro_1():
    time.sleep(5)
    pyautogui.write('Bonjour, ceci est une simulation de macro clavier 1.', interval=0.1)
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('ctrl', 'v')
    messagebox.showinfo("Info", "Macro 1 terminée")

def run_macro_2():
    time.sleep(5)
    pyautogui.write('Bonjour, ceci est une simulation de macro clavier 2.', interval=0.1)
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('alt', 'tab')
    messagebox.showinfo("Info", "Macro 2 terminée")
