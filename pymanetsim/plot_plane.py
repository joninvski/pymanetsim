import pdb
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def plot_plane(plane, all_nodes, name):
    x = [0]*plane.x_size
    y = [0]*plane.y_size

    X = np.meshgrid(x, y)

    #For each node
    for node in all_nodes.values():
        #Get its heat value
        heat = 100 #TODO - This is fake

        #Put that value on the heat map
        x = node.location.x
        y = node.location.y
        X[0][x][y] = heat

    plt.imshow(X[0], interpolation='nearest', origin='lower', \
               extent=[0, plane.x_size, 0, plane.y_size])

    plt.savefig('/tmp/' + str(name))

#    plt.show()
#    plt.savefig('../results/images/plots/' + str(name))
