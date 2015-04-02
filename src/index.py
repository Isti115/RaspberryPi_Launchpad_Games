import launchpad
from pygame import time

import os

import menuanimation

import hello
import disco
import paint
import snake
import snake_old
import brush

programs = {
  "h": {"program": hello,             "color": [0, 1]},
  "d": {"program": disco,             "color": [3, 3]},
  "p": {"program": paint,             "color": [1, 3]},
  "s": {"program": snake,             "color": [0, 3]},
  "o": {"program": snake_old,         "color": [0, 3]},
  "b": {"program": brush,             "color": [3, 1]},
  "m": {"program": menuanimation,     "color": [1, 1]}
}

layout = [
  ["m", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", "p", "p", "p", " ", "h", " "],
  [" ", "d", " ", "p", " ", "p", " ", " ", " "],
  [" ", " ", " ", "p", "p", "p", " ", " ", " "],
  ["s", "s", "s", "p", "b", "b", "b", " ", " "],
  ["o", " ", " ", "p", "b", " ", " ", "b", " "],
  ["s", "s", "s", " ", "b", "b", "b", " ", " "],
  [" ", " ", "s", " ", "b", " ", " ", "b", " "],
  ["s", "s", "s", " ", "b", "b", "b", " ", " "]
]

def drawMenu(LP):
  LP.Reset()
  
  for y in range(9):
    for x in range(9):
      if layout[y][x] != " ":
        LP.LedCtrlXY(x, y, programs[layout[y][x]]["color"][0], programs[layout[y][x]]["color"][1])
    
  LP.LedCtrlXY(4, 0, 3, 0)
  LP.LedCtrlXY(8, 4, 3, 0)
  
  # LP.LedCtrlXY(8, 7, 1, 0)

def main():
  
  LP = launchpad.Launchpad()
  LP.Open()
  
  menuanimation.start(LP)
  
  drawMenu(LP)
  
  exit = {"count": 0, "buttons": [[4, 0], [8, 4]]}
  
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
      elif layout[but[1]][but[0]] != " ":
        LP.Reset()
        programs[layout[but[1]][but[0]]]["program"].start(LP)
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

