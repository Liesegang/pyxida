#!/usr/bin/env 
# -*- coding: utf-8 -*-

from math import pi, tan, atan, sin, cos, acos, atan2

def deg2rad(x):
  return x * pi / 180

class Position:
  def __init__(self, lat, lng):
    self.lat = lat # 緯度
    self.lng = lng # 経度

  def latr(self):
    return deg2rad(self.lat)

  def lngr(self):
    return deg2rad(self.lng)

  def distance(self, other):
    eps = 0.00001
    if abs(self.lat - other.lat) < eps and abs(self.lng - other.lng) < eps:
      return 0

    EQUATOR_RADIUS = 6378140 # metor
    POLER_RADIUS = 6356755 # metor

    f = (EQUATOR_RADIUS + POLER_RADIUS) / EQUATOR_RADIUS

    p1 = atan((POLER_RADIUS / EQUATOR_RADIUS) * tan(self.latr()))
    p2 = atan((POLER_RADIUS / EQUATOR_RADIUS) * tan(other.latr()))

    x = acos(sin(p1) * sin(p2) + cos(p1) * cos(p2) * cos(self.lngr() - other.lngr()))
    l = (f / 8) * (sin(x) - x) * ((sin(p1) + sin(p2)) ** 2 / cos(x / 2) ** 2 - (sin(p1) - sin(p2)) ** 2 / sin(x) ** 2)

    return EQUATOR_RADIUS * (x + l)

  def direction(self, other):
    y = cos(other.lngr()) * sin(other.latr() - self.latr())
    x = cos(self.lngr()) * sin(other.lngr()) - sin(self.lngr()) * cos(other.lngr()) * cos(other.latr() - self.latr())

    dirE0 = 180 * atan2(y, x) / pi;

    dirN0 = (dirE0 + 360 + 90) % 360

    return dirN0



