import actuator
import threading
import time
import random
import cv2


class State:
    def __init__(self, prior):
        self.prior_s = prior

    def run(self, actuator):
        assert 0, "run not implemented"

    def next(self):
        assert 0, "next not implemented"

    def prior(self):
        if self.prior_s:
            return self.prior_s
        else:
            return self
        
    def stop(self):
        return Stop(self)


class Out(State):
    def run(self, actuator):
        print('out')
        actuator.move_to_xy(0, 270)
        actuator.move_to_xy(350000, 270)

    def next(self):
        return Down(self)


class Down(State):
    def run(self, actuator):
        print('down')
        actuator.move_to_xy(350000, -830)

    def next(self):
        return In(self)


class In(State):
    def run(self, actuator):
        print('in')
        actuator.move_to_xy(0, 0)

    def next(self):
        return Out2(self)


class Out2(State):
    def run(self, actuator):
        print('out2')
        actuator.move_to_xy(350000, -1100)

    def next(self):
        return Locate(self)
    
    
class Locate(State):
    def run(self, actuator):
        print('locate')
        actuator.move_to_xy(360000, -1100)
        time.sleep(1)
        actuator.move_to_xy(350000, -1100)

    def next(self):
        return In2(self)


class In2(State):
    def run(self, actuator):
        print('in2')
        actuator.move_to_xy(350000, 270)
        actuator.move_to_xy(0, 270)
        actuator.move_to_xy(0, 0)

    def next(self):
        return Out(self)

class Stop(State):
    def run(self, actuator):
        print('stop')
        actuator.stop()
        
    def next(self):
        return Reset(self)


class Reset(State):
    def run(self, actuator):
        print('reset')
        actuator.move_to_xy(0, 0)
        #actuator.stop()
        #actuator.reset_to_origin()

    def next(self):
        return Out(self)


class StateMachine:
    def __init__(self):
        self.actuator = actuator.Actuator()
        self.state = Stop(None)
        self.state_change = False
        self.cur_t = None
        
        cv2.namedWindow("click")
        cv2.waitKey(1)
        cv2.destroyWindow("click")

        cv2.namedWindow("click")#, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("click", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback("click", self.mouse_event)

    def start(self):
        while True:
            cv2.waitKey(1)
            if self.state_change:
                print()
                self.cur_t = threading.Thread(target=self.state.run, args=(self.actuator,))
                self.cur_t.start()
                self.state_change = False

    def mouse_event(self, event, x, y, flags, param):
        if event == 6:
            self.state_change = True
            self.state = self.state.stop()
        elif event == 4:
            self.state_change = True            
            self.state = self.state.next()
        elif event == 5:
            self.state_change = True            
            self.state = self.state.prior()

sm = StateMachine()
sm.start()

