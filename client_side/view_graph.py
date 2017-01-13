import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

data = np.genfromtxt('results.csv', delimiter=',', names=['x', 'y'])
events = np.genfromtxt('events.csv', delimiter=',', names=['x', 'y'])

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.plot(data['x'], data['y'], color='r', label='bps')

ax1.set_title("Tor data rate")    
ax1.set_xlabel('time')
ax1.set_ylabel('data rate (in bps)')

leg = ax1.legend()

for event in events:
	plt.plot(event[0], event[1], 'go')

plt.show()
