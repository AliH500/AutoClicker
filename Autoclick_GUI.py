import time
import os
import sys
import threading
import random
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Listener, KeyCode, Controller as KeyboardController
import tkinter
from tkinter import messagebox
from customtkinter import *

window = CTk()
#window.geometry("800x400")
window_width = 700
window_height = 700
x_position = (1920-700)//2   #(window.winfo_screenwidth() - window_width) // 2
y_position = (1080-1050)//2  #(window.winfo_screenheight() - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

set_appearance_mode("dark")  # dark, light, system
window.resizable(False, False)


infopadx = 20
infopady = 10
fontname = "Helvetica"
fontsize = 20
appstatecolor = "#f75c03" #first label
appstatecolor2 = "#00cc66" #btncolor
appstatecolor3 = "#49e597" #btn hover color
tobepressed = ""
click_thread = None
listener_thread = None
Clicking = False
currentstate = False


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

window.title("Auto-Clicker by Ali Hani")


def clearmouse():
    if key_entry.get() == 1:
        mouse_entry.deselect()
        whichkey_entry.configure(state = "normal")
        whichkey_entry.configure(placeholder_text= "Enter Key(s)...")
        mouse_entry.configure(state = "disabled")
        leftmouse_entry.deselect()
        rightmouse_entry.deselect()
        leftmouse_entry.configure(state = "disabled")
        rightmouse_entry.configure(state = "disabled")
    else:
        mouse_entry.configure(state = "normal")
        whichkey_entry.delete(0, END)
        whichkey_entry.configure(state = "disabled")

def clearkey():
    if mouse_entry.get() == 1:
        key_entry.deselect()
        key_entry.configure(state = "disabled")
        leftmouse_entry.configure(state = "normal")
        rightmouse_entry.configure(state = "normal")
        whichkey_entry.delete(0, END)
        whichkey_entry.configure(state = "disabled")
    else:
        key_entry.configure(state = "normal")
        leftmouse_entry.deselect()
        rightmouse_entry.deselect()
        leftmouse_entry.configure(state = "disabled")
        rightmouse_entry.configure(state = "disabled")



def get_entry_length(entry_widget):
    entry_text = entry_widget.get()
    entry_length = len(entry_text)
    return entry_length

def get_character_at_index(entry_widget, index):
    entry_text = entry_widget.get()
    if 0 <= index < len(entry_text):
        return str(entry_text[index])
    else:
        return None  # Index out of range

def disable_all_widgets():
    for widget in info_frame.winfo_children():
        if isinstance(widget, (CTkEntry, CTkCheckBox, CTkSlider)):
            widget.configure(state="disabled")
    
    for widget in info2_frame.winfo_children():
        if isinstance(widget, (CTkEntry, CTkCheckBox, CTkSlider)):
            widget.configure(state="disabled")

def enable_all_widgets():
    for widget in info_frame.winfo_children():
        if isinstance(widget, (CTkEntry, CTkCheckBox, CTkSlider)):
            widget.configure(state="normal")
    
    for widget in info2_frame.winfo_children():
        if isinstance(widget, (CTkEntry, CTkCheckBox, CTkSlider)):
            widget.configure(state="normal")

def changecolors(appstate):
    global nlrmouse, tobepressed, appstatecolor, appstatecolor2, appstatecolor3
    
    app_state_label.configure(text_color = appstatecolor)
    toggleverify_label.configure(text_color = appstatecolor)
    keyverify_label.configure(text_color = appstatecolor)
    timeverify_label.configure(text_color = appstatecolor)
    button.configure(fg_color = appstatecolor2, hover_color = appstatecolor3)
    
    mins = min_entry.get()
    secs = sec_entry.get()
    if set_lowest.get() != 1: 
        timeverify_label.configure(text = "After every " +str(int(mins))+ " min and " +str(int(secs))+ " sec")
    else:
        timeverify_label.configure(text = "After every " +str(mins)+ " min and 0.01 sec")
    toggler = togglekey_entry.get()
    toggleverify_label.configure(text = "This "+ str(toggler) +" key will act as a toggle to start the program")

    if leftmouse_entry.get() == 1:
        keyverify_label.configure(text = "Left mouse button will be pressed")
        tobepressed = ""
    elif rightmouse_entry.get() == 1:
        tobepressed = ""
        keyverify_label.configure(text = "Right mouse button will be pressed")
    else:
        presskey = whichkey_entry.get()
        tobepressed = presskey 
        keyverify_label.configure(text = str(presskey) + " key will be pressed")
    
    if appstate:
        app_state_label.configure(text = "APP STATE: ON")
        button.configure(text = "STOP LISTENING")
    else:
        app_state_label.configure(text = "APP STATE: OFF")
        button.configure(text = "START LISTENING")


