# import the GPIO and time package
import RPi.GPIO as GPIO
import time


class MotorController:
    _pins = [40, 38, 36, 32]

    def __init__(self):
        # (pin, on/off)
        self.commands_map = {'ls-down': [(1, True), (0, False)],
                             'ls-up': [(0, True), (1, False)],
                             'gaa-out': [(2, True), (3, False)],
                             'gaa-in': [(3, True), (2, False)],
                             'ls-stop': [(0, False), (1, False)],
                             'gaa-stop': [(3, False), (2, False)],
                             'stop': [(0, False), (1, False), (2, False), (3, False)]}

        GPIO.setmode(GPIO.BOARD)

        for pin in self._pins:
            GPIO.setup(pin, GPIO.OUT)

        self.relay(['stop'])

    def relay(self, commands):
        for command in commands:
            print('motor: ' + command)
            for (pin_index, is_on) in self.commands_map[command]:
                GPIO.output(self._pins[pin_index], not is_on)


class MotorEncoder:
    ENC_LS = (23, 29)
    ENC_GAA = (33, 31)

    def __init__(self, pin_a, pin_b):
        self.A_PIN = pin_a
        self.B_PIN = pin_b
        self._seq = 0
        self.pos = 0
        self._clockwise = True

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.A_PIN, GPIO.IN)
        GPIO.setup(self.B_PIN, GPIO.IN)

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
        print(self.pos)

    def get_delta(self):
        seq = (GPIO.input(self.A_PIN) ^ GPIO.input(self.B_PIN)) | GPIO.input(self.B_PIN) << 1
        delta = (seq - self._seq) % 4
        self._seq = seq
        return delta

    def set_to_origin(self):
        self.pos = 0

    def get_pos(self):
        return self.pos


class LimitSwitch:
    def __init__(self, pin, callback_f):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        PIO.add_event_detect(pin, GPIO.BOTH, bouncetime=300, callback=callback_f)


class Actuator:
    def __init__(self):
        self.mc = MotorController()
        self.encode_ls = MotorEncoder(*MotorEncoder.ENC_LS)
        self.encode_gaa = MotorEncoder(*MotorEncoder.ENC_GAA)

    def stop(self):
        self.mc.relay(['stop'])

    def reset_to_origin(self):
        self.mc.relay(['ls-down', 'gaa-in'])
        time.sleep(4)
        self.encode_ls.set_to_origin()
        self.encode_ls.set_to_origin()

    def move_time(self, t, commands):
        self.mc.relay(commands)
        time.sleep(t)

    def move_xy(self, dx, dy):
        y, x = self.encode_ls.get_pos(), self.encode_gaa.get_pos()

        new_x = x + dx
        new_y = y + dy

        while True:
            pass

        if diff_x > 0:
            self.mc.relay(['gaa-out'])
        elif diff_x < 0:
            self.mc.relay(['gaa-in'])

        if diff_y > 0:
            self.mc.relay(['ls-up'])
        elif diff_y < 0:
            self.mc.relay(['ls-down'])

        while (me.get_pos()[0] != new_x and me.get_pos()[1] != new_y):
            continue

        self.mc.stop()

    def move_to_xy(self, x, y):
        pass


# GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# PIO.add_event_detect(18, GPIO.BOTH, bouncetime=300)

## ALEX change this from ls-up to ls-down to move the arm up/down.
## Press the play button at the top to run the code
## Pressing the button stops the program
# a.mc.relay(['ls-up'])

# GPIO.wait_for_edge(18, GPIO.RISING)

# print('stopped')
# a.stop()

##a.reset_to_origin()
##
##a.move_time(2, ['ls-up'])
##a.move_time(2, ['ls-down'])
##a.move_time(1, ['gaa-out'])
##a.move_time(1, ['gaa-in'])
##a.reset_to_origin()

GPIO.cleanup()
