import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
import sys,tty,termios
camera = PiCamera()
image_width = 640
image_height = 480
camera.resolution = (image_width, image_height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(image_width, image_height))
center_image_x = image_width / 2
center_image_y = image_height / 2
minimum_area = 4
maximum_area = 100

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pins = [18,27,13,21]
GPIO.setup(pins,GPIO.OUT)
p = GPIO.PWM(13,100)
p2 = GPIO.PWM(18,100)
p.start(0)
p2.start(0)
def fast():
    p.ChangeDutyCycle(90)
    p2.ChangeDutyCycle(85)
    # GPIO.output(18,True)
    GPIO.output(27,False)
    # GPIO.output(13,True)
    GPIO.output(21,False)
    #time.sleep(5)
    #GPIO.cleanup()
    #exit()
def slow():
    p2.ChangeDutyCycle(60);p.ChangeDutyCycle(70)
    # GPIO.output(18,True)
    GPIO.output(27,False)
    # GPIO.output(13,True)
    GPIO.output(21,False)
def stop():
    p2.ChangeDutyCycle(0);p.ChangeDutyCycle(0)
    # GPIO.output(18,False)
    GPIO.output(27,False)
    # GPIO.output(13,False)
    GPIO.output(21,False)
HUE_VAL = 170 # for red
HUE_VAL2 = 45 # for green
go = True
wait_for_green = False
stop_detected= False
prev = []
lower_color = np.array([HUE_VAL-10, 100, 100])
upper_color = np.array([HUE_VAL+10, 255, 255])
lower_color2 = np.array([HUE_VAL2-10, 100, 100])
upper_color2 = np.array([HUE_VAL2+10, 255, 255])
stop_sign_detected = False
#this for is treated like a while
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
    color_mask = cv2.inRange(hsv, lower_color, upper_color)
    color_mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
    
    countours, hierarchy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    countours2, hierarchy2 = cv2.findContours(color_mask2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    object_area = 0
    object_x = 0
    object_y = 0
    for contour in countours:
        x, y, width, height = cv2.boundingRect(contour)
        found_area = width * height
        center_x = x + (width / 2)
        center_y = y + (height / 2)
        if object_area < found_area:
            object_area = found_area
            object_x = center_x
            object_y = center_y
    if object_area > 0:
        object_location = [object_area, object_x, object_y]
    else:
        object_location = None
    object_area2 = 0
    object_x2 = 0
    object_y2 = 0
    for contour2 in countours2:
        x, y, width, height = cv2.boundingRect(contour2)
        found_area = width * height
        center_x = x + (width / 2)
        center_y = y + (height / 2)
        if object_area2 < found_area:
            object_area2 = found_area
            object_x2 = center_x
            object_y2 = center_y
            
    if object_area > 0:
        object_location = [object_area, object_x, object_y]
    else:
        object_location = None
    if object_area2 > 0:
        object_location2 = [object_area, object_x, object_y]
    else:
        object_location2 = None
    img_gray = cv2.cvtColor(frame.array, cv2.COLOR_BGR2GRAY)
    stop_data = cv2.CascadeClassifier('stop_data.xml')
    found = stop_data.detectMultiScale(img_gray, 
                                   minSize =(20, 20))
    amount_found = len(found)
    print(amount_found)
    if amount_found != 0 and go == False:
        stop_detected = True
        slow()
        # for (x, y, width, height) in found:
        #         cv2.rectangle(frame.array, (x, y), 
        #                   (x + height, y + width), 
        #                   (0, 255, 0), 5)
    if amount_found == 0:
       stop()
    if object_location:
        if stop_detected == False:
            slow()
            print('RED')
            go = False
            print('RED')
#and this for green
    if object_location2:
        stop_detected = False
        go = True
        fast()
        print('GREEN')
    else:
        if go==True:
            fast()
    rawCapture.truncate(0)
