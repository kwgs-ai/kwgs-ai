from http.client import RemoteDisconnected
from app import app
from flask_restful import Api, Resource
import datetime
from pyicloud import PyiCloudService
import time
import random
# import multiprocessing as mp
from http.client import RemoteDisconnected
from requests.exceptions import ConnectionError
from tenacity import retry

JST = datetime.timezone(datetime.timedelta(hours=9), "JST")

api = Api(app)
# 何回もスマホに承認の要求が来る
api2 = PyiCloudService('ai12071994@yahoo.co.jp', '12071207Ai')
# api2 = PyiCloudService('', '')
global status, flag
status = "OK"
flag = False


class StatusCheck(Resource):
    global pre_lat, pre_lon, start_time, flag
    pre_lat = None
    pre_lon = None

    @retry()
    def get_auth(self):
        # リトライ処理確認用
        # if random.random() < 0.5:
        #     raise ConnectionError()
        #     print(11)
        auth = api2.devices[3].location()
        auth: str = str(auth)
        return auth

    def post(self):
        global pre_lat, pre_lon, flag
        try:
            auth = self.get_auth()
        except (ConnectionError, RemoteDisconnected) as e:
            print("Remote Disconnected error!" + str(e))

        eval_auth = eval(auth)
        is0 = auth.find('isOld')
        auth.find('positionType')
        lat = eval_auth['latitude']
        lon = eval_auth['longitude']
        lat = round(lat, 3)
        lon = round(lon, 3)

        if pre_lat is None or pre_lon is None:
            pre_lat = lat
            pre_lon = lon

        # lat += 1  # 外出実験用
        if pre_lat == lat and pre_lon == lon:
            flag = True
        dt_now = datetime.datetime.now(JST)
        date = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
        return {"now": date, "status": status, "check": flag}


api.add_resource(StatusCheck, "/statuscheck")
