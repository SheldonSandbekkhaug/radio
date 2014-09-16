#!/usr/bin/env python

""" Written by Sheldon Sandbekkhaug.
    All rights reserved.

"""

import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_p, K_q, K_s
from pygame import mixer

from MusicPlayer import MusicPlayer

mp = None # Music Player

def main():
  """ Initialize radio and play sounds """
  music_directory = 'music'

  global mp
  mp = MusicPlayer(music_directory) # Must create mp before pygame.init()

  pygame.init()
  display = pygame.display.set_mode((800,600),0,32)
  pygame.display.set_caption("radio.py")

  mp.start_random_queue()

  print("Press S to skip the current song.")
  print("Press P to return to the previous song.")

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
  global mp
  for event in pygame.event.get():
    if (event.type == QUIT or 
        (event.type == KEYDOWN and event.key == K_q)):
      return 'EXIT'
    elif (event.type == KEYDOWN and event.key == K_s):
      # Skip the current song
      mp.play_next()
    elif (event.type == KEYDOWN and event.key == K_p):
      # Go back to the previous song
      mp.play_prev()
    elif (event.type == MusicPlayer.SONG_ENDED):
      # Song ended naturally, play next
      mp.play_next()


if __name__ == "__main__":
    main()
