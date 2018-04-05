import actuator
import threading


class State:
    def __init__(self):
        pass

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


class StateMachine:
    def __init__(self):
        self.actuator = actuator.Actuator()

        self.state_changes = ['out', 'locate', 'up', 'in']

        self.states = {'reset': self.reset,
                       'out': self.out,
                       'locate': self.vision_locator,
                       'up': self.up,
                       'in': self.inside}

        t = threading.Thread(target=self.mouse_thread)
        t.start()

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
