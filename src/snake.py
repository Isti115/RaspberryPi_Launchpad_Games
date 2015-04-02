from pygame import time
import random

def countdown(LP):
  for i in range(3):
    LP.LedCtrlChar(str(3 - i), 0, 3, 1)
    time.wait(1000)
  LP.Reset()

def init_snake(LP, snake):
  countdown(LP)
  snake["alive"] = True
  
  snake["score"] = 0
  
  snake["head"] = [3, 3]
  snake["body"] = [[2, 3], [1, 3]]
  snake["dir"] = 1
  
  snake["food"] = [random.randint(0, 7), random.randint(1, 8)]
  while snake["food"] in snake["body"] or snake["food"] == snake["head"]:
    snake["food"] = [random.randint(0, 7), random.randint(1, 8)]

dirMatrix = [[0, -1], [1, 0], [0, 1], [-1, 0]]

def update(LP, snake):
  nextHead = [(snake["head"][0] + dirMatrix[snake["dir"]][0]) % 8,
              (snake["head"][1] + dirMatrix[snake["dir"]][1] - 1) % 8 + 1]
  
  if nextHead in snake["body"]:
    snake["alive"] = False
    return
    
  snake["body"].insert(0, snake["head"])
  
  snake["head"] = nextHead
  
  LP.LedCtrlXY(snake["head"][0], snake["head"][1], 1, 3)
  for b in snake["body"]:
    LP.LedCtrlXY(b[0], b[1], 0, 3)
  
  if snake["head"] == snake["food"]:
    snake["score"] += 1
    while snake["food"] in snake["body"] or snake["food"] == snake["head"]:
      snake["food"] = [random.randint(0, 7), random.randint(1, 8)]
  else:
    last = snake["body"].pop()
    LP.LedCtrlXY(last[0], last[1], 0, 0)
  
  LP.LedCtrlXY(snake["food"][0], snake["food"][1], 3, 0)

def start(LP):
  snake = {}
  
  init_snake(LP, snake)
  LP.LedCtrlXY(snake["head"][0], snake["head"][1], 1, 3)
  for b in snake["body"]:
    LP.LedCtrlXY(b[0], b[1], 0, 3)
  
  LP.LedCtrlXY(0, 0, 0, 1)
  LP.LedCtrlXY(1, 0, 0, 1)
  LP.LedCtrlXY(8, 8, 1, 0)
  
  time.wait(500)
  
  while snake["alive"]:
    time.wait(250)
    
    but = LP.ButtonStateXY()
    while but != [] and not but[2]:
      but = LP.ButtonStateXY()
    
    if but != [] and but[2]:
      if but[0:2] == [8, 8]:
        break
      elif but[0:2] == [0, 0]:
        snake["dir"] = (snake["dir"] - 1) % 4
      elif but[0:2] == [1, 0]:
        snake["dir"] = (snake["dir"] + 1) % 4
    
    update(LP, snake)
  
  if not snake["alive"]:
    for i in range(3):
      LP.LedCtrlXY(snake["head"][0], snake["head"][1], 0, 0)
      for b in snake["body"]:
        LP.LedCtrlXY(b[0], b[1], 0, 0)
      time.wait(500)
      LP.LedCtrlXY(snake["head"][0], snake["head"][1], 1, 3)
      for b in snake["body"]:
        LP.LedCtrlXY(b[0], b[1], 0, 3)
      time.wait(500)
    LP.LedCtrlString("Score: ", 0, 3, -1, 30)
    LP.LedCtrlString(str(snake["score"]), 0, 3, -1, 100)