def listen():
    
    global  nlrmouse, tobepressed, click_thread, listener_thread
    
    activator = togglekey_entry.get()
    
    if set_lowest.get() == 1:
        waittime = 0.01
    else:
        waittime = (int(min_entry.get())*60) + int(sec_entry.get())

    #Press_key = KeyCode(char=tobepressed)
    Activate_Key = KeyCode(char=activator)

    mouse = MouseController()
    keyboard = KeyboardController()

    def clicker():
        global currentstate, Clicking
        while currentstate:
            if Clicking:
                if leftmouse_entry.get() == 1:
                    mouse.click(Button.left)
                elif rightmouse_entry.get() == 1:
                    mouse.click(Button.right)
                else:
                    for x in range(get_entry_length(whichkey_entry)):
                        Press_key = KeyCode(char = get_character_at_index(whichkey_entry, x))
                        keyboard.press(Press_key)
                        keyboard.release(Press_key)
                time.sleep(0.001)  # Adjust the sleep time to control the rate of clicks
            interval = waittime
            time.sleep(interval)

    def activation(key):
            global Clicking, currentstate
            if key == Activate_Key:
                Clicking = not Clicking
            elif currentstate == False:
                Clicking = False

    click_thread = threading.Thread(target=clicker, daemon = True)
    click_thread.start()

    listener_thread = threading.Thread(target=lambda:Listener(on_press=activation).start(), daemon = True)
    listener_thread.start()

def verify():
    global currentstate
    if currentstate:
        if (get_entry_length(togglekey_entry) == 0):
            tkinter.messagebox.showwarning(title="Error", message="Toggle key input left empty")
            btnfunc()
        elif (get_entry_length(togglekey_entry) > 1):
            tkinter.messagebox.showwarning(title="Error", message="Toggle key should only be 1 character")
            btnfunc()
        elif (leftmouse_entry.get() == 0) and (rightmouse_entry.get() == 0) and           (whichkey_entry.get()== ""):
            tkinter.messagebox.showwarning(title="Error", message="No action to do when toggle key is pressed")
            btnfunc()
        



def btnfunc():
    global appstatecolor, appstatecolor2, appstatecolor3, currentstate
    currentstate = not currentstate

    window.focus_set()
    if currentstate:
        appstatecolor = "#00cc66"
        appstatecolor2 = "#f75c03"
        appstatecolor3 = "#f78e52"
        disable_all_widgets()
        
        changecolors(currentstate)
    else:
        appstatecolor = "#f75c03"   #first label
        appstatecolor2 = "#00cc66"  #btncolor
        appstatecolor3 = "#49e597" #btnhover
        enable_all_widgets()
        changecolors(currentstate)

    if key_entry.get() == 1:
        clearmouse()
        whichkey_entry.configure(state = "disabled")
    else:
        clearkey()
    
    verify()
    listen()
    

#Frame
frame = CTkFrame(master=window, fg_color="#242424")
frame.pack(pady=30)

app_state_label = CTkLabel(frame, text="APP STATE: OFF", text_color="#f75c03", 
font=(fontname,fontsize+10))
app_state_label.grid(row=0, column=0, padx=infopadx, pady=infopady)

interval_label = CTkLabel(frame, text="Interval after each mouseclick/keypress", 
font=(fontname,fontsize+5), text_color = "#726da8")
interval_label.grid(row=1, column=0, padx=5, pady=0)

#Purple Frame
info_frame = CTkFrame(master=frame, fg_color="transparent", border_color="#726da8", border_width=3,)
info_frame.grid(row=2, column=0, padx=infopadx, pady=10)

#SLIDERS=======

sec_label = CTkLabel(info_frame, text="1 Second")
sec_label.grid(row=0, column=1)

def slider(value):
    sec_label.configure(text=str(int(value)) + " Seconds")
    set_lowest.deselect()

sec_entry = CTkSlider(info_frame, from_=1, to=60, command=slider, button_color= "#726da8", fg_color="white", button_hover_color= "#aaa2fa", progress_color= "#726da8")
sec_entry.grid(row=1, column=1)
sec_entry.set(1)

min_label = CTkLabel(info_frame, text="0 Minuite")
min_label.grid(row=0, column=0)

def slider(value):
    sec_label.configure(text = "1 Second")
    min_label.configure(text=str(int(value)) + " Minuites")
    set_lowest.deselect()

