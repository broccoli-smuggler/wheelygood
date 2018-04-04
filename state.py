import actuator

class State:
    def run(self):
        assert 0, "run not implemented"
        
    def next(self, input):
        assert 0, "next not implemented"
     
class Out(State):
    def run(self):
        print('out')
        
    def next(self, input):
        if input is StateMachine.Out:
            return StateMachine.Out
        
        return StateMachine.locate    
        
class Locate(State):
    def run(self):
        print('out')
        
    def next(self, input):
        return StateMachine.locate
    
class Up(State):
    def run(self):
        print('out')
        
    def next(self, input):
        return StateMachine.locate
    
class In(State):
    def run(self):
        print('out')
        
    def next(self, input):
        return StateMachine.locate      
     
        
class States:
    def __init__(self, actuator):
        self.actuator = actuator
        
          
                
class StateMachine:    
    def __init__(self):
        #self.actuator = actuator.Actuator()
        
        self.state_changes = ['out', 'locate', 'up', 'in']
        
        self.states = {'reset': self.reset,
                       'out': self.out,
                       'locate': self.vision_locator,
                       'up': self.up,
                       'in': self.inside}
        

import struct
print('f')
file = open( "/dev/input/mice", "rb" );

def getMouseEvent():
  buf = file.read(3);
  button = ord( buf[0] );
  bLeft = button & 0x1;
  bMiddle = ( button & 0x4 ) > 0;
  bRight = ( button & 0x2 ) > 0;
  x,y = struct.unpack( "bb", buf[1:] );
  print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) );
  # return stuffs

while( 1 ):
  getMouseEvent();
file.close();

