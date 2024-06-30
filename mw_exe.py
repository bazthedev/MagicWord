# Magic Word

import threading
import tkinter as tk
from tkinter import ttk
import pynput
from tkinter import messagebox as mb
from PIL import Image, ImageSequence, ImageTk
from playsound import playsound
from itertools import cycle
import time
import requests
import tempfile as tf
import zipfile as zf
import json

tmp = tf.gettempdir()
cdir = f"{tmp}\\content"
condir = f"{tmp}\\mw.json"
opend = False
try:
    with open(condir, "r") as _:
        config = json.load(_)
        opend = True
except FileNotFoundError:
    __ = open(condir, "w")
    __.write("{\"magic_word\": \"please\"}")
    __.close()
finally:
    if not opend:
        with open(condir, "r") as _:
            config = json.load(_)

_password = config["magic_word"]

def check_for_mouse_movement(_mouse):
    global appear
    global _stop
    while True:
        if _stop == True:
            break
        if _mouse.position != POSITION:
            sem.acquire()
            if appear != True:
                appear = True
            sem.release()

def lock_mouse_pos_login(_mouse):
    global _stop
    global _stop_login_lock
    while True:
        if _stop == True:
            break
        if _stop_login_lock:
            break
        if (_mouse.position[0] > POSITIONXL or _mouse.position[0] < POSITIONXS) or (_mouse.position[1] > POSITIONYL or _mouse.position[1] < POSITIONYS):
            _mouse.position = POSITION

def lock_mouse_pos(_mouse):
    global _quit
    while True:
        if _quit == True:
            break
        if (_mouse.position[0] > POSITION2XL or _mouse.position[0] < POSITION2XS) or (_mouse.position[1] > POSITION2YL or _mouse.position[1] < POSITION2YS):
            _mouse.position = POSITION

def check_appear():
    global appear
    global _stop
    while True:
        if _stop == True:
            break
        if appear:
            break
    login.deiconify()

def keyb_appear(key):
    global appear
    global _keyboard
    appear = True
    if key == pynput.keyboard.Key.alt_l:
        _keyboard.release(pynput.keyboard.Key.alt_l)

def check_pwd():
    global _stop
    global _stop_login_lock
    global _password
    if _pwd.get() != _password:
        _stop_login_lock = True
        _stop = True
        login.withdraw()
        login.quit()
    else:
        login.destroy()
        _stop = True
        mb.showinfo("Successful Login", "Your session has been restored.")
        exit()

def play_gif(imagelist, label):
    try:
        img = next(imagelist)
        label.img = ImageTk.PhotoImage(img)
        label.config(image=label.img)
        label.after(100, play_gif, imagelist, label) 
    except Exception as e:
        print(e)

def _audio():
    global _quit
    while True:
        if _quit:
            break
        playsound(f"{cdir}\\ahahah.mp3")
        time.sleep(13)
def dl_content():
    dl = requests.get("https://raw.githubusercontent.com/bazthedev/MagicWord/main/content.zip")
    with open(f"{tmp}\\content.zip", "wb") as dlz:
        dlz.write(dl.content)
        dlz.close()
    with zf.ZipFile(f"{tmp}\\content.zip", "r") as content:
        content.extractall(f"{tmp}\\content\\")

dl_content()
sem = threading.Semaphore()
_mouse = pynput.mouse.Controller()
_keyboard = pynput.keyboard.Controller()
POSITION = (1100, 575)
POSITIONXS = 1000
POSITIONXL = 1200
POSITIONYS = 550
POSITIONYL = 625
POSITION2XS = 650
POSITION2XL = 1290
POSITION2YS = 350
POSITION2YL = 750
WINICONPATH = "C:\\Windows\\System32\\@WLOGO_48x48.png"
_mouse.position = POSITION
appear = False
_stop = False
_quit = False
_stop_login_lock = False
with Image.open(f"{cdir}\\ahahah.gif") as im:
    imagelist = cycle(ImageSequence.all_frames(im))

listener = pynput.keyboard.Listener(on_press=keyb_appear)
listener.start()
root = tk.Tk()
root.withdraw()
login = tk.Toplevel(root)
login.lift()
login.attributes("-topmost", True)
login.withdraw()
login.geometry("200x100+1000+500")
login.resizable(False, False)
login.title("Login")
try:
    ico = Image.open(WINICONPATH)
    photo = ImageTk.PhotoImage(ico)
    login.wm_iconphoto(False, photo)
except Exception as e:
    print(e)
_message = tk.Label(login, text="Your session has timed out.\nPlease login again.")
_message.pack()
_pwd = tk.StringVar()
_password_field = tk.Entry(login, bg="light grey", textvariable=_pwd)
_password_field.pack()
_submit = tk.Button(login, text="Login", command=check_pwd)
_submit.pack()

cfmm = threading.Thread(target=check_for_mouse_movement, args=(_mouse,))
cfmm.start()
cat = threading.Thread(target=check_appear)
cat.start()
lmpl = threading.Thread(target=lock_mouse_pos_login, args=(_mouse,))
lmpl.start()
login.mainloop()
word = tk.Toplevel(root)
word.withdraw()
word.title("Ah ah ah, you didn't say the magic word!")
try:
    ico = Image.open(f"{cdir}\\icon.jpeg")
    photo = ImageTk.PhotoImage(ico)
    word.wm_iconphoto(False, photo)
except Exception as e:
    print(e)
word.resizable(False, False)
word.geometry("640x480+650+300")
ah = tk.PhotoImage(master=word, file=f"{cdir}\\ahahah.gif", format="gif -index 2")
_label = ttk.Label(word, image=ah)
_label.pack()
word.lift()
word.attributes("-topmost", True)
word.after(10, play_gif, imagelist, _label)
a = threading.Thread(target=_audio)
a.start()
lmp = threading.Thread(target=lock_mouse_pos, args=(_mouse,))
lmp.start()
word.deiconify()
word.mainloop()
_quit = True
