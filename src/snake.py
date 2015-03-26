from pygame import time
import random

def countdown(LP):
  LP.LedCtrlString("3")
  time.wait(1000)
  LP.LedCtrlString("2")
  time.wait(1000)
  LP.LedCtrlString("1")
  time.wait(1000)

def init_snake(LP, snake):
  countdown(LP)
  snake["head"] = [5, 5]
  snake["body"] = [[4, 5], [3, 5]]
  snake["dir"] = 1
  
  snake["food"] = [random.randint(0, 7), random.randint(1, 8)]

dirMatrix

def update(snake, dirChange):
  snake["dir"] = (snake["dir"] + dirChange) % 4
  snake["head"] = [snake["head"][0] + dirMatrix[snake["dir"]][0]
  
  last = body.pop
  LP.LedCtrlXY(snake["body"][0][0], snake["body"][0][0])
  
  

def start(LP):
  snake = {}
  
  init_snake(LP, snake)
  
  LP.LedCtrlXY(8, 8, 3, 0)
  
  exit = 0
  
  while 1:  
    time.wait(250)
    
    but = LP.ButtonStateXY()
    while but != [] and not but[2]:
      but = LP.ButtonStateXY()
    
    if but != [] and but[2]:
      print(but)
      if but[0:2] == [8, 8]:
        update(snake, -1)
      elif but[0:2] == [0, 0]:
        update(snake, -1)
      elif but[0:2] == [1, 0]:
        update(snake, +1)
      else:
        update(snake, 0)
