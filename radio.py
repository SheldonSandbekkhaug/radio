#!/usr/bin/env python

""" Written by Sheldon Sandbekkhaug.
    All rights reserved.

"""

import os
import sys
import wave
import random

import pygame
from pygame.locals import QUIT, KEYDOWN, K_p, K_q, K_s
from pygame import mixer

music_queue = None
music_queue_position = -1
SONG_ENDED = pygame.USEREVENT + 1


def main():
    """ Initialize radio and play sounds """
    music_directory = 'music'
    songs = get_list_of_songs(music_directory)
    if (len(songs) <= 0):
        print("Please place a .wav file in the directory %s" % directory)

    # Initialize mixer with correct frame rate
    mixer.pre_init(get_frame_rate(music_directory + '/' + songs[0]))

    pygame.init()
    display = pygame.display.set_mode((800,600),0,32)
    pygame.display.set_caption("radio.py")

    mixer.music.set_endevent(SONG_ENDED)

    print("Press S to skip the current song.")
    print("Press P to return to the previous song.")

    # Randomize the music queue and start it
    global music_queue
    music_queue = generate_queue('music', len(songs))
    play_next(music_queue, -1)

    # Could use play_random_song if we wanted to play a single song
    # play_random_song(queue, None)

    # Wait for an interrupt
    exit = False
    while (exit == False):
        # Can call non-radio.py application functions in this loop
        if (handle_events() == 'EXIT'):
            exit = True

    # Terminate gracefully
    pygame.quit()
    sys.exit()


def handle_events():
  """ Handle user input and other events. Return 'EXIT' if we should stop the
  program.

  """
  for event in pygame.event.get():
    if (event.type == QUIT or 
      (event.type == KEYDOWN and event.key == K_q)):
        return 'EXIT'
    elif (event.type == KEYDOWN and event.key == K_s):
        # Skip the current song
        play_next(music_queue, music_queue_position)
    elif (event.type == KEYDOWN and event.key == K_p):
        # Go back to the previous song
        play_prev(music_queue, music_queue_position)
    elif (event.type == SONG_ENDED):
        # Song ended naturally, play next
        play_next(music_queue, music_queue_position)


def get_list_of_songs(directory):
    """ Return a list of supported sound files in directory """
    files = os.listdir(directory)
    songs = []
    for file in files:
        if (file.endswith(".wav") or file.endswith(".mp3") or 
          file.endswith(".ogg")):
            songs.append(file)
    return songs


def play_random_song(songs, previous_song):
    """ Select one random song from the list of songs and play it.
    Does not select the previous song. Good to if you want to
    one-off a random song.

    """
    music_filename = previous_song
    while (music_filename == previous_song):
        music_filename = "music/" + random.sample(songs, 1)[0]

    mixer.music.load(music_filename)
    mixer.music.play(0,0)


def get_frame_rate(filepath):
    """ Return the frame rate of a wav file.
    Returns an integer.

    """
    try:
        sound_file = wave.open(filepath, 'r')
        frame_rate = sound_file.getframerate()
        sound_file.close()
        return frame_rate
    except:
        return 8000 # Default


def generate_queue(directory, n):
    """ Create a random list of n songs selected from the given
    directory with no repeats.

    Returns a list of filpaths (strings) to the songs in the queue.

    """
    songs = get_list_of_songs(directory)
    for i in xrange(len(songs)):
        songs[i] = directory + '/' + songs[i]

    random.shuffle(songs) # Shuffles in-place
    return songs    


def play_next(queue, position):
    """ Stop playing the current song (if any) and play the next song in 
    the queue.

    queue is a list of songs (strings)
    position the index of the current song in the queue

    """
    mixer.music.stop();

    new_position = position + 1
    if (new_position >= len(queue)):
        # Don't play anything if we're at the end of the queue
        return
    else:
        song_filename = queue[new_position]
        mixer.music.load(song_filename)
        mixer.music.play(0,0)
        global music_queue_position
        music_queue_position = new_position


def play_prev(queue, position):
    """ Stop playing the current song (if any) and play the previous song in
    the queue.

    queue is a list of songs (strings)
    position the index of the current song in the queue

    """
    mixer.music.stop()

    new_position = position - 1

    if (new_position <= len(queue)):
        # Play the current song if we're at the beginning of the queue
        mixer.music.play(0,0)
        return
    else:
        song_filename = queue[new_position]
        mixer.music.load(song_filename)
        mixer.music.play(0,0)
        global music_queue_position
        music_queue_position = new_position

if __name__ == "__main__":
    main()