min_entry = CTkSlider(info_frame, from_=0, to=60, command=slider, button_color= "#726da8",fg_color="white", button_hover_color= "#aaa2fa", progress_color= "#726da8")
min_entry.grid(row=1, column=0)
min_entry.set(0)

#SLIDERS=======

#CHECKBOX===

def returnsliders():
    min_entry.set(0)
    sec_entry.set(0)
    min_label.configure(text= "0 Minuite")
    if set_lowest.get() == 1:
        sec_label.configure(text = "0.01 Second")
    else:
        sec_label.configure(text = "1 Second")

set_lowest = CTkCheckBox(master=info_frame, text="Set interval to lowest value (0.01s)", fg_color="#726da8", hover_color = "#aaa2fa", checkbox_height= 30, checkbox_width = 30, corner_radius = 36, command=returnsliders)
set_lowest.grid(row=2, column=0)

#CHECKBOX===

#Configure widgets inside purple frame
for widget in info_frame.winfo_children():
    widget.grid_configure(padx=infopadx, pady=infopady)
    if isinstance(widget, (CTkEntry, CTkLabel, CTkCheckBox)):
        widget.configure(font=(fontname, fontsize))



keyselect_label = CTkLabel(frame, text="Select Key/Mouse button", font=(fontname,fontsize+5), text_color = "#f56e9d")
keyselect_label.grid(row=3, column=0, padx=5, pady=0)

#Pink Frame
info2_frame = CTkFrame(master=frame, fg_color="transparent", border_color="#f56e9d", border_width=3,)
info2_frame.grid(row=4, column=0, padx=infopadx, pady=10)


key_entry = CTkCheckBox(master=info2_frame, text="Key character", fg_color="#f56e9d", hover_color = "#F6BDD1", checkbox_height=30, checkbox_width = 30, command=clearmouse)
key_entry.grid(row=0, column=0)

whichkey_entry = CTkEntry(master = info2_frame, placeholder_text= "Enter Key(s)..", width=250, state = "disabled")
whichkey_entry.grid(row=1, column=0)

togglekey_label = CTkLabel(info2_frame, text="Toggle Key")
togglekey_label.grid(row=2, column=0)

togglekey_entry = CTkEntry(master = info2_frame, placeholder_text= "Enter only 1 Key..", width=250)
togglekey_entry.grid(row=3, column=0)


mouse_entry = CTkCheckBox(master=info2_frame, text="Mouse button", fg_color="#f56e9d", hover_color = "#F6BDD1", checkbox_height=30, checkbox_width = 30, command=clearkey)
mouse_entry.grid(row=0, column=1)


def clearleftmouse():
    if rightmouse_entry.get() == 1:
        leftmouse_entry.deselect()

def clearrightmouse():
    if leftmouse_entry.get() == 1:
        rightmouse_entry.deselect()


rightmouse_entry = CTkCheckBox(master=info2_frame, text="Right mouse", fg_color="#f56e9d", hover_color = "#F6BDD1", checkbox_height= 30, checkbox_width = 30, corner_radius = 36, state = "disabled", command=clearleftmouse)
rightmouse_entry.grid(row=1, column=1)

leftmouse_entry = CTkCheckBox(master=info2_frame, text="Left mouse", fg_color="#f56e9d", hover_color = "#F6BDD1", checkbox_height=30, checkbox_width = 30, corner_radius = 36, state = "disabled", command=clearrightmouse)
leftmouse_entry.grid(row=2, column=1)


#Configure widgets inside pink frame
for widget in info2_frame.winfo_children():
    widget.grid_configure(padx=infopadx+2, pady=infopady)
    if isinstance(widget, (CTkEntry, CTkLabel, CTkCheckBox)):
        widget.configure(font=(fontname, fontsize))


button = CTkButton(master = frame, fg_color="#00cc66", text = "START LISTENING", font=(fontname,fontsize), hover_color = "#49e597", width=250, height=40, command=btnfunc)
button.grid(row=5, column=0, padx=infopadx, pady=infopady+5)

toggleverify_label = CTkLabel(frame, text="This __ key will act as a toggle to start the program", font = (fontname,15), text_color = appstatecolor)
toggleverify_label.grid(row=6, column=0, pady= 10)

timeverify_label = CTkLabel(frame, text="After every __ min and __ sec", font = (fontname,15), text_color = appstatecolor)
timeverify_label.grid(row=7, column=0)

keyverify_label = CTkLabel(frame, text="__ button will be pressed", font = (fontname,15), text_color = appstatecolor)
keyverify_label.grid(row=8, column=0)


window.mainloop()