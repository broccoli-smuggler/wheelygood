#import the GPIO and time package
import RPi.GPIO as GPIO
import time
from encoder import MotorEncoder
from controller import MotorController

mc = MotorController()
encoder1 = MotorEncoder(*MotorEncoder.ENC_UP_DOWN)

time.sleep(0.5)
mc.move_dx(go_out=False)
#mc.move_dy(go_up=True)
time.sleep(2)
mc.stop()
'''
time.sleep(1.5)
mc.move_dx(go_out=False)
time.sleep(1.5)
mc.stop()
time.sleep(0.5)
mc.move_dy(go_up=True)
time.sleep(1.5)
mc.move_dy(go_up=False)
time.sleep(1.5)
mc.stop(False, True)'''

    
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
        
        #self.in_out_limit = LimitSwitch(LimitSwitch.IN_OUT, self)
        #self.up_down_limit = LimitSwitch(LimitSwitch.UP_DOWN, self)
        self.stop_flag = False
        self.moving = False
    
    def stop (self):
        self.stop_flag = True
        self.mc.stop()
        
    def get_position(self):
        return self.encode_in_out.get_pos(), self.encode_up_down.get_pos()
        
    def move_time (self, t, commands):
        self.mc.relay(commands)
        time.sleep(t)
    
    def move_xy(self, dx, dy):
        toly = 40
        tolx = 500
        x, y = self.encode_in_out.get_pos(), self.encode_up_down.get_pos()
        print('y:', y, 'x:', x)
        
        if dx > 0:
            self.mc.move_dx()
        elif dx < 0:
            self.mc.move_dx(False)
            
        if dy > 0:
            self.mc.move_dy()
        elif dy < 0:
            self.mc.move_dy(False)
        
        new_x = x + dx
        new_y = y + dy
                
        first = True                       
        self.moving = True 
        while True:
            time.sleep(0.4)
            y, x = self.encode_in_out.get_pos(), self.encode_up_down.get_pos()
            diff_x = new_x - x
            diff_y = new_y - y
            
            #if diff_x < 0 and x < tolx:
            #    diff_x = 0
            #if diff_y < 0 and y < toly:
            #    diff_y = 0
                
            print('y:', y, 'x:', x, 'newx', new_x, 'newy', new_y, 'dfx', diff_x, 'dfy', diff_y)
                
            if abs(diff_x) < tolx:
                self.mc.stop(True, False)
            if abs(diff_y) < toly:
                self.mc.stop(False, True)
                
            if abs(diff_x) < tolx and abs(diff_y) < toly or self.stop_flag:
                break
            
        self.mc.stop()
        self.moving = False
        self.stop_flag = False
            
    def set_target(self, x, y):
        toly = 10
        tolx = 10
                
        new_x = x
        new_y = y
                
        first = True                       
        self.moving = True 
        while not self.stop_flag:
            time.sleep(0.01)
            x, y = self.encode_in_out.get_pos(), self.encode_up_down.get_pos()
            dx = new_x - x
            dy = new_y - y
            
            if first:
                first = False
                if dx > 0:
                    self.mc.move_dx()
                elif dx < 0:
                    self.mc.move_dx(False)
                    
                if dy > 0:
                    self.mc.move_dy()
                elif dy < 0:
                    self.mc.move_dy(False)
                
            print('y:', y, 'x:', x, 'newx', new_x, 'newy', new_y, 'dx', dx, 'dy', dy)
                
            if abs(dx) < tolx:
                self.mc.stop(True, False)
            if abs(dy) < toly:
                self.mc.stop(False, True)
                
            if abs(dx) < tolx and abs(dy) < toly or self.stop_flag:
                break
            
        self.mc.stop()
        self.moving = False
        self.stop_flag = False

GPIO.cleanup()