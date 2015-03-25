import random
from pygame import time

def start(LP):
  while 1:
    LP.LedCtrlRaw( random.randint(0,127), random.randint(0,3), random.randint(0,3) )
    
    # some extra time to give the button events a chance to come through...
    time.wait( 5 )
    
    but = LP.ButtonStateRaw()
    if but != []:
      print( but )
      if but[0] == 119:
        break