import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import math
from flask import Flask
import time

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
    self.ci = ci  # self.ci = [120, 50, 0, 75]
    self.max_error = -1
    self.tol = 0.00005
    
    if (self.fo > 0.5):
      raise Exception('Não atingiu convergência !!! Fo > 0.5 ')

    print("nós :", self.rows * self.columns)

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

    # Checks if there is a isolated edge
    if None in self.ci:
      return self.calculateIsolated()
    else:
      print("Normal calculation")

    start = time.time()
    for t in range(1, int(60/self.dt) * self.minutos + 1):
      prev = np.copy(self.timeline[t - 1].array)
      new = np.copy(prev)

      biggest_iteration_error = 0
      for i in range(1, self.rows - 1):
        for j in range(1, self.columns - 1):
          new[i][j] = (self.fo * (prev[i][j+1] + prev[i][j-1] + prev[i-1][j] + prev[i+1][j])
                      + (1 - (4*self.fo)) * prev[i][j])

          if(new[i][j] != 0):
            erro = abs((new[i][j] - prev[i][j]) / new[i][j])
          else:
            erro = abs((new[i][j] - prev[i][j]))

          # print("error: ", erro)
          if (erro > self.max_error and t > 1):
            self.max_error = erro        

          if (erro > biggest_iteration_error):
            biggest_iteration_error = erro

      self.timeline.append(Instant(new, self.n))
      self.n += 1

      # print("max_error: ", self.max_error)
      if(biggest_iteration_error < self.tol):
        print("Passou da tolerancia")
        break

    end = time.time()
    deltaT = end - start
    print("took ", deltaT, "ms")

  def isOnEdge(self, i, j):
    if i == 0:
      return 0
    elif j == 0:
      return 3
    elif i == self.rows - 1:
      return 2
    elif j == self.columns - 1:
      return 1
    else:  
      return -1

  def isOnCorner(self, i, j):
    if ((i == 0 and j == 0) or (i == 0 and j == self.columns-1)
      or (i == self.rows-1 and j == 0) or (i == self.rows-1 and j == self.columns-1)):
        return True
    return False
      
  def calculateIsolated(self):
    "Fills self.timeline with calculated values"

    self.initial[np.isnan(self.initial)] = 0

    print("Has isolated border")
    for t in range(1, int(60/self.dt) * self.minutos + 1):
      prev = np.copy(self.timeline[t - 1].array)
      new = np.copy(prev)

      biggest_iteration_error = 0
      for i in range(0, self.rows):
        for j in range(0, self.columns):
          edge = self.isOnEdge(i, j)

          # se ta em um canto
          if self.isOnCorner(i, j):
            continue # ignora

          # se ta em uma lateral
          elif edge != -1:
            # e ta isolado
            if self.ci[edge] == None:
              # faz a operação especifica pra cada borda
              if edge == 0:
                new[i][j] = (self.fo * (prev[i][j+1] + prev[i][j-1] + 0 + prev[i+1][j])
                  + (1 - (4*self.fo)) * prev[i][j])
              elif edge == 1:
                new[i][j] = (self.fo * (0 + prev[i][j-1] + prev[i-1][j] + prev[i+1][j])
                  + (1 - (4*self.fo)) * prev[i][j])
              elif edge == 2:
                new[i][j] = (self.fo * (prev[i][j+1] + prev[i][j-1] + prev[i-1][j] + 0)
                  + (1 - (4*self.fo)) * prev[i][j])
              elif edge == 3:
                new[i][j] = (self.fo * (prev[i][j+1] + 0 + prev[i-1][j] + prev[i+1][j])
                  + (1 - (4*self.fo)) * prev[i][j])
            # se ta numa lateral mas nao ta isolado 
            else:
              continue
          
          else:
            new[i][j] = (self.fo * (prev[i][j+1] + prev[i][j-1] + prev[i-1][j] + prev[i+1][j])
              + (1 - (4*self.fo)) * prev[i][j])

          if(new[i][j] != 0):
            erro = abs((new[i][j] - prev[i][j]) / new[i][j])
          else:
            erro = abs((new[i][j] - prev[i][j]))

          # print("error: ", erro)
          if (erro > self.max_error and t > 1):
            self.max_error = erro

          if (erro > biggest_iteration_error):
            biggest_iteration_error = erro

      self.timeline.append(Instant(new, self.n))
      self.n += 1

      # print("max_error: ", self.max_error)
      if(biggest_iteration_error < self.tol):
        print("Passou da tolerancia")
        break

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



