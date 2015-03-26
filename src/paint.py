from pygame import time

colors = {
"0|0": [3, 1],
"1|0": [2, 1],
"2|0": [3, 2],
"3|0": [3, 3],
"4|0": [2, 2],
"5|0": [1, 1],
"6|0": [1, 2],
"7|0": [2, 3],
"8|1": [1, 3],
"8|2": [1, 0],
"8|3": [2, 0],
"8|4": [3, 0],
"8|5": [0, 1],
"8|6": [0, 2],
"8|7": [0, 3],
"8|8": [0, 0]
}

def init_colors(LP):
  for c in colors:
    pos = c.split("|")
    x, y = int(pos[0]), int(pos[1])
    LP.LedCtrlXY(x, y, colors[c][0], colors[c][1])

def start(LP):
  init_colors(LP)
  currColor = [0, 3]
  
  exit = 0
  fill = 0
  
  while True:
    time.wait(5)
    
    but = LP.ButtonStateXY()
    
    if but != []:
      if [but[0], but[1]] in [[0, 1], [0, 8], [7, 1], [7, 8]]:
        if but[2]:
          exit += 1
        else:
          exit -= 1
    
    if but != []:
      if [but[0], but[1]] in [[3, 4], [4, 4], [3, 5], [4, 5]]:
        if but[2]:
          fill += 1
        else:
          fill -= 1
          
    if exit == 4:
      break
    
    if fill == 4:
      for i in range(8*8):
        LP.LedCtrlXY(i % 8, int(i / 8) + 1, currColor[0], currColor[1])
    
    if but != [] and but[2]:
      if but[0] == 8 or but[1] == 0:
        currColor = colors[str(but[0]) + "|" + str(but[1])]
      else:
        LP.LedCtrlXY(but[0], but[1], currColor[0], currColor[1])
        
