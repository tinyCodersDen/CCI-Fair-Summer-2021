import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
def output(list1):
    for t in list1:
        if t[1] == 'HIGH':
            GPIO.output(t[0],GPIO.HIGH)
        if t[1] == 'LOW':
            GPIO.output(t[0],GPIO.LOW)
pins = [21,16]
GPIO.setup(pins, GPIO.OUT)
GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_UP)
output([[16,'LOW'],[21,'LOW']])
flag = True
while True:
    button_state = GPIO.input(26)
    if button_state == 0:
        if flag==True:
            output([[16,'LOW'],[21,'HIGH']])
            sleep(1)
            flag = False
        elif flag==False:
            output([[16,'HIGH'],[21,'LOW']])
            sleep(1)
            flag = True
