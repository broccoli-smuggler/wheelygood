import time
import RPi.GPIO as GPIO


class LimitSwitch:
    OUT = 12

    def __init__(self, pin):
        self.on = False
        self.pin = pin
        self.callback_f = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=20, callback=self.pin_callback)

    def pin_callback(self, pin):
        time.sleep(0.02)
        self.on = not GPIO.input(pin)
        if self.callback_f:
            self.callback_f(self.on)

    '''
    The callback function is of type func(is_on)
    '''
    def set_callback(self, callback_f):
        self.callback_f = callback_f


if __name__ == "__main__":
    limit_switch = LimitSwitch(LimitSwitch.OUT)

    def on(is_on):
        print('on = ' + str(is_on))

    # limit_switch.set_callback_on_low(off)
    limit_switch.set_callback(on)
    while True: continue
