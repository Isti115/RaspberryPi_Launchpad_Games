import launchpad

import test

def main():

  LP = launchpad.Launchpad()  # creates a Launchpad instance (first Launchpad found)
  LP.Open()                   # start it
  
  while 1:
    # LP.LedCtrlRaw( random.randint(0,127), random.randint(0,3), random.randint(0,3) )
    
    # some extra time to give the button events a chance to come through...
    time.wait( 5 )
    
    but = LP.ButtonStateRaw()
    if but != []:
      print( but )
      if but[0] == 120:
        break
        
  
  test.start()
  
  LP.Reset() # turn all LEDs off
  LP.Close() # close the Launchpad
  
  
if __name__ == '__main__':
  main()

