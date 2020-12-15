import cv2
import os
import numpy as np
import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import scipy.spatial as spatial

data_path = "C:/VDData/cv5_6_marchingcubes/"
num_particles = 64000
dist = 0.018

class Particle:
    def __init__(self, id, posx, posy, posz, velx, vely, velz, rho, press, rad):
        self.id = id

        self.posx = posx
        self.posy = posy
        self.posz = posz

        self.velx = velx
        self.vely = vely
        self.velz = velz
        
        self.rho = rho
        self.press = press
        self.rad = rad

class Triangle:
    def __init__(self, id, posx, posy, posz):
        self.id = id
        self.posx = posx
        self.posy = posy
        self.posz = posz

### Load binary data
def LoadBinaryData():
    particles = []
    d = 0
    for filename in os.listdir(data_path):
        if(".bin" in filename and d < 5):
            i = 0
            x = 0
            sphArray = np.fromfile(data_path + filename, dtype=np.float16)
            for x in range(0, len(sphArray), 9):
                particles.append(Particle(i, sphArray[x], sphArray[x+1], sphArray[x+2], sphArray[x+3],
                                sphArray[x+4], sphArray[x+5], sphArray[x+6], sphArray[x+7], sphArray[x+8],))
                i = i + 1
        d = d + 1
    return particles

### Get k-NN neighbors closest
def GetNeighbors(particles):
    samplePoints = []
    for particle in particles:
        samplePoints.append([particle.posx, particle.posy, particle.posz])
    point_tree = spatial.cKDTree(samplePoints)
    print(point_tree.query_ball_point([0.225, 0.225, 0.225], dist))

def Vizualize():
    # Load binary data
    particles = LoadBinaryData()
    for frame in range(5): # timestep -> 500 
        # Init neighbors
        GetNeighbors(particles)
###
Vizualize()
