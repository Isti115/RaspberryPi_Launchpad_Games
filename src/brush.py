from pygame import time
# import random

def countdown(LP):
  for i in range(3):
    LP.LedCtrlChar(str(3 - i), 0, 3, 1)
    time.wait(1000)
  LP.Reset()

def make_brush(color, midcolor, lowcolor, pos, buttons, dir):
  brush = {}
  
  brush["active"] = False
  
  brush["hurt"] = 0
  
  brush["defpos"] = pos
  brush["prevpos"] = pos
  brush["pos"] = pos
  
  brush["dir"] = dir
  
  brush["color"] = color
  brush["midcolor"] = midcolor
  brush["lowcolor"] = lowcolor
  
  brush["buttons"] = buttons
  brush["lastbut"] = []
  
  brush["count"] = 0
  
  return brush

dirMatrix = [[0, -1], [1, 0], [0, 1], [-1, 0]]

def update(LP, brush):
  if brush["hurt"] > 0:
    brush["hurt"] -= 1
  
  if brush["hurt"] % 2 == 1:
    return
  
  LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], brush["lowcolor"][0], brush["lowcolor"][1])
  
  nextPos = [brush["pos"][0] + dirMatrix[brush["dir"]][0], brush["pos"][1] + dirMatrix[brush["dir"]][1]]
  
  nextPos[0] = 0 if nextPos[0] < 0 else 7 if nextPos[0] > 7 else nextPos[0]
  nextPos[1] = 1 if nextPos[1] < 1 else 8 if nextPos[1] > 8 else nextPos[1]
  
  brush["prevpos"] = brush["pos"]
  brush["pos"] = nextPos
  
  if brush["hurt"] > 0:
    LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], brush["midcolor"][0], brush["midcolor"][1])
  else:
    LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], brush["color"][0], brush["color"][1])

