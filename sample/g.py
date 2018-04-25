#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import smbus
import time

address = 0x68
channel = 1
bus     = smbus.SMBus(channel)

# レジスタをリセットする
bus.write_i2c_block_data(address, 0x6B, [0x80])
time.sleep(0.1)     

# PWR_MGMT_1をクリア
bus.write_i2c_block_data(address, 0x6B, [0x00])
time.sleep(0.1)

# 生データを取得する
while True:
    data    = bus.read_i2c_block_data(address, 0x3B ,6)
    rawX    = data[0] << 8 | data[1]    # 上位ビットが先
    rawY    = data[2] << 8 | data[3]    # 上位ビットが先
    rawZ    = data[4] << 8 | data[5]    # 上位ビットが先
    print "%+8.7f" % rawX + "\t",
    print "%+8.7f" % rawY + "\t",
    print "%+8.7f" % rawZ
    time.sleep(0.1)
