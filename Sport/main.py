from threading import Thread
from pynput.keyboard import Key, Listener 
from djitellopy import Tello
import cv2

class RCController:
    def __init__(self):
        self.isListening = False
        self.forward_back = 0
        self.left_right = 0
        self.up_down = 0
        self.yaw = 0
        self.rc_speed = 20     
    def startListenKeyboard(self):
        self.isListening = True
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
    def stopListenKeyboard(self):
        self.listener.stop()
    def on_press(self, key):
        if self.isListening:
            if 'char' in dir(key):
                if key.char == ('w'): self.forward_back = self.rc_speed
                elif key.char == ('a'): self.left_right = -self.rc_speed
                elif key.char == ('s'): self.forward_back = -self.rc_speed
                elif key.char == ('d'): self.left_right = self.rc_speed
                elif key.char == ('q'): self.yaw = -self.rc_speed
                elif key.char == ('e'): self.yaw = self.rc_speed
                elif key.char == ('r'): self.up_down = self.rc_speed
                elif key.char == ('f'): self.up_down = -self.rc_speed
    def on_release(self, key):
        if self.isListening:
            if key == Key.esc: self.isListening = False #esc
            elif 'char' in dir(key):
                if key.char == ('w') and self.forward_back == self.rc_speed: self.forward_back = 0
                elif key.char == ('a') and self.left_right == -self.rc_speed: self.left_right = 0
                elif key.char == ('s') and self.forward_back == -self.rc_speed: self.forward_back = 0
                elif key.char == ('d') and self.left_right == self.rc_speed: self.left_right = 0
                elif key.char == ('q') and self.yaw == -self.rc_speed: self.yaw = 0
                elif key.char == ('e') and self.yaw == self.rc_speed: self.yaw = 0
                elif key.char == ('r') and self.up_down == self.rc_speed: self.up_down = 0
                elif key.char == ('f') and self.up_down == -self.rc_speed: self.up_down = 0

class Program:
    def __init__(self, tello, rc):
        self.tello = tello
        self.rc = rc
        self.isRunning = False
        self.commands = """Commands:
                            quit 
                            forward x (20 <= x <= 100) 
                            back x (20 <= x <= 100) 
                            left x (20 <= x <= 100)
                            right x (20 <= x <= 100) 
                            up x (20 <= x <= 100) 
                            down x (20 <= x <= 100) 
                            speed x (10 <= x <= 100)
                            turn left x (1 <= x <= 360)
                            turn right x (1 <= x <= 360)
                            rc"""

    def run(self):
        self.isRunning = True
        print("Connecting to Tello")
        self.tello.connect()
        print("Starting display thread")
        displayThread = Thread(target=self.updateImg, args={})
        displayThread.start()     
        print(self.commands)

        try:
            self.mainLoop()
        except: 
            print("Exception in main loop")
        
        print("Stopping")
        self.isRunning = False
        self.tello.land()
        self.tello.streamoff()
        self.tello.end()
        print("Stopped")

    def mainLoop(self):
        while True:
            cmd = input().split(" ")
            if cmd[0] == "quit": 
                print("Quitting") 
                break;
            elif cmd[0] == "takeoff":
                if not self.tello.is_flying:
                    self.tello.takeoff()
                else: 
                    print("Tello is already flying")
            elif cmd[0] == "land":
                if self.tello.is_flying:
                    self.tello.land()
                else: 
                    print("Tello is not flying")
            elif cmd[0] in ["forward", "back", "left", "right", "up", "down"]:
                if len(cmd) == 2 and cmd[1].isdigit() and int(cmd[1]) >= 20 and int(cmd[1]) <= 100:
                    distance = int(cmd[1])
                    print(f"move {cmd[0]} {distance}")
                    if cmd[0] == "forward": self.tello.move_forward(distance)
                    elif cmd[0] == "back": self.tello.move_back(distance)
                    elif cmd[0] == "left": self.tello.move_left(distance)
                    elif cmd[0] == "right": self.tello.move_right(distance)
                    elif cmd[0] == "up": self.tello.move_up(distance)
                    elif cmd[0] == "down": self.tello.move_down(distance)
                else:
                    print(f"Invalid movement value (20 <= x <= 100)")
            elif cmd[0] == "speed":
                if len(cmd) == 2 and cmd[1].isdigit() and int(cmd[1]) >= 10 and int(cmd[1]) <= 100:
                    speed = int(cmd[1])
                    print(f"Set SPEED to {speed}")
                    self.tello.set_speed(speed);
                else:
                    print("invalid speed value (10 <= x <= 10)")
            elif cmd[0] == "turn":
                if len(cmd) == 3 and cmd[1] in ["left","right"] and cmd[2].isdigit() and int(cmd[2]) >= 1 and int(cmd[2]) <= 360:
                    print(f"turning {cmd[1]} {cmd[2]}°")
                    degrees = int(cmd[2])
                    if cmd[1] == "left":
                        self.tello.rotate_counter_clockwise(degrees)
                    else:
                        self.tello.rotate_clockwise(degrees)
                else:
                    print ("Invalid turn command (turn left 360)") 
            elif cmd[0] == "rc":
                if self.tello.is_flying:
                    self.rc.startListenKeyboard()
                    while self.rc.isListening:
                        # print(f"send_rc_control({rc.left_right},{rc.forward_back},{rc.up_down},{rc.yaw})")
                        self.tello.send_rc_control(self.rc.left_right, self.rc.forward_back, self.rc.up_down, self.rc.yaw)
                    self.rc.stopListenKeyboard()
                    print(f"Sending stop")
                    self.tello.send_rc_control(0,0,0,0)
                else:
                    print("To use RC you should take off first")
            else: 
                print("Unknown command")

    def updateImg(self):
        self.tello.streamon()
        frame_read = self.tello.get_frame_read()
        while self.isRunning:
            img = frame_read.frame
            cv2.putText(img, f"Battery: {self.tello.get_battery()}", (0,100), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            cv2.putText(img, f"Temp: {self.tello.get_temperature()}", (0,200), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            cv2.imshow("drone", img)
            if(cv2.waitKey(33) & 0xFF ==27):
                break;
    
def main():
    tello = Tello()
    rc = RCController()
    prg = Program(tello, rc)
    prg.run()

if __name__ == '__main__':
    main()