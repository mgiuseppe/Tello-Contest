import cv2
import time
from djitellopy import Tello

def main():
    tello = Tello()
    tello.connect()

    print(f"battery level: {tello.get_battery()}")
    print(f"temp: {tello.get_temperature()}")
    tello.takeoff()
    tello.move_left(50)
    tello.move_right(50)
    tello.rotate_clockwise(360)

    print(f"Waiting for 1 secs")
    time.sleep(1)
    tello.flip_left()

    tello.land()
    tello.end()

if __name__ == "__main__":
    main()