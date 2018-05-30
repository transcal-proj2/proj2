import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt

l = 50
dx = 5
dt = int(5)
alpha = 1
minutos = 2
fo = float(alpha*dt)/(dx**2)

initial = [20.0]* int(l/dx)
initial[0] = 0.0
initial[-1] = 0.0

timeline = []
timeline.append(initial)

print("Initial", initial)
print("Timeline", timeline)

print(fo)

for t in range(1, int(60/dt) * minutos):
  print("T: ", t)
  prev = timeline[t - 1]
  print(prev)

#   # print("t", t, "prev" , prev)
#   # print(prev)
  new = prev[:]
  plt.plot(new)
  plt.show()
  for i in range (1, len(prev) - 1):
    new[i] = fo * (prev[i + 1] + prev[i - 1]) + ((1 - (2 * fo)) * prev[i])

  timeline.append(new)

print('\n')
pprint(timeline)
