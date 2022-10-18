from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.wave import WAVE
import tkinter.ttk as ttk
import os
from pathlib import Path

#Set home directory
home=str(Path.home())

#Create UI Window
root = Tk()
root.title("WAV Music Player")
root.geometry("500x300")
#Initialize Pygame Mixer
pygame.mixer.init()

#Create "Add Song" Function
def add_songs():
    songs = filedialog.askopenfilenames(initialdir="Music", title="Choose Songs", filetypes=(("WAV files", "*.wav"), ))
    for song in songs:
        song = song.replace("C:/Users/brett/Music/", "")
        song = song.replace(".wav", "")
        playlist_box.insert(END, song)

#Create "Remove Song" Function
def remove_song():
    playlist_box.delete(ACTIVE)
    pygame.mixer.music.stop()
    status_bar.config(text='')
    playlist_box.selection_clear(0, END)

#Create "Remove all songs" Function
def remove_songs():
    playlist_box.delete(0, END)
    pygame.mixer.music.stop()
    status_bar.config(text='')
    playlist_box.selection_clear(0, END)
    

#Play selected song
def play():
    song = playlist_box.get(ACTIVE)
    song = f"C:/Users/brett/Music/{song}.wav"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_time()
    
    

#Create Global Pause Variable
global paused
paused = False

#Pause and unpause song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused == True:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#Skip to the next song in playlist
def next():
    next_song = playlist_box.curselection()
    next_song = next_song[0]+1
    song = playlist_box.get(next_song)
    #Add directory structure
    song = f"C:/Users/brett/Music/{song}.wav"
    #Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    #Clear active selection
    playlist_box.selection_clear(0, END)
    #Set active selection to the next song
    playlist_box.activate(next_song)

    #Set active bar to the next song
    playlist_box.selection_set(next_song, last=None)

    #Update slider to position
    slider_postion = int(song_length)
    

#Create Back button
def back():
    previous_song = playlist_box.curselection()
    previous_song = previous_song[0]-1
    song = playlist_box.get(previous_song)
    #Add directory structure
    song = f"C:/Users/brett/Music/{song}.wav"
    #Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    #Clear active selection
    playlist_box.selection_clear(0, END)
    #Set active selection to the previous song
    playlist_box.activate(previous_song)

    #Set active bar to the previous song
    playlist_box.selection_set(previous_song, last=None)

    
    
#Get song length information
def song_time():
    #Find active song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000
    #Convert to time format
    converted_time = time.strftime("%M:%S", time.gmtime(current_time))
    #Get currently playing song
    song = playlist_box.get(ACTIVE)
    #Add directory structure
    song = f"C:/Users/brett/Music/{song}.wav"
    
    
    #Load song
    song_mutagen = WAVE(song)
    #Get song length
    global song_length
    song_length = song_mutagen.info.length
    #Convert to time format 
    song_mutagen_converted = time.strftime("%M:%S", time.gmtime(song_length))
    #Increase current time to 1 second
    current_time +=1
    
    #Output time to status bar
    status_bar.config(text=f'{converted_time} of {song_mutagen_converted}')
    #Update slider to song position
    slider_postion = int(song_length)
    
    
    #Update time every second
    status_bar.after(1000, song_time)

#Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


#Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)
    
#Create Playlist Box
playlist_box = Listbox(master_frame, bg="black", fg="white", selectbackground="white", selectforeground="black", width=60)
playlist_box.grid(row=0, column=0)


#Create the status bar
status_bar = Label(master_frame, text=" ", bd=10, relief=FLAT) 
status_bar.grid(row=3, column=0)

#Create Player Control Buttons
back_button_img = PhotoImage(file="C:/Users/brett/OneDrive/Documents/Coding Projects/MP3 Player/backbutton.png")
forward_button_img = PhotoImage(file="C:/Users/brett/OneDrive/Documents/Coding Projects/MP3 Player/forwardbutton.png")
play_button_img = PhotoImage(file="C:/Users/brett/OneDrive/Documents/Coding Projects/MP3 Player/playbutton.png")
pause_button_img = PhotoImage(file="C:/Users/brett/OneDrive/Documents/Coding Projects/MP3 Player/pausebutton.png")

#Create Player Control Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=2)

#Create Player Control Buttons
back_button = Button(controls_frame, image=back_button_img, borderwidth=0, command=back)
forward_button = Button(controls_frame, image=forward_button_img, borderwidth=0, command=next)
play_button = Button(controls_frame, image=play_button_img, borderwidth=0, command=play) 
pause_button = Button(controls_frame, image=pause_button_img, borderwidth=0, command=lambda: pause(paused))

back_button.grid(row=0, column=0)
play_button.grid(row=0, column=1)
pause_button.grid(row=0, column=2)
forward_button.grid(row=0, column=3)

#Create Volume Label Frame
volume_frame = LabelFrame(master_frame, text='Volume')
volume_frame.grid(row=0, column=1, padx=20)

#Create Volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)


#Create Menu
MainMenu = Menu(root)
root.config(menu=MainMenu)

#Create "Add Songs" Menu
add_songs_menu = Menu(root)
MainMenu.add_cascade(label="Add Songs", menu=add_songs_menu)
add_songs_menu.add_command(label="Add songs to playlist", command=add_songs)

#Create "Remove Song" Menu
remove_song_menu = Menu(root)
MainMenu.add_cascade(label="Remove songs", menu=remove_song_menu)
#Create "Remove selected song" option
#remove_song_menu.add_command(label="Remove selected song from playlist", command=remove_song)
#Create "Remove All Songs" option
remove_song_menu.add_command(label="Remove all songs from playlist", command=remove_songs)


root.mainloop()