from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()
print(f"battery level: {tello.get_battery()}")
print(f"temp: {tello.get_temperature()}")

print("Activating stream")
tello.streamon()
frame_read = tello.get_frame_read()

print("Taking off")
tello.takeoff()
while True:
    # In reality you want to display frames in a seperate thread. Otherwise
    #  they will freeze while the drone moves.
    img = frame_read.frame
    cv2.imshow("drone", img)
    key = cv2.waitKey(1) & 0xff
    if key == 27: # ESC
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('e'):
        tello.rotate_clockwise(30)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)    

print("Landing")
tello.land()
tello.streamoff()
tello.end()