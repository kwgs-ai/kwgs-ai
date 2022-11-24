from time import sleep
import datetime
import requests
import schedule
import pygame.mixer
import random
import math
import time

from gpiozero import AngularServo

JST = datetime.timezone(datetime.timedelta(hours=9), "JST")


# BASE = "http://192.168.100.167/" #バイト先のwifi

BASE = "http://192.168.100.175/"  # バイト先のwifi



global start_time, flag, move_start
start_time = datetime.datetime.now(JST)
flag = False  # 一時間同じ場所かどうか
move_start = None

#
def move():
    # 角度で調整する方
    servo = AngularServo(17, min_angle=-50, max_angle=50)
    for i in range(2):
        servo.angle = -50
        sleep(1)
        servo.angle = -25
        sleep(1)
        servo.angle = 0
        sleep(1)
        servo.angle = 25
        sleep(1)
        servo.angle = 50
        sleep(1)

# 通常時の音声
def voice():
    num = math.floor(random.uniform(1, 3))
    print(num)
    if num == 1:
        pygame.mixer.init(frequency=44100)
        pygame.mixer.music.load("./teru-teru.mp3")
        pygame.mixer.music.play(1)
        time.sleep(3)
        pygame.mixer.music.stop()
    elif num == 2:
        pygame.mixer.init(frequency=44100)
        pygame.mixer.music.load("./kitaku1.mp3")
        pygame.mixer.music.play(1)
        time.sleep(3)
        pygame.mixer.music.stop()
    elif num == 3:
        pygame.mixer.init(frequency=44100)
        pygame.mixer.music.load("./terute-ru.mp3")
        pygame.mixer.music.play(1)
        time.sleep(3)
        pygame.mixer.music.stop()


# BASEのURLはサーバを立てたPCのIPアドレス

def auth_check(check):
    global start_time, flag, move_start
    stop_timeList = [13]
    rest_time = datetime.timedelta(minutes=1)  # 運動を促すまでの時間
    sport_time = datetime.timedelta(minutes=1)  # 帰宅を促すまでの時間
    # 適宜カッコ内は変更してください。
    # 目安としては30分に一度という感じなので、現在はテスト用として30秒としています
    middle_time = datetime.timedelta(milliseconds=30)
    if datetime.datetime.now(JST).hour in stop_timeList:
        print("stop system")
        start_time = datetime.datetime.now(JST)
        return
    if check:
        print("動いてない")
        if move_start is not None:
            move_start = None
        # 普通時の音声を30分に一度出す。現在時刻はend_timeからそのままもらう
        end_time = datetime.datetime.now(JST)
        diff_time = end_time - start_time
        if diff_time > rest_time:
            start_time = datetime.datetime.now(JST)
            print("１時間動いてない")
            # 外出促し
            move()
            pygame.mixer.init(frequency=44100)
            pygame.mixer.music.load("./gaishutu2.mp3")
            pygame.mixer.music.play(1)
            time.sleep(3)
            pygame.mixer.music.stop()
        elif diff_time > middle_time:
            voice()
            move()
            print(1)
            # 今の状態では30秒に一度３種類の音の中からどれかが鳴るようになっているはず。
        print("動いていない時間の合計" + str(end_time - start_time) + "秒です")

    else:
        print("動いた！")
        start_time = datetime.datetime.now(JST)
        if move_start is None:
            move_start = datetime.datetime.now(JST)
        else:
            move_end = datetime.datetime.now(JST)
            diff_time = move_end - move_start
            if diff_time > sport_time:
                flag = True
                print('運動終了')
                # 帰宅を促す音声
                move()
                pygame.mixer.init(frequency=44100)
                pygame.mixer.music.load("./gkitaku2.mp3")
                pygame.mixer.music.play(1)
                time.sleep(3)
                pygame.mixer.music.stop()
            print("運動時間は" + str(diff_time))


def task():
    response = requests.post(BASE + "statuscheck")
    word = response.json()
    print(word)
    status = word["status"]
    check = word["check"]
    auth_check(check)
    if status == "OK":
        print("successful receive")
    else:
        print("nothing")


schedule.every(10).seconds.do(task)

while True:
    if flag:
        continue
    schedule.run_pending()
    sleep(1)
