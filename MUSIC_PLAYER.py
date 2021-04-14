import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

statusbar = ttk.Label(root, text = 'Hello Friends! Welcome to Music Player', relief = SUNKEN, anchor = W, font = 'Times 12 italic' )
statusbar.pack(side = BOTTOM, fill = X)


# Code for Menubar
menubar = Menu(root)
root.config (menu = menubar)

# Code for Submenu
subMenu = Menu(menubar, tearoff=0)

play_list = []         # contains path along with file_path

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    add_to_playlist(file_path)

    mixer.music.queue(file_path)

def add_to_playlist(filename):
    filename = os.path.basename(file_path)
    index = 0
    playlist.insert(index, filename)
    play_list.insert(index, file_path)
    index += 1

def close():
    msgbox = tkinter.messagebox.askquestion('Music Player', 'Do you really want to exit?')
    if msgbox == 'yes':
       stop_music()
       root.destroy()
    else:
       tk.messagebox.showinfo('Return', 'Playing Music again')

menubar.add_cascade(label = "File", menu = subMenu)
subMenu.add_command(label = "Open", command = browse_file)
subMenu.add_command(label = "Exit", command = close)


def about_us():
    tkinter.messagebox.showinfo('About Music Player', 'This is a Python Miniproject named Music Player created by group MPC01 using Tkinter')

subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Help", menu = subMenu)
subMenu.add_command(label = "About Us", command = about_us)

mixer.init()

#root.geometry('400x400')
root.title("Music Player")
root.iconbitmap("MP.ico")

leftframe = Frame(root)
leftframe.pack(side = LEFT, padx=30, pady = 30)

playlist = Listbox(leftframe)
playlist.pack()

addButton = ttk.Button(leftframe, text = "+ ADD", command = browse_file)
addButton.pack(side = LEFT, pady = 2)

def delete_song():
    selected_song = playlist.curselection()
    selected_song = int(selected_song[0])
    playlist.delete(selected_song)
    play_list.pop(selected_song)

deleteButton = ttk.Button(leftframe, text = "- DELETE", command = delete_song)
deleteButton.pack(side = LEFT, pady = 2)

rightframe = ttk.Frame(root)
rightframe.pack(pady = 30)

topframe = ttk.Frame(rightframe)
topframe.pack()

length = ttk.Label(topframe, text='Total Length ~ --:--', font = 'Times 12 normal')
length.pack(pady=5)

currenttime = ttk.Label(topframe, text = 'Current Time ~ --:--', relief = GROOVE, font = 'Times 12 normal')
currenttime.pack()

def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    min, sec = divmod(total_length, 60)
    min = round(min)
    sec = round(sec)
    timeformat = '{:02d}:{:02d}'.format(min, sec)
    length['text'] = "Total Length" + ' ~ ' + timeformat

    t1 = threading.Thread(target=counter, args=(total_length,))
    t1.start()

def counter(t):
    global paused
    current_time = 0
    while current_time <=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            min, sec = divmod(current_time, 60)
            min = round(min)
            sec = round(sec)
            timeformat = '{:02d}:{:02d}'.format(min, sec)
            currenttime['text'] = "Current Time" + ' ~ ' + timeformat
            time.sleep(1)
            current_time += 1

def play_music():
    global paused

    if paused:
       mixer.music.unpause()
       statusbar['text'] = "Music Resumed" + " : " + "Playing" + ' - ' + os.path.basename(file_path)
       paused = FALSE
    else:
       try:
           stop_music()
           time.sleep(1)
           selected_song = playlist.curselection()
           selected_song = int(selected_song[0])
           play_it = play_list[selected_song]
           mixer.music.load(play_it)
           mixer.music.play()
           statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
           show_details(play_it)
       except:
           tkinter.messagebox.showerror('File not found', 'Music Player could not find the file. Please select a file.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def set_volum(val):
    volume = float(val)/100
    mixer.music.set_volume(volume)

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded" + " : " + "Playing" + ' - ' + os.path.basename(file_path)

muted = FALSE

def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.4)
        volumeButton.configure(image=volumePhoto)
        scale.set(40)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeButton.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE

middleframe = ttk.Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file='PLAY.png')
playButton = ttk.Button(middleframe, image=playPhoto, command=play_music)
playButton.grid(row = 0,column = 0, padx = 10)

stopPhoto = PhotoImage(file='stop.png')
stopButton = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopButton.grid(row = 0,column = 1, padx = 10)

pausePhoto = PhotoImage(file='pause.png')
pauseButton = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseButton.grid(row = 0,column = 2, padx = 10)

bottomframe = ttk.Frame(rightframe)
bottomframe.pack()

rewindPhoto = PhotoImage(file='rewind.png')
rewindButton = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindButton.grid(row = 0, column = 0)

mutePhoto = PhotoImage(file='mute.png')
volumePhoto = PhotoImage(file='volume.png')
volumeButton = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeButton.grid(row = 0, column = 1, padx=10)

scale = ttk.Scale(bottomframe, from_=0, to = 100,orient = HORIZONTAL, command = set_volum)
scale.set(40)
mixer.music.set_volume(0.4)
scale.grid(row = 0, column = 2, pady = 15)

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
