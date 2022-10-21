from time import sleep
import datetime
import requests
import schedule

JST = datetime.timezone(datetime.timedelta(hours=9), "JST")

BASE = "http://192.168.100.167/"

global start_time, flag, move_start
start_time = datetime.datetime.now(JST)
flag = False  # 一時間同じ場所かどうか
move_start = None


# BASEのURLはサーバを立てたPCのIPアドレス

def auth_check(check):
    global start_time, flag, move_start
    stop_timeList = [13]
    rest_time = datetime.timedelta(minutes=1)  # 運動を促すまでの時間
    sport_time = datetime.timedelta(minutes=1)  # 運動を促すまでの時間
    if datetime.datetime.now(JST).hour in stop_timeList:
        print("stop system")
        start_time = datetime.datetime.now(JST)
        return
    if check:
        print("動いてない")
        if move_start is not None:
            move_start = None
        end_time = datetime.datetime.now(JST)
        diff_time = end_time - start_time
        if diff_time > rest_time:
            start_time = datetime.datetime.now(JST)
            print("１時間動いてない")
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

