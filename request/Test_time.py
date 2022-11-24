import time

from gpiozero import AngularServo


def move():
    # 角度で調整する方
    servo = AngularServo(17, min_angle=-50, max_angle=50)
    while True:
        servo.angle = -50
        time.sleep(1)
        servo.angle = -25
        time.sleep(1)
        servo.angle = 0
        time.sleep(1)
        servo.angle = 25
        time.sleep(1)
        servo.angle = 50
        time.sleep(1)


if __name__ == '__main__':
    move()