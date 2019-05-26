#import the GPIO and time package
import RPi.GPIO as GPIO
import time
from encoder import MotorEncoder
from controller import MotorController


class LimitSwitch:
    IN_OUT = 12
    UP_DOWN = 26
    
    def __init__ (self, pin, actuator):
        self.actuator = actuator
        self.on = False
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(pin, GPIO.RISING, bouncetime=1000, callback=self.callback_f)
        
    def callback_f(self, channel):
        self.on = not self.on
        if self.on:
            if channel == self.IN_OUT:
                self.actuator.mc.relay(['in-out-stop'])
                self.actuator.encode_ls.set_to_origin()
                print('limit in out')
                
            if channel == self.UP_DOWN:
                self.actuator.mc.relay(['up-down-stop'])
                self.actuator.encode_gaa.set_to_origin()
                print('limit up down')
        
class Actuator:
    def __init__ (self):
        self.mc = MotorController()
        self.encode_in_out = MotorEncoder(*MotorEncoder.ENC_IN_OUT)
        self.encode_up_down = MotorEncoder(*MotorEncoder.ENC_UP_DOWN)
        self.stop_flag = False
        self.x_moving = False
        self.y_moving = False
        
    def initialise_encoders(self):
        # Run the encoders in/down. Check the positions. If they haven't moved zero the encoders
        self.mc.move_dx(False)
        self.mc.move_dy(False)
        prior_x = self.encode_in_out.get_pos()
        prior_y = self.encode_up_down.get_pos()
        x_set = False
        y_set = False
        
        while not self.stop_flag:
            time.sleep(0.5)
            current_x = self.encode_in_out.get_pos()
            current_y = self.encode_up_down.get_pos()
            print('x %d, y %d' % (current_x, current_y))
            if current_x == prior_x and not x_set:
                self.encode_in_out.set_to_origin()
                print('x origin set')
                x_set = True
                self.mc.stop(True, False)
                
            if current_y == prior_y and not y_set:
                self.encode_up_down.set_to_origin()
                print('y origin set')
                y_set = True
                self.mc.stop(False, True)
            
            if x_set and y_set:
                break
            
            prior_x = current_x
            prior_y = current_y
    
    def go_up_end(self, reverse=False):
        if self.stop_flag: return
        self.mc.move_dy(not reverse)
        prior_y = self.encode_up_down.get_pos()
        print('Going fully up' if not reverse else 'going fully down')
        
        while not self.stop_flag:
            time.sleep(0.5)
            current_y = self.encode_up_down.get_pos()
            if current_y == prior_y:
                print('y end')
                if reverse:
                    self.encode_up_down.set_to_origin()
                break
            
            prior_y = current_y
        print('y %d' % current_y)
        self.mc.stop(False, True)
    
    def go_out_end(self, reverse=False):
        if self.stop_flag: return
        self.mc.move_dx(not reverse)
        prior_x = self.encode_in_out.get_pos()
        print('Going fully out' if not reverse else 'going fully in')
        
        while not self.stop_flag:
            time.sleep(0.5)
            current_x = self.encode_in_out.get_pos()
            if current_x == prior_x:
                print('x end')
                if reverse:
                    self.encode_in_out.set_to_origin()
                break
            
            prior_x = current_x
        print('x %d' % current_x)
        self.mc.stop(True, False)
        
    def stop (self):
        self.stop_flag = True
        self.mc.stop()
        
    def go (self):
        self.stop_flag = False
        
    def get_position(self):
        return self.encode_in_out.get_pos(), self.encode_up_down.get_pos()
        
    def move_time (self, t, commands):
        self.mc.relay(commands)
        time.sleep(t)
            
    def set_target(self, new_x, new_y):
        toly = 15
        tolx = 1000
                
        first = True       
        while not self.stop_flag:
            x, y = self.encode_in_out.get_pos(), self.encode_up_down.get_pos()
            dx = new_x - x
            dy = new_y - y
            
            if first:
                first = False
                if dx > 0:
                    self.x_moving = True
                    self.mc.move_dx()
                elif dx < 0:
                    self.mc.move_dx(False)
                    self.x_moving = True
                    
                if dy > 0:
                    self.mc.move_dy()
                    self.y_moving = True
                elif dy < 0:
                    self.mc.move_dy(False)
                    self.y_moving = True
            
            #print('y:', y, 'x:', x, 'newx', new_x, 'newy', new_y, 'dx', dx, 'dy', dy)
                
            if abs(dx) < tolx and self.x_moving:
                self.mc.stop(True, False)
                self.x_moving = False
            if abs(dy) < toly and self.y_moving:
                self.mc.stop(False, True)
                self.y_moving = False
                
            print('x %d, y %d' % (x, y))
            if (not self.x_moving and not self.y_moving) or self.stop_flag:
                break
            
            time.sleep(0.05)
            
        self.mc.stop()
        self.x_moving = False
        self.y_moving = False
        
if __name__ =='__main__':
    a = Actuator()
    a.initialise_encoders()

GPIO.cleanup()
