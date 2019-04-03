import dbus
import dbus.mainloop.glib
import gobject
import sys
import time
import random
from optparse import OptionParser

global proxSensorsVal
global proxDelta
proxSensorsVal=[0,0,0,0,0]
proxDelta=[101,101]

global direction
direction = "go"

def dbusReply():
  pass

def dbusError(e):
  print 'error %s'
  print str(e)



def Braitenberg():
  #get the values of the sensors
  network.GetVariable("thymio-II", "prox.horizontal",reply_handler=get_variables_reply,error_handler=get_variables_error)
  network.GetVariable("thymio-II", "prox.ground.delta",reply_handler=get_deltavariables_reply,error_handler=get_variables_error)



  #print the proximity sensors value in the terminal
  print "prox" 
  print proxSensorsVal[0],proxSensorsVal[1],proxSensorsVal[2],proxSensorsVal[3],proxSensorsVal[4]
  print "    "
  print "delta" 

  print proxDelta[0],proxDelta[1]
  print "  "
  #send motor value to the robot
  #network.SetVariable("thymio-II", "motor.left.target", [-100])
  #network.SendEventName('SetColor', [32,0,32], reply_handler = dbusReply ,error_handler=dbusError)
  #char = sys.stdin.read(1)
  #if char == 'w':
  #   network.SendEventName('event1', [32,0,32,0,32,0,32,0], reply_handler = dbusReply ,error_handler=dbusError)

  #if char == 'w':

  global BeeClust
  global direction
  global Clear
  
  #sum_prox = proxSensorsVal[0] + proxSensorsVal[1] + proxSensorsVal[2] + proxSensorsVal[3] + proxSensorsVal[4]
  #sum_sideprox = proxSensorsVal[0] + proxSensorsVal[4]

  #Leftturn = proxSensorsVal[0]+proxSensorsVal[1]
  #Rightturn = proxSensorsVal[3]+proxSensorsVal[4]
  #Frontturn = proxSensorsVal[2] #wierd name

  #global boarder
  #boarder = 0.67

  if (proxSensorsVal[3]+proxSensorsVal[4])>= 4500:
    print "Leftturn"
    Clear = False
    #print Leftturn
    direction = "Right"

  if (proxSensorsVal[0]+proxSensorsVal[1]) >= 4500:
    print "Rightturn"
    Clear = False
    #print Rightturn
    direction = "Left"

  if proxSensorsVal[2] >= 1750:
    print "Frontturn"
    Clear = False
    #print Frontturn
    direction = "Front"  
  #Evasive action
  if direction == "Left":
    Clust(BeeClust)
    print "turning right"
    network.SetVariable("thymio-II", "motor.left.target", [300])
    network.SetVariable("thymio-II", "motor.right.target", [-300])
    time.sleep(0.75) 
    network.SetVariable("thymio-II", "motor.left.target", [0])
    network.SetVariable("thymio-II", "motor.right.target", [0])
    direction = "go"

  if direction == "Right":
    Clust(BeeClust)
    print "turning left"
    network.SetVariable("thymio-II", "motor.left.target", [-300])
    network.SetVariable("thymio-II", "motor.right.target", [300])
    time.sleep(0.75) 
    network.SetVariable("thymio-II", "motor.left.target", [0])
    network.SetVariable("thymio-II", "motor.right.target", [0])
    direction = "go"

  if direction == "Front":
    Clust(BeeClust)
    print "Fronting"
    network.SetVariable("thymio-II", "motor.left.target", [-300])
    network.SetVariable("thymio-II", "motor.right.target", [300])
    time.sleep(0.75) 
    network.SetVariable("thymio-II", "motor.left.target", [0])
    network.SetVariable("thymio-II", "motor.right.target", [0])
    direction = "go"

  if direction == "Boarder":
    network.SetVariable("thymio-II", "motor.left.target", [-300])
    network.SetVariable("thymio-II", "motor.right.target", [300])
    time.sleep(0.75) 
    network.SetVariable("thymio-II", "motor.left.target", [0])
    network.SetVariable("thymio-II", "motor.right.target", [0])
    direction = "go"

  if direction == "go":
    print "going"
    network.SetVariable("thymio-II", "motor.left.target", [150])
    network.SetVariable("thymio-II", "motor.right.target", [150])
 
  if proxDelta[0] <= 75 or proxDelta[1] <= 75: 
    direction = "Boarder"
    print "Boarder"

  if (proxDelta[0] <= 130 and proxDelta[0] >= 75) or (proxDelta[1] <= 130 and proxDelta[1] >= 75):
    BeeClust = 2
    #direction = "go"
    print "Blackground"
    return BeeClust

  if (proxDelta[0] <= 300 and proxDelta[0] >= 130) or (proxDelta[1] <= 300 and proxDelta[1] >= 130):
    BeeClust = 4
    #direction = "go"
    print "GrayGround"
    return BeeClust

  if (proxDelta[0] <= 500 and proxDelta[0] >= 300) or (proxDelta[1] <= 500 and proxDelta[1] >= 300):
    BeeClust = 8
    #direction = "go"
    print "White"
    return BeeClust

  if (proxDelta[0] <= 700 and proxDelta[0] >= 500) or (proxDelta[1] <= 700 and proxDelta[1] >= 500):
    BeeClust = 16
    #direction = "go"
    print "Target"
    return BeeClust


    
  return True

#  return True
 
def get_variables_reply(r):
  global proxSensorsVal
  proxSensorsVal=r

def get_deltavariables_reply(r):
  global proxDelta
  proxDelta=r

def get_variables_error(e):
  print 'error:'
  print str(e)
  loop.quit()

def Clust(BeeClust):
  print "Clustin'"
  network.SetVariable("thymio-II", "motor.left.target", [0])
  network.SetVariable("thymio-II", "motor.right.target", [0])
  time.sleep(BeeClust)

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
 
  (options, args) = parser.parse_args()
 
  dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
 
  if options.system:
    bus = dbus.SystemBus()
  else:
    bus = dbus.SessionBus()
 
  #Create Aseba network 
  network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
 
  #print in the terminal the name of each Aseba NOde
  print network.GetNodesList()  
  #GObject loop
  #print 'starting loop'
  loop = gobject.MainLoop()
  #call the callback of Braitenberg algorithm
  handle = gobject.timeout_add (50, Braitenberg) #every 0.05 sec || 20 times per second
  loop.run()