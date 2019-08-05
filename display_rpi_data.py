import paramiko
import os
import ast

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# https://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(hostname='alexandergreerrpi.local', username='pi', password='pass')
print("CONNECTED")

sftp = ssh.open_sftp()
print("TRANSFER OPENED")

sftp.get('/home/pi/myscript/loggedfile.txt', '/Users/alexandergreer/Desktop/test.txt')
print("file copied")

sftp.close()
ssh.close()

counter = 0
logged_data = []

with open("/Users/alexandergreer/Desktop/test.txt", "r") as file:
    if counter == 0:
        # https://www.geeksforgeeks.org/python-convert-a-string-representation-of-list-into-list/
        firstline = file.readline()
        firstline = ast.literal_eval(firstline)

        timestamp_zero = firstline[0]
        firstline[0] -= timestamp_zero

        logged_data.append(firstline)

    for line in file:
        if not line:
            break
        this_line = ast.literal_eval(line)
        this_line[0] -= timestamp_zero
        logged_data.append(this_line)

    counter += 1

print(logged_data)

# Create figure for plotting
fig = plt.figure()
ax1 = fig.add_subplot(311)
plt.title('IoT Piano Teacher - Orientation Data')
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
ax1.set(ylabel='R')
ax2.set(ylabel='Theta')
ax3.set(xlabel ='Time (ms)', ylabel='Phi')

# plot parameters
x_len = len(logged_data)
r_range = [0, 1500]
theta_range = [-180, 180]
phi_range = [-180, 180]
xs = list(range(0, x_len))
ys1 = []
ys2 = []
ys3 = []

print(x_len)

for value in logged_data:
    print(value)
    ys1.append(value[1])
    ys2.append(value[2])
    ys3.append(value[3])


ax1.set_ylim(r_range)
line1, = ax1.plot(xs, ys1, 'bo')
ax1.plot(xs, smooth(ys1, 9), 'r-', lw=2)

ax2.set_ylim(theta_range)
line2, = ax2.plot(xs, ys2, 'bo')
ax2.plot(xs, smooth(ys2, 9), 'r-', lw=2)

ax3.set_ylim(phi_range)
line3, = ax3.plot(xs, ys3, 'bo')
ax3.plot(xs, smooth(ys3, 9), 'r-', lw=2)

plt.show()
