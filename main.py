#!/usr/bin/env
# -*- coding: utf-8 -*-
import math
import geo
import serial
import micropyGPS
import threading
import time
import RTIMU

direction = 0

latitude = 0
longitude = 0

# 9DOF setting
SETTING_FILE = "RTIMULib"
s = RTIMU.Settings(SETTING_FILE)
imu = RTIMU.RTIMU(s)
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()

def run9dof():
    print "initialized"
    global direction
    while True:
        if imu.IMURead():
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
            direction = math.defrees(fusionPose[2])
            print direction






# GPS setting
gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。

# for GPU updating function
def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s = serial.Serial('/dev/serial0', 9600, timeout=10)
    s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)


# start threads
dofthread = threading.Thread(target=run9dof, args=())
dofthread.demon = True
dofthread.start()

gpsthread = threading.Thread(target=rungps, args=()) # 上の関数を実行するスレッドを生成
gpsthread.daemon = True
#gpsthread.start() # スレッドを起動

while True:
    #print('緯度経度: %2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
    print('%3f' % direction)
    time.sleep(10)
