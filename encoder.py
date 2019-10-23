import time
import RPi.GPIO as GPIO


class MotorEncoder:
    ENC_IN_OUT = (3, 5)
    ENC_UP_DOWN = (33, 31)

    def __init__(self, pin_a, pin_b):
        self.A_PIN = pin_a
        self.B_PIN = pin_b
        self._seq = 0
        self.pos = 0
        self._clockwise = True

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.A_PIN, GPIO.BOTH, callback=self.on_move)
        GPIO.add_event_detect(self.B_PIN, GPIO.BOTH, callback=self.on_move)

    def on_move(self, _pin):
        delta = self.get_delta()
        if delta == 1:
            self.pos += 1
            self._clockwise = True

        if delta == 2:
            if self._clockwise:
                self.pos += 2
            else:
                self.pos -= 2
        if delta == 3:
            self._clockwise = False
            self.pos -= 1

    def get_delta(self):
        seq = (GPIO.input(self.A_PIN) ^ GPIO.input(self.B_PIN)) | GPIO.input(self.B_PIN) << 1
        delta = (seq - self._seq) % 4
        self._seq = seq
        return delta

    def set_to_origin(self):
        self.pos = 0

    def get_pos(self):
        return self.pos


if __name__ == "__main__":
    mc = MotorEncoder(*MotorEncoder.ENC_IN_OUT)
    mc2 = MotorEncoder(*MotorEncoder.ENC_UP_DOWN)
    while True:
        print('inout %d, updown %d' % (mc.get_pos(), mc2.get_pos()))
        time.sleep(0.1)
