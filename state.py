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
        actuator.move_time(2, ['gaa-out'])

    def next(self):
        return Locate(self)


class Locate(State):
    def run(self, actuator):
        print('locate')

    def next(self):
        return Up(self)


class Up(State):
    def run(self, actuator):
        print('up')

    def next(self):
        return In(self)


class In(State):
    def run(self, actuator):
        print('in')

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

    def next(self):
        return Out(self)


class StateMachine:
    def __init__(self):
        self.actuator = actuator.Actuator()
        self.state = Reset(None)
        self.state_change = False
        
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
                t = threading.Thread(target=self.state.run, args=(self.actuator,))
                t.start()
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

