import os
import pygame
import time
import threading
from pathlib import Path


#would have to make new global var queuelist that retains information. figure out how to remove once done
queuelist = []
mp3_files = []
paused = False
current_folder = None
playing = False   # True while a song is supposed to be playing


def watcher():
    global playing
    while True:
        time.sleep(0.5)
        # get_busy() is False while paused, so check the flag too
        if playing and not paused and not pygame.mixer.music.get_busy():
            if queuelist:
                next_song = queuelist.pop(0)
                pygame.mixer.music.load(os.path.join(current_folder, next_song))
                pygame.mixer.music.play()
                print(f"\nnow playing: {next_song}")
                print(f"Queue: {queuelist}")
                print("> ", end="", flush=True)
            else:
                playing = False
                print("\nqueue finished. press enter / type STOP to return home")
                print("> ", end="", flush=True)


def queuemusic(folder, song_name):
    #path song 
    file_path = os.path.join(folder, song_name)
    if not os.path.exists(file_path):
        print("file not found")
        return
    
    #this is causing issues
    queuelist.append(song_name)
    print(f"Queue: {queuelist}")
    print("----------------------------------------")
    return

def play_music(folder, song_name):
    global paused, playing, current_folder
    file_path = os.path.join(folder, song_name)
    if not os.path.exists(file_path):
        print("file not found")
        return

    current_folder = folder
    paused = False
    playing = True
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    #if there is something in the queue list print it. if not then don't

    print("----------------------------------------")
    print(f"now playing: {song_name}")
    print("commands: [Pause], [Resume], [Stop], [Queue], [Skip]")
    if not queuelist:
        print("Queue: []")
    else:
        print(f"Queue: {queuelist}")

    while True:

        command = input("> ").upper()

        if command == "PAUSE":
            pygame.mixer.music.pause()
            paused = True
            print("Paused")
        elif command == "RESUME":
            pygame.mixer.music.unpause()
            paused = False
            print("Resumed")
        elif command == "QUEUE":
            queue = input("input song # to queue: ")
            if not queue.isdigit():
                print("invalid number, input a new command")
                continue
            queue1 = int(queue) - 1
            if 0 <= queue1 < len(mp3_files):
                queuemusic(folder, mp3_files[queue1])
            else:
                print("song index does not exist")
            #figure out how to queue music
        elif command == "SKIP":
            paused = False
            if not queuelist:
                playing = False
                pygame.mixer.music.stop()
                print("no songs in queue. sending back to home")
                time.sleep(1)
                return
            pygame.mixer.music.stop()
        elif command == "STOP" or command == "QUIT":
            playing = False
            queuelist.clear()
            pygame.mixer.music.stop()
            print("Stopped")
            return
        else:
            print("Invalid command")


def main():
    try:
        pygame.mixer.init()
    except  pygame.error as e:
        print("failed to initialize mixer", e)
        return
    
    threading.Thread(target=watcher, daemon=True).start()
    folder = Path("C:/Users/User/Music")

    if not os.path.isdir(folder):
        #os.path.isdir() checks if folder exists
        print(f"Folder '{folder} 'not found")
        return
    
    for file in os.listdir(folder):
        if file.endswith("mp3"):
            mp3_files.append(file)
    
    while True:
        print("------------mp3 player------------")
        for index, song in enumerate(mp3_files, start=1):
            print(f"{index}: {song}")

        choice_input = input("\nEnter the song # to play (or 'Q' to quit): ")
        if choice_input.upper() == "Q":
            print("closing..")
            break
        if not choice_input.isdigit():
            print("enter valid num")
            continue
        choice = int(choice_input) - 1

        if 0 <= choice < len(mp3_files):
            play_music(folder, mp3_files[choice])
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
#basically this is the code that runs only if the script is executed directly. this code doesn't run when it's imported
#without this importing a file runs the entire file when importing it. when imported __name__ becomes file name
