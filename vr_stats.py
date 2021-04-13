"""
Script to calculate step height and width over time 
during a gaming session of GaitKeeper. Each Right datapoint has a corresponding 
Left datapoint at that exact time step, so right and left datasets will have the same length.


"""

# IMPORTS
import re 
import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks


# FUNCTIONS
def get_coordinates(line):
	"""
	Uses regular expressions module to find 
	x y and z values in a given line
	"""
	x_pattern = r'X=\S*'
	y_pattern = r'Y=\S*'
	z_pattern = r'Z=\S*'

	x_match = re.search(x_pattern,line)
	x_value = float(x_match.group()[2:])
	y_match = re.search(y_pattern,line)
	y_value = float(y_match.group()[2:])
	z_match = re.search(z_pattern,line)
	z_value = float(z_match.group()[2:])

	return x_value, y_value, z_value

def get_arrays(f):
	"""
	Loops through log file to get a list of 
	tupes in the form (x,y,z) for each foot
	"""
	right = []
	left = []

	for line in f:

		if 'Right:' in line:
		

			right.append(get_coordinates(line))

		elif 'Left:' in line: 
		

			left.append(get_coordinates(line))
		else: 
			pass

	return right, left 

def step_height(right, left):
	"""
	Creates a list of step heights by taking 
	the absolute value of the difference between
	left and right z coordinates.
	"""
	step_height = []
	for i in range(len(right)):

		height = abs(right[i][2] - left[i][2])
		step_height.append(height)

	return step_height

def euclidean_distance(right, left):
	"""
	Creates a list of the euclidean distance between
	each foot over time. 
	"""
	step_width = []
	for i in range(len(right)):

		x_1 = right[i][0]
		x_2 = left[i][0]
		y_1 = right[i][1]
		y_2 = left[i][1]

		width = np.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
		step_width.append(width)

def get_time(vector):
	"""
	Creates a list of incrementing time values based 
	on the length of the input vector
	"""
	time = []
	for i in range(len(vector)):

		if i == 0:

			curr_time = 0
		else:
			curr_time = time[i-1] + 30

		time.append(curr_time)
	return time

def step_width(right, left):

	"""
	Creates a list of step widths by taking the absolute
	value of the difference between y coordinates.
	"""
	step_width = []
	for i in range(len(right)):

		width = abs(right[i][1] - left[i][1])
		step_width.append(width)

	return step_width


# SCRIPT



# search log file to get arrays 
f = open("HelloVR.log")
right, left = get_arrays(f)

# remove outliers
right = right[50:350]
left = left[50:350]

# calculate neccessary vectors
step_height = step_height(right, left)

step_width = step_width(right, left)
euclidean_distance = euclidean_distance(right, left)
time = get_time(right)
print(time)


# get peaks from step height 
height_peaks, _ = find_peaks(step_height, height = [40, 70])

# apply peaks to step_height
new_height = np.array(step_height)
new_time = np.array(time)
average_height = np.mean(new_height[height_peaks])

# apply same peaks to step width
new_width = np.array(step_width)
avg_width = np.mean(new_width[height_peaks])

fig, ax = plt.subplots(2)
fig.tight_layout(h_pad=2)

ax[0].plot(time, step_height)
ax[0].plot(new_time[height_peaks], new_height[height_peaks], 'x')
ax[0].set_title('Step Height')
ax[0].set(xlabel='Time (ms)',ylabel='Distance (cm)')
ax[0].text(7000, 50, 'Avg Peak = {} cm'.format(round(average_height, 2)))


ax[1].plot(time, step_width)
ax[1].plot(new_time[height_peaks], new_width[height_peaks], 'x')
ax[1].set_title('Horizontal Distance between Feet')
ax[1].set(xlabel='Time (ms)', ylabel='Distance (cm)')
ax[1].text(7000, 20, 'Avg = {} cm'.format(round(avg_width, 2)))
plt.show()

