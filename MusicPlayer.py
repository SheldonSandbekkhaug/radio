""" Written by Sheldon Sandbekkhaug.
    All rights reserved.

"""

import os
import sys
import wave
import random

import pygame
from pygame import mixer


class MusicPlayer(object):
  SONG_ENDED = pygame.USEREVENT + 1

  def __init__(self, music_directory):
    """ Initialize the MusicPlayer with the music in the given directory. 
    Needs to be called before pygame.init().

    """
    self.music_directory = music_directory
    songs = self.get_list_of_songs(self.music_directory)
    if (len(songs) <= 0):
      print("Please place a .wav file in the directory %s" % directory)
    
    # Initialize mixer with correct frame rate
    mixer.pre_init(self.get_frame_rate(music_directory + '/' + songs[0]))    

  def start_random_queue(self):
    """ Create the queue by randomizing a list of songs and start it. """
    mixer.music.set_endevent(MusicPlayer.SONG_ENDED)
    songs = self.get_list_of_songs(self.music_directory)
    
    # Randomize the music queue and start it
    self.music_queue = self.generate_queue('music', len(songs))
    self.music_queue_position = -1 # Incremented by self.play_next()
    self.play_next()
    
  def get_list_of_songs(self, directory):
    """ Return a list of supported sound files in directory """
    files = os.listdir(directory)
    songs = []
    for file in files:
      if (file.endswith(".wav") or file.endswith(".mp3") or 
          file.endswith(".ogg")):
        songs.append(file)
    return songs
    
  def play_random_song(self, songs, previous_song):
    """ Select one random song from the list of songs and play it.
    Does not select the previous song. Good to if you want to
    one-off a random song.

    """
    music_filename = previous_song
    while (music_filename == previous_song):
      music_filename = "music/" + random.sample(songs, 1)[0]

    mixer.music.load(music_filename)
    mixer.music.play(0,0)
    
  def get_frame_rate(self, filepath):
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
    
  def generate_queue(self, directory, n):
    """ Create a random list of n songs selected from the given
    directory with no repeats.

    Returns a list of filpaths (strings) to the songs in the queue.
    
    """
    songs = self.get_list_of_songs(directory)
    for i in xrange(len(songs)):
      songs[i] = directory + '/' + songs[i]
    
    random.shuffle(songs) # Shuffles in-place
    return songs    
    
  def play_next(self):
    """ Stop playing the current song (if any) and play the next song in 
    the queue.
    
    queue is a list of songs (strings)
    position the index of the current song in the queue
    
    """
    mixer.music.stop();
    
    new_position = self.music_queue_position + 1
    if (new_position >= len(self.music_queue)):
      # Don't play anything if we're at the end of the queue
      return
    else:
      song_filename = self.music_queue[new_position]
      mixer.music.load(song_filename)
      mixer.music.play(0,0)
      self.music_queue_position = new_position
    
  def play_prev(self):
    """ Stop playing the current song (if any) and play the previous song in
    the queue.
    queue is a list of songs (strings)
    position the index of the current song in the queue

    """
    mixer.music.stop()

    new_position = self.music_queue_position - 1
    
    if (new_position <= 0):
      # Play the current song if we're at the beginning of the queue
      mixer.music.play(0,0)
      return
    else:
      song_filename = self.music_queue[new_position]
      mixer.music.load(song_filename)
      mixer.music.play(0,0)
      self.music_queue_position = new_position
