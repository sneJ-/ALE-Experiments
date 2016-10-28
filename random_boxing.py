#!/usr/bin/env python
# random_boxing.py
# Two random agents playing against each other Boxing with different frame skips
# to evaluate which impact frame skip has on the game.
# Author: Jens Roewekamp
#
import sys
import os

#check if ALE_PATH exits and add to path if it exits
if os.environ['ALE_PATH']:
    sys.path.append(os.environ['ALE_PATH'])

from random import randrange
from ale_python_interface import ALEInterface

ale = ALEInterface()

# Get & Set the desired settings
ale.setInt('random_seed', 123)

# Set USE_SDL to true to display the screen. ALE must be compilied
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
USE_SDL = False
if USE_SDL:
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
    ale.setBool('sound', False) # Sound doesn't work on OSX
  elif sys.platform.startswith('linux'):
    ale.setBool('sound', True)
  ale.setBool('display_screen', True)

# Load the Boxing ROM file
ale.loadROM("boxing.bin")

# Get the list of legal actions
legal_actions = ale.getLegalActionSet()
legal_actionsB = ale.getLegalActionSetB()

# Manually handle the replay_action_proability for both players individually
# to be able to emulate real time behaviour by setting individual frame skips
ale.setFloat("repeat_action_probability", 0.0);

result_file = open("result.csv", "w")
result_file.write("# frame_skip_agent_A, frame_skip_agent_B, episode, score_A, score_B, reward\n")

for frame_skip_agent_A in xrange(1,31): # Agent A is allowed to change his action every X frames
  for frame_skip_agent_B in xrange(1,31): # Agent B is allowed to change his action every Y frames
    frame_counter = 0
    frame_counter_reset = frame_skip_agent_A * frame_skip_agent_B
    # Play 300 episodes
    for episode in xrange(300):
      total_reward = score_A = score_B = 0
      ale.setMode(1) # Switch Boxing to two player mode

      while not ale.game_over():
        # Set action for agent A
        if frame_counter % frame_skip_agent_A == 0:
          a = legal_actions[randrange(len(legal_actions))]
        # Set action for agent B
        if frame_counter % frame_skip_agent_B == 0:
          b = legal_actionsB[randrange(len(legal_actionsB))]

        # Reset frame counter to prevent overflow
        frame_counter += 1
        if frame_counter == frame_counter_reset:
          frame_counter = 0

        # Apply actions and get the resulting reward
        reward = ale.actAB(a,b)
        if reward > 0:
          score_A += reward
        if reward < 0:
          score_B += -reward
        total_reward += reward

      result_file.write("%d,%d,%d,%d,%d,%d\n" % (frame_skip_agent_A,frame_skip_agent_B,episode,score_A,score_B,total_reward)) 
      ale.reset_game()
    result_file.flush()
result_file.close()
