import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import math
from flask import Flask

class Instant():
  def __init__(self, instant_np_array, n_id):
    self.n = n_id
    self.array = instant_np_array

class Calc():
  def __init__(self, minutos, alpha, l=1, dx=0.05, dy=0.05, dt=1, ci=[0, 0, 0, 0]):
    self.n = 0
    self.l = l
    self.dx = dx
    self.dy = dy
    self.dt = dt 
    self.alpha = alpha
    self.minutos = minutos
    self.fo = float(self.alpha*self.dt)/(self.dx**2)
    self.rows = int(self.l/self.dx)
    self.columns = int(self.l/self.dy)
    self.initial = np.zeros((self.rows, self.columns))
    self.timeline = []
    self.ci = ci # self.ci = [120, 50, 0, 75]

    # FILLS CONTOURS
    for i in range(self.rows):
      for j in range(self.columns):
          self.initial[0][j] = ci[0]
          self.initial[i][-1] = ci[1]
          self.initial[-1][j] = ci[2]
          self.initial[i][0] = ci[3]

    self.timeline.append(Instant(self.initial, self.n))
    self.n += 1

  def calculate(self):
    "Fills self.timeline with calculated values"

    for t in range(1, int(60/self.dt) * self.minutos + 1):
      prev = np.copy(self.timeline[t - 1].array)
      new = np.copy(prev)

      for i in range(1, self.rows - 1):
        for j in range(1, self.columns - 1):
          new[i][j] = (self.fo * (prev[i][j+1] + prev[i][j-1] + prev[i-1][j] + prev[i+1][j])
                      + (1 - (4*self.fo)) * prev[i][j])

      self.timeline.append(Instant(new, self.n))
      self.n += 1
    
  def show(self):
    plt.switch_backend('Qt5Agg')
    self.fig = plt.figure(figsize=(8, 6))
    self.ax = self.fig.add_subplot(111)
    self.fig.subplots_adjust(left=0.25, bottom=0.25)
    min0 = 0
    max0 = len(self.timeline) - 1
    self.im1 = self.ax.imshow(self.timeline[-1].array, cmap='jet', interpolation='nearest')
    self.fig.colorbar(self.im1)
    axmin = self.fig.add_axes([0.25, 0.1, 0.65, 0.03])
    sl = Slider(axmin, 'Time', valmin=min0, valmax=max0, valinit=max0, valfmt="%ds")
    sl.on_changed(self.update)
    plt.show()

  def update(self, val):
      # print(chr(27) + "[2J")
      i = math.floor(val)
      # print(timeline[i])
      self.im1.set_data(self.timeline[i].array)
      self.fig.canvas.draw()



# padding
# self.initial = np.pad(self.initial, (1, 1, 1,), mode='constant', constant_values=(200, 200))
# print(np.shape(self.initial))

# self.initial = np.array([[np.random.randint(0, 100)] * int(self.l/self.dx)] * int(self.l/self.dx))

# self.initial[0] = 0.0
# self.initial[-1] = 0.0

# print("Initial", self.initial)
# print("Timeline", timeline)

# print(self.fo)

# for t in range(1, int(60/dt) * minutos):
#   print("T: ", t)
#   prev = timeline[t - 1]
#   print(prev)

# #   # print("t", t, "prev" , prev)
# #   # print(prev)
#   new = prev[:]
#   # plt.plot(new)
#   # plt.show()
#   for i in range(1, len(prev) - 1):
#     new[i] = self.fo * (prev[i + 1] + prev[i - 1]) + ((1 - (2 * self.fo)) * prev[i])

#   timeline.append(new)



