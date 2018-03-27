import actuator
from enum import Enum

class States(Enum):
    IDLE = 1
    RESET = 0
    OUT = 2
    L0CATE = 3
    LIFT = 4
    IN = 5
    
    def __init__(self):
        self.cur = IDLE
        self.cur_pos = (0,0)
    
    def get_pos(self):        
        switch self.cur:
            case RESET:
                self.cur_pos = (0,0)
                break
            case OUT:
                self.cur_pos = (0.8, 0.2)
                break
            case LIFT:
                self.cur_pos[1] = 0.7
                break
            case IN:
                self.cur_pos = (0, 0.4)
                break
        return cur_pos
                
                
class StateMachine:    
    def __init__(self):
        self.states = States
        
    def goto_state(new_state):
        
        
        