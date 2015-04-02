from pygame import time

color = [0, 3]

middle = [[4, 3], [4, 4], [3, 4], [3, 3]]

frames = [
  [[4, 2], [4, 1], [4, 0]],
  [[5, 1], [5, 0], [6, 0]],
  [[5, 2], [6, 1], [7, 0]],
  [[6, 2], [7, 2], [7, 1]],
  [[5, 3], [6, 3], [7, 3]],
]

def draw(LP, x, y, color):
  LP.LedCtrlXY(x, y + 1, color[0], color[1])

def rotate(frame, n):
  out = []
  for p in frame:
    op = [p[0], p[1]]
    for i in range(n):
      op[0], op[1] = int(-(op[1] - 3.5) + 3.5), op[0]
    out.append(op)
  return out

def start(LP):
  LP.Reset()
  
  # for p in middle:
    # LP.LedCtrlXY(p[0], p[1], color[0], color[1])
  
  time.wait(75)
  
  for i in range(4):
    for frame in frames:
      rframe = rotate(frame, i)
      draw(LP, middle[i][0], middle[i][1], color)
      for p in rframe:
        draw(LP, p[0], p[1], color)
      time.wait(75)
  
  for i in range(4):
    for frame in frames:
      rframe = rotate(frame, i)
      draw(LP, middle[i][0], middle[i][1], [0, 0])
      for p in rframe:
        draw(LP, p[0], p[1], [0, 0])
      time.wait(75)
