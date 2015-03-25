import launchpad
from pygame import time

import os

import testa
import testb

def drawMenu(LP):
  LP.Reset()
  LP.LedCtrlXY(5, 1, 0, 3)
  LP.LedCtrlXY(6, 1, 3, 3)
  LP.LedCtrlXY(8, 8, 3, 0)

def main():
  
  LP = launchpad.Launchpad()  # creates a Launchpad instance (first Launchpad found)
  LP.Open()                   # start it
  
  drawMenu(LP)
  
  while 1:
    # LP.LedCtrlRaw( random.randint(0,127), random.randint(0,3), random.randint(0,3) )
    
    # some extra time to give the button events a chance to come through...
    time.wait( 5 )
    
    but = LP.ButtonStateRaw()
    if but != []:
      print( but )
      if but[0] == 120:
        testa.start(LP)
        drawMenu(LP)
      if but[0] == 5:
        testb.start(LP)
        drawMenu(LP)
      if but[0] == 6:
        os.system("sudo poweroff")
        drawMenu(LP)
  
  LP.Reset() # turn all LEDs off
  LP.Close() # close the Launchpad

if __name__ == '__main__':
  main()

