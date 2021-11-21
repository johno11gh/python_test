#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#物体を加速度を与えながら投げ上げる
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.80665 #重力加速度
v0 = 60 #初速度
a = 0 #加速度
interval = 10
t = np.arange(0, 4.60, interval/1000) #時間 0~4.60秒まで,interval/1000ごと
theta = np.pi/2 #投げ上げ角度
y0 = [0, v0*np.sin(theta) ] #[y, x]要素とする y初期条件 [距離, 速度]
x0 = [0, v0*np.cos(theta)] #x初期条件
def equation1(y,  t,  g):
    ret1 = [ ((v0+a*t)*np.sin(theta) -g*t), a*np.sin(theta)-g]
    return ret1
def equation2(x, t, a):
    ret2 = [ ((v0 + a*t)*np.cos(theta)), a*np.cos(theta)]
    return ret2
y = odeint(equation1, y0, t, args=(g,))
x = odeint(equation2, x0, t, args=(a,))
print('y方向')
print(y)
print('x方向')
print(x)

plt.plot(t, y[:, 0], 'y', label='y')
plt.plot(t, y[:, 1], 'g', label='Vy')
plt.plot(t, x[:, 0], 'c', label='x')
plt.plot(t, x[:, 1], 'm', label='Vx')
plt.legend(loc='best')
plt.xlabel('t')
plt.title('v0={}m/s, a={}m/s^2, theta={}°'.format(v0, a, theta*180/np.pi))
plt.grid()
plt.show()
fig, ax =  plt.subplots()
obj, = ax.plot([], [], 'o')
ax.set_xlim(0, max(x.T[0] ) * 1.5) #左端,右端
#ax.set_ylim(-10, 30)
ax.set_ylim(min(y.T[0]) * 1.5, max(y.T[0]) * 1.5)
ax.set_title('v0={}, a={}, theta={}°'.format(v0, a, theta*180/np.pi))
def update_anim(frame_num):
    obj.set_data(x.T[0][frame_num], y.T[0][frame_num])
    return obj,
anim = FuncAnimation(fig, update_anim, frames = np.arange(0, len(t)), interval = interval, blit = True, repeat = True)
plt.show()
