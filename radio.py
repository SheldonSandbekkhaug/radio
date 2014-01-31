#!/usr/bin/env python

import os
import wave
import random

import pygame
from pygame import mixer


def main():
    """ Initialize radio and play sounds """
    mixer.pre_init(get_frame_rate()) # Initialize mixer with correct frame rate

    pygame.init()

    # Default directory for songs is "music"
    songs = get_list_of_songs("music")

    # Get the name of the first song to play
    music_filename = "music/" + random.sample(songs, 1)[0]
    previous_song = music_filename
    mixer.music.load(music_filename)

    # Start playing from random position in the song, as if you just tuned in
    # Note: some wav files don't support position setting
#   mixer.music.play(0, randint(0,60)) # TODO: programmatically check length
    mixer.music.play(0,0)    

    radio_on = True

    # Select next song
    while(radio_on == True):
        # Wait for the current song to finish
        if (mixer.get_busy() == False):
            play_random_song(songs, previous_song)
    
    # If the radio is turned off, stop playing music
    mixer.music.stop()


def get_list_of_songs(directory):
    """ Return a list of .wav files in directory """
    files = os.listdir(directory)
    songs = []
    for file in files:
        if (file.endswith(".wav")):
            songs.append(file)
    return songs


def play_random_song(songs, previous_song):
    """ Select a random song from the list of songs and play it.
    Does not select the previous song.

    """
    music_filename = previous_song
    while (music_filename == previous_song):
        music_filename = "music/" + random.sample(songs, 1)[0]

    mixer.music.load(music_filename)
    mixer.music.play(0,0)


def get_frame_rate():
    """ Return the frame rate of a wav file.
    Returns an integer.

    """
    sound_file = wave.open('music/chocoRain.wav', 'r')
    frame_rate = sound_file.getframerate()
    sound_file.close()
    print("frame rate: %i" % frame_rate) # TODO: remove
    return frame_rate


main()
