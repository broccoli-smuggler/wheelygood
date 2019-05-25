import threading
import cv2
import time
import actuator


class IStateContext(object):
    current_state = None
    action_chain = []

    def setState(self, new_state):
        self.current_state = new_state


class IState(object):
    running = False

    def run(self, state_object):
        raise NotImplementedError()

    def action(self, state_object):
        if not self.running:
            t = threading.Thread(target=self.run, args=(state_object,))
            t.start()

    def next(self, state_object):
        raise NotImplementedError()

    def prior(self, state_object):
        raise NotImplementedError()

    def stop(self, state_object):
        state_object.setState(state_object.stop)


class IntoCar(IState):
    def run(self, state_object):
        print("go into car")
        self.running = True
        x, y = state_object.actuator.get_position()
        state_object.actuator.set_target(x, 100)
        self.running = False
        print("into car")

    def next(self, state_object):
        if not self.running:
            state_object.setState(state_object.out)

    def prior(self, state_object):
        if not self.running:
            state_object.setState(state_object.up)


class OutCar(IState):
    def run(self, state_object):
        print("go out")
        self.running = True
        x, y = state_object.actuator.get_position()
        state_object.actuator.set_target(x, y + 200)
        self.running = False
        print("out of car")

    def next(self, state_object):
        if not self.running:
            state_object.setState(state_object.locate)

    def prior(self, state_object):
        if not self.running:
            state_object.setState(state_object.into_car)


class Locate(IState):
    def run(self, state_object):
        print("locating chair (down)")
        self.running = True
        x, y = state_object.actuator.get_position()
        state_object.actuator.set_target(x, y - 100)
        self.running = False

    def next(self, state_object):
        if not self.running:
            state_object.setState(state_object.up)

    def prior(self, state_object):
        if not self.running:
            state_object.setState(state_object.out)


class Up(IState):
    def run(self, state_object):
        print("chair off floor")
        self.running = True
        x, y = state_object.actuator.get_position()
        state_object.actuator.set_target(x, y + 100)
        self.running = False
        

    def next(self, state_object):
        if not self.running:
            state_object.setState(state_object.into_car)

    def prior(self, state_object):
        if not self.running:
            state_object.setState(state_object.locate)


class Stop(IState):
    def run(self, state_object):
        pass

    def action(self, state_object):
        print("stopped")
        state_object.actuator.stop()

    def next(self, state_object):
        state_object.setState(state_object.before_stop)

    def prior(self, state_object):
        state_object.before_stop.prior(state_object)

    def stop(self, state_object):
        pass


class RoboChair(IStateContext):
    def __init__(self):
        self.actuator = actuator.Actuator()
        self.into_car = IntoCar()
        self.out = OutCar()
        self.locate = Locate()
        self.up = Up()
        self.stop = Stop()
        # self.reset_func()
        self.current_state = self.into_car
        self.before_stop = None

    def next(self):
        self.current_state.next(self)
        self.current_state.action(self)

    def prior(self):
        self.current_state.prior(self)
        self.current_state.action(self)

    def stop_func(self):
        if self.current_state != self.stop:
            self.before_stop = self.current_state
        self.current_state.stop(self)
        self.current_state.action(self)


rob = RoboChair()


def mouse_event(event, x, y, flags, param):
    if event == 6:
        rob.stop_func()
    elif event == 4:
        rob.next()
    elif event == 5:
        rob.prior()


if __name__ == "__main__":
    cv2.namedWindow("click")
    cv2.waitKey(1)
    cv2.destroyWindow("click")

    cv2.namedWindow("click")  # , cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("click", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("click", mouse_event)

    while True:
        cv2.waitKey(0)
        time.sleep(0.1)