def start(LP):
  allbrushes = []
  allbrushes.append(make_brush([0, 3], [0, 2], [0, 1], [0, 1], [[0, 0], [1, 0]], 2))
  allbrushes.append(make_brush([1, 3], [1, 2], [1, 1], [7, 1], [[8, 1], [7, 0]], 3))
  allbrushes.append(make_brush([3, 0], [2, 0], [1, 0], [7, 8], [[8, 8], [8, 7]], 0))
  
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
  
  for brush in allbrushes:
    LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], brush["lowcolor"][0], brush["lowcolor"][1])
  
  time.wait(500)
  
  gameTime = 3
  
  for i in range(5):
    if i < gameTime:
      LP.LedCtrlXY(i, 8, 1, 3)
    else:
      LP.LedCtrlXY(i, 8, 1, 1)
  
  while True:
    time.wait(5)
    
    but = LP.ButtonStateXY()
    
    if but != [] and but[2]:
      if go[but[1]][but[0]] > 0:
        break
      for brush in allbrushes:
        if [but[0], but[1]] == brush["pos"]:
          brush["active"] = not brush["active"]
          currColor = brush["color"] if brush["active"] else brush["lowcolor"]
          LP.LedCtrlXY(brush["pos"][0], brush["pos"][1], currColor[0], currColor[1])
      if but[1] == 8 and but[0] in range(5):
        gameTime = but[0] + 1
        for i in range(5):
          if i < gameTime:
            LP.LedCtrlXY(i, 8, 1, 3)
          else:
            LP.LedCtrlXY(i, 8, 1, 1)
  
  brushes = []
  for brush in allbrushes:
    if brush["active"]:
      brushes.append(brush)
  
  LP.Reset()
  for brush in brushes:
    LP.LedCtrlXY(brush["buttons"][0][0], brush["buttons"][0][1], brush["color"][0], brush["color"][1])
    LP.LedCtrlXY(brush["buttons"][1][0], brush["buttons"][1][1], brush["color"][0], brush["color"][1])
  
  field = [[-1 for i in range(8)] for i in range(8)]
  
  p = 0
  
  for brush in brushes:
    field[brush["pos"][1] - 1][brush["pos"][0]] = p
    p += 1
  
  gameTime = gameTime * 15
  passedTime = 0
  
  while True:
    time.wait(400)
    passedTime += 400
    
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
    
    bn = 5
    
    for i in range(bn):
      LP.LedCtrlXY(2 + i, 0, min(((passedTime / 1000) - ((gameTime / bn) * i)) / (gameTime / bn / 3), 3), 0)
    
    if exit == 4 or passedTime > gameTime * 1000:
      break
    
    for brush in brushes:
      if brush["lastbut"] == brush["buttons"][0]:
        brush["dir"] = (brush["dir"] - 1) % 4
        brush["lastbut"] = []
      elif brush["lastbut"] == brush["buttons"][1]:
        brush["dir"] = (brush["dir"] + 1) % 4
        brush["lastbut"] = []
    
    p = 0
    
    for brush in brushes:
      update(LP, brush)
      
      for k in range(len(brushes)):
        for l in range(k + 1, len(brushes)):
          if brushes[k]["pos"] == brushes[l]["pos"] or (brushes[k]["pos"] == brushes[l]["prevpos"] and brushes[k]["prevpos"] == brushes[l]["pos"]):
            LP.LedCtrlXY(brushes[k]["pos"][0], brushes[k]["pos"][1], 0, 0)
            LP.LedCtrlXY(brushes[l]["pos"][0], brushes[l]["pos"][1], 0, 0)
            
            brushes[k]["pos"] = brushes[k]["defpos"]
            brushes[l]["pos"] = brushes[l]["defpos"]
            
            brushes[k]["hurt"] = 8
            brushes[l]["hurt"] = 8
      
      field[brush["pos"][1] - 1][brush["pos"][0]] = p
      p += 1
  
  timebuttons = [[2 + i, 0] for i in range(5)]
  
  for x in range(3):
    for b in timebuttons:
      LP.LedCtrlXY(b[0], b[1], 0, 0)
    time.wait(500)
    for b in timebuttons:
      LP.LedCtrlXY(b[0], b[1], 3, 0)
    time.wait(500)
  
  for y in field:
    for x in y:
      if x != -1:
        brushes[x]["count"] += 1
  
  places = range(len(brushes))
  
  done = False
  
  while not done:
    done = True
    for i in range(len(places) - 1):
      if brushes[places[i]]["count"] < brushes[places[i + 1]]["count"]:
        places[i], places[i + 1] = places[i + 1], places[i]
        done = False
  
  for p in reversed(range(len(places))):
    LP.LedCtrlXY(8, 3 + p, brushes[places[p]]["lowcolor"][0], brushes[places[p]]["lowcolor"][1])
    time.wait(200)
    LP.LedCtrlXY(8, 3 + p, brushes[places[p]]["midcolor"][0], brushes[places[p]]["midcolor"][1])
    time.wait(200)
    LP.LedCtrlXY(8, 3 + p, brushes[places[p]]["color"][0], brushes[places[p]]["color"][1])
    time.wait(200)
  
  while True:
    time.wait(5)
    
    but = LP.ButtonStateXY()
    
    if but != [] and but[2]:
      if but[0:2] == [0, 8]:
        break
      elif but[0:2] in [[8, 3 + i] for i in range(len(places))]:
        LP.LedCtrlString(str(brushes[places[but[1] - 3]]["count"]), brushes[places[but[1] - 3]]["color"][0], brushes[places[but[1] - 3]]["color"][1], -1, 75)
        for i in range(8 * 8):
          if field[int(i / 8)][i % 8] != -1:
            LP.LedCtrlXY(i % 8, int(i / 8) + 1, brushes[field[int(i / 8)][i % 8]]["lowcolor"][0], brushes[field[int(i / 8)][i % 8]]["lowcolor"][1])
            
            but = LP.ButtonStateXY()
            while but != []:
              but = LP.ButtonStateXY()
