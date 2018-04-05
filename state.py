#import actuator
import threading
import time
import random


class State:
    def __init__(self, prior):
        self.prior_s = prior

    def run(self):
        assert 0, "run not implemented"

    def next(self):
        assert 0, "next not implemented"

    def prior(self):
        if self.prior_s:
            return self.prior_s
        else:
            return self


class Out(State):
    def run(self):
        print('out')

    def next(self):
        return Locate(self)


class Locate(State):
    def run(self):
        print('locate')

    def next(self):
        return Up(self)


class Up(State):
    def run(self):
        print('up')

    def next(self):
        return In(self)


class In(State):
    def run(self):
        print('in')

    def next(self):
        return Out(self)


class Stop(State):
    def run(self):
        print('stop')

    def next(self):
        return Reset(self)


class Reset(State):
    def run(self):
        print('reset')

    def next(self):
        return Out(self)


class StateMachine:
    def __init__(self):
        #self.actuator = actuator.Actuator()
        t = threading.Thread(target=self.mouse_thread)
        #t.start()

        self.state = Reset(None)

        while True:
            self.state.run()
            time.sleep(1)
            if random.getrandbits(1):
                self.state = self.state.prior()
            else:
                self.state = self.state.next()

    def mouse_thread(self):
        while True:
            left, middle, right = self.get_mouse_event()
            if left != 0 or right != 0 or middle != 0:
                print(left, middle, right)

    @staticmethod
    def get_mouse_event():
        with open("/dev/input/mice", "rb") as f:
            buf = f.read(3)
            button = ord(buf[0])
            return button & 0x1, (button & 0x4) > 0, (button & 0x2) > 0

sm = StateMachine()

# def mouse_event(event, x, y, flags, param):
# cv2.namedWindow("click")
# cv2.waitKey(1)
# cv2.destroyWindow("click")
#
# cv2.namedWindow("click")#, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("click", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cv2.setMouseCallback("click", mouse_event)
#
# cv2.waitKey(0)
