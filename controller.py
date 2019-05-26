import time
import RPi.GPIO as GPIO

class MotorController:
    _pins = [40, 38, 36, 32]
    _switch_time = 0.5
    
    def __init__(self):
        self.commands_map = {'in' : [(1, True), (0, False)],
                             'out': [(0, True), (1, False)],
                             'down': [(3, True), (2, False)],
                             'up' : [(2, True), (3, False)],
                             'in-out-stop': [(0, False), (1, False)],
                             'up-down-stop': [(3, False), (2, False)],
                             'stop' : [(0, False),(1, False),(2, False),(3,False)]}
        
        GPIO.setmode(GPIO.BOARD)
        
        for pin in self._pins:
            GPIO.setup(pin, GPIO.OUT)
            
        self.stop()
        
    def move_dx(self, go_out=True):
        self.stop(self.moving_dx, False)
        time.sleep(self._switch_time)
        
        self.execute_command('out' if go_out else 'in')
        self.moving_dx = True
        
    def move_dy(self, go_up=True):
        self.stop(False, self.moving_dy)
        time.sleep(self._switch_time)
        
        self.execute_command('up' if go_up else 'down')
        self.moving_dy = True
        
    def stop(self, dx=True, dy=True):
        if dx:
            self.execute_command('in-out-stop')
            self.moving_dx = False
        if dy:
            self.execute_command('up-down-stop')
            self.moving_dy = False
            
    def execute_command(self, command):
        if command in self.commands_map:
            #print('Motor: ' + command)
            for (pin_index, is_on) in self.commands_map[command]:
                GPIO.output(self._pins[pin_index], not is_on)
                
if __name__ == '__main__':
    mc = MotorController()
    time.sleep(0.5)
    mc.move_dx(go_out=False)
    mc.move_dy(go_up=True)
    time.sleep(5)
    mc.stop()
    time.sleep(1.5)
    mc.move_dx(go_out=False)
    time.sleep(1.5)
    mc.stop()
    time.sleep(0.5)
    mc.move_dy(go_up=True)
    time.sleep(1.5)
    mc.move_dy(go_up=False)
    time.sleep(1.5)
    mc.stop(False, True)