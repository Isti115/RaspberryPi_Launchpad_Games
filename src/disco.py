import random
from pygame import time

def start(LP):
  while True:
    LP.LedCtrlXY(random.randint(0,8), random.randint(0,8), random.randint(0,3), random.randint(0,3))
    
    time.wait(5)
    
    but = LP.ButtonStateXY()
    if but != [] and but[0:2] == [8, 8]:
      break