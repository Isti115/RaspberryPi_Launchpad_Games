from pygame import time
import random

def countdown(LP):
  for i in range(3):
    LP.LedCtrlChar(str(3 - i), 0, 3, 1)
    time.wait(1000)
  LP.Reset()

def init_snake(LP, snake):
  countdown(LP)
  snake["head"] = [5, 5]
  snake["body"] = [[4, 5], [3, 5]]
  snake["dir"] = 1
  
  snake["food"] = [random.randint(0, 7), random.randint(1, 8)]

dirMatrix = [[0, -1], [1, 0], [0, 1], [-1, 0]]

def update(LP, snake):
  snake["body"].insert(0, snake["head"])
  
  snake["head"] = [snake["head"][0] + dirMatrix[snake["dir"]][0], snake["head"][1] + dirMatrix[snake["dir"]][1]]
  
  LP.LedCtrlXY(snake["head"][0], snake["head"][1], 1, 3)
  for b in snake["body"]:
    LP.LedCtrlXY(b[0], b[1], 0, 3)
  
  if snake["head"] == snake["food"]:
    snake["food"] = [random.randint(0, 7), random.randint(1, 8)]
  else:
    last = snake["body"].pop()
    LP.LedCtrlXY(last[0], last[1], 0, 0)
  
  LP.LedCtrlXY(snake["food"][0], snake["food"][1], 3, 0)

def start(LP):
  snake = {}
  
  init_snake(LP, snake)
  
  LP.LedCtrlXY(0, 0, 0, 1)
  LP.LedCtrlXY(1, 0, 0, 1)
  LP.LedCtrlXY(8, 8, 1, 0)
  
  time.wait(500)
  
  while True:
    time.wait(500)
    
    but = LP.ButtonStateXY()
    while but != [] and not but[2]:
      but = LP.ButtonStateXY()
    
    if but != [] and but[2]:
      if but[0:2] == [8, 8]:
        break
      if but[0:2] == snake["food"]:
        snake["head"] = [3, 3]
      elif but[0:2] == [0, 0]:
        snake["dir"] = (snake["dir"] - 1) % 4
      elif but[0:2] == [1, 0]:
        snake["dir"] = (snake["dir"] + 1) % 4
    
    update(LP, snake)
