from pygame import time
# import random

def countdown(LP):
  for i in range(3):
    LP.LedCtrlChar(str(3 - i), 0, 3, 1)
    time.wait(1000)
  LP.Reset()

def make_brush(color, lowcolor, pos, buttons):
  brush = {}
  
  brush["active"] = False
  brush["defpos"] = pos
  brush["pos"] = pos
  brush["dir"] = 1
  brush["color"] = color
  brush["lowcolor"] = lowcolor
  brush["buttons"] = buttons
  brush["lastbut"] = []
  return brush

dirMatrix = [[0, -1], [1, 0], [0, 1], [-1, 0]]

def update(LP, brush):
  LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], brush["lowcolor"][0], brush["lowcolor"][1])
  
  nextPos = [brush["pos"][0] + dirMatrix[brush["dir"]][0], brush["pos"][1] + dirMatrix[brush["dir"]][1]]
  
  nextPos[0] = 0 if nextPos[0] < 0 else 7 if nextPos[0] > 7 else nextPos[0]
  nextPos[1] = 1 if nextPos[1] < 1 else 8 if nextPos[1] > 8 else nextPos[1]
  
  # if nextPos in brush["body"]:
  #   brush["alive"] = False
  #   return
    
  brush["pos"] = nextPos
  
  LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], brush["color"][0], brush["color"][1])
  
  # if brush["pos"] == brush["food"]:
  #   brush["score"] += 1
  #   while brush["food"] in brush["body"] or brush["food"] == brush["pos"]:
  #     brush["food"] = [random.randint(0, 7), random.randint(1, 8)]
  
  # LP.LedCtrlXY(brush["food"][0], brush["food"][1], 3, 0)

def start(LP):
  brushes = []
  brushes.append(make_brush([0, 3], [0, 1], [0, 1], [[0, 0], [1, 0]]))
  brushes.append(make_brush([1, 3], [1, 1], [7, 1], [[8, 1], [7, 0]]))
  brushes.append(make_brush([3, 0], [1, 0], [7, 8], [[8, 8], [8, 7]]))
  
  go = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 2, 2, 2, 2, 0],
    [1, 0, 0, 0, 2, 0, 0, 2, 0],
    [1, 0, 1, 1, 2, 0, 0, 2, 0],
    [1, 0, 0, 1, 2, 2, 2, 2, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ]
  
  goColors = [[0, 0], [0, 2], [2, 0]]
  
  for y in range(9):
    for x in range(9):
      LP.LedCtrlXY(x, y, goColors[go[y][x]][0], goColors[go[y][x]][1])
  
  for brush in brushes:
    LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], brush["lowcolor"][0], brush["lowcolor"][1])
  
  time.wait(500)
  
  while True:
    time.wait(5)
    
    but = LP.ButtonStateXY()
    
    if but != [] and but[2]:
      if go[but[1]][but[0]] > 0:
        break
      for brush in brushes:
        if [but[0], but[1]] == brush["pos"]:
          brush["active"] = not brush["active"]
          currColor = brush["color"] if brush["active"] else brush["lowcolor"]
          LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], currColor[0], currColor[1])
  
  LP.Reset()
  for brush in brushes:
    if brush["active"]:
      LP.LedCtrlXY(brush["buttons"][0][0], brush["buttons"][0][1], brush["color"][0], brush["color"][1])
      LP.LedCtrlXY(brush["buttons"][1][0], brush["buttons"][1][1], brush["color"][0], brush["color"][1])
  
  while True:
    time.wait(400)
    
    exit = 0
    
    but = LP.ButtonStateXY()
    while but != []:
      if but[0:2] == [0, 8]:
        exit += 1
      if but[2]:
        for brush in brushes:
          if but[0:2] in brush["buttons"]:
            brush["lastbut"] = but[0:2]
      but = LP.ButtonStateXY()
    
    if exit == 4:
      break
    
    for brush in brushes:
      if brush["lastbut"] == brush["buttons"][0]:
        brush["dir"] = (brush["dir"] - 1) % 4
        brush["lastbut"] = []
      elif brush["lastbut"] == brush["buttons"][1]:
        brush["dir"] = (brush["dir"] + 1) % 4
        brush["lastbut"] = []
        
    
    for brush in brushes:
      if brush["active"]:
        update(LP, brush)