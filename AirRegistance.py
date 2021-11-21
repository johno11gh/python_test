#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.80665 #m/s2
v0 = 0 #m/s
interval = 10 #ms　ミリセコンド
t = np.arange(0, 35, interval/1000) #0秒から10秒まで 0.01秒毎
μ = 1.8*10**(-5) #Pa・s
r = 0.05*10**(-3) #雨粒の半径 mm→m変換
k = 6*np.pi*μ*r #抵抗係数
ρ = 1003 #kg/m^3
m = 4/3*np.pi*ρ*r**3 #
#y0 = [0, 0]
ramda = k / m
e = np.exp(-1*k/m*10**-2*t)
v =g/ramda*(1-e)

#def func(e, t, a):
#    dedt = a*e
#    return dedt
#a = -1
#e0 = -1
#e = odeint(func, e0, t, args=(a,))
y = g / ramda * (t + (1/ramda)*e) - g/ramda**2
print(v)
print(y)
plt.plot(t, v, label = 'v')
plt.legend()
plt.show()
