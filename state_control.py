import threading
import time

import cv2

import actuator
import limit
import vision

max_height = 4850
resting_height = 4100
max_out = 300000
locate_height = 1590


class IStateContext(object):
    current_state = None
    action_chain = []

    def set_state(self, new_state):
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
        state_object.set_state(state_object.stop)


class IntoCar(IState):
    def run(self, state_object):
        print("go into car")
        self.running = True
        # Go into car at current max height
        x, y = state_object.actuator.get_position()
        state_object.actuator.set_target(x, max_height)
        state_object.actuator.go_out_end(reverse=True)

        # Once in, go to resting position
        state_object.actuator.set_target(0, resting_height)
        self.running = False
        print("into car")

    def next(self, state_object):
        if not self.running:
            state_object.set_state(state_object.out)

    def prior(self, state_object):
        if not self.running:
            state_object.set_state(state_object.up)


class IntoCarNoChair(IState):
    def run(self, state_object):
        print("go into car no chair")
        self.running = True
        # go to zero zero
        state_object.actuator.go_out_end(reverse=True)
        self.running = False
        print("into car no chair")

    def next(self, state_object):
        if not self.running:
            state_object.set_state(state_object.out_no_chair)

    def prior(self, state_object):
        if not self.running:
            state_object.set_state(state_object.down)


class OutCar(IState):
    def run(self, state_object):
        print("go out")
        self.running = True
        x, y = state_object.actuator.get_position()
        # Go up before out
        state_object.actuator.set_target(x, max_height)
        state_object.actuator.go_out_end()

        self.running = False
        print("out of car")

    def next(self, state_object):
        if not self.running:
            state_object.set_state(state_object.down)

    def prior(self, state_object):
        if not self.running:
            state_object.set_state(state_object.into_car)


class OutCarNoChair(IState):
    def run(self, state_object):
        print("go out no chair")
        self.running = True
        x, y = state_object.actuator.get_position()
        state_object.actuator.go_out_end()

        self.running = False
        print("out of car")

    def next(self, state_object):
        if not self.running:
            state_object.set_state(state_object.locate)

    def prior(self, state_object):
        if not self.running:
            state_object.set_state(state_object.into_car_no_chair)


class Down(IState):
    def run(self, state_object):
        print("chair down")
        self.running = True
        state_object.actuator.go_out_end()
        x, y = state_object.actuator.get_position()
        # Move to chair height
        state_object.actuator.set_target(x, locate_height)
        self.running = False
        print("down")

    def next(self, state_object):
        if not self.running:
            state_object.set_state(state_object.into_car_no_chair)

    def prior(self, state_object):
        if not self.running:
            state_object.set_state(state_object.out)


class Locate(IState):
    def __init__(self):
        self.vision = vision.VisionLocator()

    def run(self, state_object):
        print("locating chair")
        self.running = True
        state_object.actuator.go_out_end()
        x, y = state_object.actuator.get_position()
        # Move to chair height
        state_object.actuator.set_target(x, locate_height)

        # The first X is fully out, thus we can't go any further than this
        x_limit = x
        print(x)

        dx = None
        tolerence = 800
        while not state_object.actuator.is_stopped():
            time.sleep(0.03)
            x, y = state_object.actuator.get_position()
            dx = self.vision.get_chair_dx(False)
            print(dx)
            if dx is not None:
                if x + dx > x_limit:
                    print('chair too far')
                else:
                    if abs(dx) < tolerence:
                        print('Located!')
                        break
                    state_object.actuator.set_target(x + dx, y)
        self.running = False

    def next(self, state_object):
        if not self.running:
            state_object.set_state(state_object.up)

    def prior(self, state_object):
        if not self.running:
            state_object.set_state(state_object.out_no_chair)


class Up(IState):
    def run(self, state_object):
        print("chair off floor")
        self.running = True
        x, y = state_object.actuator.get_position()
        state_object.actuator.set_target(x, max_height)
        state_object.actuator.go_out_end()
        self.running = False

    def next(self, state_object):
        if not self.running:
            state_object.set_state(state_object.into_car)

    def prior(self, state_object):
        if not self.running:
            state_object.set_state(state_object.locate)


class Stop(IState):
    def run(self, state_object):
        pass

    def action(self, state_object):
        print("stopped")
        state_object.actuator.stop()

    def next(self, state_object):
        state_object.actuator.go()
        print(state_object.before_stop)
        state_object.set_state(state_object.before_stop)

    def prior(self, state_object):
        state_object.actuator.go()
        print(state_object.before_stop)
        state_object.before_stop.prior(state_object)

    def stop(self, state_object):
        pass


class RoboChair(IStateContext):
    def __init__(self):
        self.actuator = actuator.Actuator()
        self.actuator.initialise_encoders()
        self.limit_switch = limit.LimitSwitch(limit.LimitSwitch.OUT)
        self.limit_switch.set_callback(self.limit_callback)

        self.out_limit = False
        self.into_car = IntoCar()
        self.into_car_no_chair = IntoCarNoChair()
        self.out = OutCar()
        self.out_no_chair = OutCarNoChair()
        self.locate = Locate()
        self.down = Down()
        self.up = Up()
        self.stop = Stop()
        self.current_state = self.into_car_no_chair
        self.current_state.action(self)
        self.before_stop = None

    def limit_callback(self, is_on):
        print("out limit hit!" if is_on else "out limit off")
        self.out_limit = is_on
        if is_on:
            self.stop_func()

    def next(self):
        if not self.out_limit:
            self.current_state.next(self)
            self.current_state.action(self)

    def prior(self):
        if not self.out_limit:
            self.current_state.prior(self)
            self.current_state.action(self)

    def stop_func(self):
        if self.current_state != self.stop:
            self.before_stop = self.current_state
            self.current_state.stop(self)
        self.current_state.action(self)


if __name__ == "__main__":
    rob = RoboChair()


def mouse_event(event, x, y, flags, param):
    if event == 6:
        rob.stop_func()
    elif event == 4:
        print("next")
        rob.next()
    elif event == 5:
        print("prior")
        rob.prior()

    cv2.namedWindow("click")
    cv2.waitKey(1)
    cv2.destroyWindow("click")

    cv2.namedWindow("click", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("click", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("click", mouse_event)

    while True:
        cv2.waitKey(10)

    GPIO.cleanup()
