from numpy.core import _ufunc_reconstruct
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.spatial as spatial
import copy

NUM_POINTS = 125
SIZE = 500
CENTER = SIZE / 2
VARIATION = 100
RAD = 30

### Point class
class Point:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

### Gaussian function to calculate Z
def Gaussian(x, y):
    dev = (2 * VARIATION * VARIATION)
    xx = math.exp(-math.pow(x - CENTER, 2) / dev)
    yy = math.exp(-math.pow(y - CENTER, 2) / dev)
    return xx * yy * 255
    

### Function to generate numbers on canvas
def GeneratePoints():
    points = []
    for i in range(NUM_POINTS):
        x = -1
        y = -1
        z = -1
        while (x < 0 or x > SIZE - 1 or y < 0 or y > SIZE - 1):
            x = np.random.normal(CENTER, VARIATION)
            y = np.random.normal(CENTER, VARIATION)
            z = Gaussian(x, y)

        #print(str(x) + " " + str(y) + " " + str(z))
        points.append(Point(i, x, y, z))
    return points

### Function to scatter plot points in 2D
def DrawPoints(points):
    for point in points:
        plt.scatter(point.x, point.y, c=point.z, s=10, cmap="gray")

### Function to find neighbours in radius
def FindNeighbors(mypoint, points):
    samplePoints = []
    for point in points:
        samplePoints.append([point.x, point.y])
    point_tree = spatial.cKDTree(samplePoints)
    return point_tree.query_ball_point([mypoint[0], mypoint[1]], RAD)

### Compute distance between two points
def ComputeDistance(point1, point2):
    return math.sqrt( (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 )

if __name__ == "__main__":
    # Generate points
    points = GeneratePoints()

    # Draw points
    plt.figure(figsize=(SIZE/96, SIZE/96), dpi=96)
    plt.xlim(0, SIZE)
    plt.ylim(0, SIZE)
    #DrawPoints(points)
    #plt.show()
    
    reconstructionMat = np.zeros((SIZE, SIZE, 1))

    print("Reconstructing")
    for row in range(SIZE):
        print(row)
        for col in range(SIZE):
            indices = FindNeighbors([row, col], points)
            if len(indices) > 0:
                indicesCount = len(indices)
                nearestDist = indices[0]

                shepardNum = 0
                shepardDenom = 0


                for indice in indices:
                    distance = ComputeDistance([row, col], [points[indice].x, points[indice].y])
                    if (distance > 0):
                        z = points[indice].z
                        lambd = z / (distance * RAD + distance)
                        lambd = lambd * lambd
                        
                        shepardNum += z * math.exp(-lambd)
                        shepardDenom += math.exp(-lambd)

                reconstructionMat[row][col] = (shepardNum / shepardDenom)

    plt.imshow(reconstructionMat, cmap='magma')
    plt.show()
    # Plt show
    #plt.show()