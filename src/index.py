import launchpad
from pygame import time

import os

import hello
import disco
import paint
import snake
import snake_old

programs = {}

def addProgram(program, color, *coords):
  for c in coords:
    programs[str(c[0]) + "|" + str(c[1])] = {"color": color, "program": program}

def drawMenu(LP):
  LP.Reset()
  
  for p in programs:
    pos = p.split("|")
    x, y = int(pos[0]), int(pos[1])
    LP.LedCtrlXY(x, y, programs[p]["color"][0], programs[p]["color"][1])
    
  LP.LedCtrlXY(3, 0, 3, 0)
  LP.LedCtrlXY(8, 5, 3, 0)
  
  # LP.LedCtrlXY(8, 7, 1, 0)

def main():
  
  LP = launchpad.Launchpad()
  LP.Open()
  
  addProgram(hello, [0, 1], [0, 1])
  addProgram(disco, [3, 3], [3, 2])
  addProgram(paint, [1, 3], [5, 1], [6, 1], [7, 1], [5, 2], [7, 2], [5, 3], [6, 3], [7, 3], [5, 4], [5, 5], [5, 6])
  addProgram(snake, [0, 3], [1, 4], [2, 4], [3, 4],         [1, 6], [2, 6], [3, 6], [3, 7], [1, 8], [2, 8], [3, 8])
  addProgram(snake_old, [0, 3], [1, 5])
  
  drawMenu(LP)
  
  exit = {"count": 0, "buttons": [[3, 0], [8, 5]]}
  
  while True:
    time.wait(5)
    
    but = LP.ButtonStateXY()
    
    if but != []:
      if [but[0], but[1]] in exit["buttons"]:
        if but[2]:
          exit["count"] += 1
        else:
          exit["count"] -= 1
    
    if but != [] and but[2]:
      if but[0:2] == [8, 7]:
        pass
        # break
      elif str(but[0]) + "|" + str(but[1]) in programs:
        LP.Reset()
        programs[str(but[0]) + "|" + str(but[1])]["program"].start(LP)
        drawMenu(LP)
        
        but = LP.ButtonStateXY()
        while but != []:
          but = LP.ButtonStateXY()
    
    if exit["count"] == len(exit["buttons"]):
      LP.LedCtrlString('Bye!', 0, 3, -1, 75)
      os.system("sudo poweroff")
      break
  
  LP.Reset()
  # LP.Close()

if __name__ == '__main__':
  main()

