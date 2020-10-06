from googlesearch import search_videos
import vlc
import pafy
import time as t
import keyboard
import string
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
songs_in_queue = []
song_name = ""
Instance = vlc.Instance()
player = Instance.media_player_new()
skip = False
layout = GridLayout()
layout.cols = 2
time = 0
layout.add_widget(Label(text="Input command:"))
command_input = TextInput()
layout.add_widget(command_input)
current_song = Label(text="Current Song:")
layout.add_widget(current_song)
state = Label(text="Chilling")
layout.add_widget(state)
layout.add_widget(Label(text="Play time left:"))
time_left = Label(text="0")
layout.add_widget(time_left)
layout.add_widget(Label(text="In Queue:"))
next_song = Label(text="")
layout.add_widget(next_song)
def check_if_song_ended(sth):
    time = float(time_left.text.split(" ")[0])
    if (time > 0 and player.get_state() == 3):
        time -= 0.1
    time = round(time,1)
    if(player.get_state() == 6):
        time = 0.0
    time_left.text = str(time) + " Seconds"
    if(player.get_state() == 6 and songs_in_queue != []):
        check_if_next_song()
def execute_command(instance):
    global player,songs_in_queue,video
    try:
        song_name = video.title
    except:
        song_name = ""
    command = command_input.text
    command_input.text = ""
    if command == "pause":
        try:
            player.pause()
            state.text = "Paused " + song_name
        except:
            pass
    elif command == "stop":
        try:
            player.stop()
            state.text = "Skipped " + song_name
            check_if_next_song()
        except:
            pass
    elif command == "play":
        try:
            player.play()
            state.text = "Playing " + song_name
        except:
            pass
    elif command == "pop":
        songs_in_queue = songs_in_queue[:-1]
        next_song.text = ""
        for i in songs_in_queue:
            next_song.text += i+","
    else:
        if(songs_in_queue == [] and player.get_state() != 3 and player.get_state() != 4):
            songs_in_queue.append(command)
            state.text = "Searching " + songs_in_queue[0]
            check_if_next_song()
        else:
            songs_in_queue.append(command)
            next_song.text = ""
            for i in songs_in_queue:
                next_song.text += i + ","
start_button = Button(text="Send command",on_press=execute_command)
layout.add_widget(start_button)
class MyApp(App):
    def build(self):
        Clock.schedule_interval(check_if_song_ended,0.1)
        return layout
#searches = input("Video name or a list seperated by ,").split(",")
def check_if_next_song():
    if(songs_in_queue != []):
        play = songs_in_queue[0]
        songs_in_queue.pop(0)
        next_song.text = ""
        for i in songs_in_queue:
            #print(i)
            next_song.text += i + ","
        find_and_play_audio(play)
def find_and_play_audio(title):
    link = ""
    try:
        for j in search_videos(title,tld="co.in",num=1,stop=1,pause=2):
            link = j
        video = pafy.new(link)
        song_name = video.title
        time = video.duration.split(":")
        best = video.getbestaudio()
        playurl = best.url
        Media = Instance.media_new(playurl)
        player.set_media(Media)
        player.play()
        time = float(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])+2#extra seconds to load the music
        time_left.text = str(time) + " Seconds"
        current_song.text = "Current Song:"+song_name
        state.text = "Playing"
        t.sleep(0.2)
        '''current_state = player.get_state()
        while current_state != 6:
            current_state = player.get_state()
            if(skip):
                skip = False
                break
            for i in string.ascii_lowercase:
                if(keyboard.is_pressed(i)):
                    command += i
            if(keyboard.is_pressed(" ")):
                command += " "
            if (keyboard.is_pressed("backspace")):
                command = command[:-1]
            if(keyboard.read_key() == "ctrl"):
                command = command_input.text
                if(command != ""):
                    print("Command given")
                    entered = True
            time.sleep(0.05)'''
    except Exception as e:
        print(e)
        state.text = "Song Loading Failed."
        check_if_next_song()
    #check_if_next_song()
#while searches != []:
#    find_and_play_audio(searches[0])
#    searches.pop(0)
MyApp().run()