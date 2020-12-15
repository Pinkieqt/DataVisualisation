#import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from matplotlib.pyplot import figure


img_size = 253
step = 25 #10
sz = 5
sizeScale = 0.05
cellSize = img_size / step + 1

### Cell class
class Cell:
    def __init__(self, id, p1, p2, p3, p4):
        self.id = id
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.value = 0

### Functions to compute b1, b2, b3, b4 values -  13 slide
def b1 (x, y): return (1.0 - x) * (1.0 - y)
def b2 (x, y): return (x) * (1.0 - y)
def b3 (x, y): return (x) * (y)
def b4 (x, y): return (1.0 - x) * (y)

### Function to compute Tquad - 24 slide
def Tquad(x, y, point1, point2, point3, point4):
    px = point1[0] * b1(x, y) + point2[0] * b2(x, y) + point3[0] * b3(x, y) + point4[0] * b4(x, y) 
    py = point1[1] * b1(x, y) + point2[1] * b2(x, y) + point3[1] * b3(x, y) + point4[1] * b4(x, y) 

    return np.asarray([px, py])

### Function to compute RS vector
def computeRS(p, point1, point2, point3, point4):
    rsVector = [0.5, 0.5] # initial estimates slide 28
    J = np.zeros((2, 2))
    J_inv = np.zeros((2, 2))

    for i in range(3):
        # 27 slide
        J[0][0] = (rsVector[1] - 1) * (point1[0] - point2[0]) + rsVector[1] * (point3[0] - point4[0])
        J[1][0] = (rsVector[1] - 1) * (point1[1] - point2[1]) + rsVector[1] * (point3[1] - point4[1])

        J[0][1] = (rsVector[0] - 1) * (point1[0] - point4[0]) + rsVector[0] * (point3[0] - point2[0])
        J[1][1] = (rsVector[0] - 1) * (point1[1] - point4[1]) + rsVector[0] * (point3[1] - point2[1])

        J_inv = np.linalg.pinv(J)
        T = Tquad(rsVector[0], rsVector[1], point1, point2, point3, point4)

        TminusP = T - np.array([p[0], p[1]])
        tmp = J_inv.dot(TminusP)
        rsVector = (rsVector - tmp)
    return rsVector

### Test function according to slides -> result is good
def testOnParameters():
    p1 = [1, 0]
    p2 = [3, 0.25]
    p3 = [4, 3]
    p4 = [0, 3.5]
    vector = [1.8, 2.7]
    rs = computeRS(vector, p1, p2, p3, p4)
    return rs

### Function to check if point is on canvas and to fix it
def checkBoundaries(point):
    tmp = point
    if (tmp[0] >= img_size): tmp[0] = img_size - 1
    if (tmp[1] >= img_size): tmp[1] = img_size - 1
    if (tmp[0] <= 0): tmp[0] = 0
    if (tmp[1] <= 0): tmp[1] = 0
    return tmp

### Function to plot grid on canvas
def showImg(img, cellPoints):
    plot = plt.imshow(img)
    plot.set_cmap('hot')
    for i in range(len(cellPoints)):
        plt.plot([cellPoints[i].p1[0], cellPoints[i].p2[0], cellPoints[i].p3[0], cellPoints[i].p4[0], cellPoints[i].p1[0]],
         [cellPoints[i].p1[1], cellPoints[i].p2[1], cellPoints[i].p3[1], cellPoints[i].p4[1], cellPoints[i].p1[1]],
          color="black", alpha=0.1)
    #plt.rcParams["figure.figsize"] = (50,10)
    #plt.savefig("./orig.png")
    plt.show()

### Function to plot reconstructed image
def showImgWithout(img):
    plot = plt.imshow(img)
    plot.set_cmap('hot')
    #plt.savefig("./cv2/results/reconstructed.png")
    plt.show()

### Function to get cell id in which the point is
def getCell(cells, point):
    for cell in cells:
        if((point[0] >= cell.p1[0] and point[0] <= cell.p2[0]) and (point[1] >= cell.p4[1] and point[1] <= cell.p1[1])):
            return cell.id
    return -1

### Function to check if point is within cell
def isInsideCell(cell, point):
    p1 = Point(point[0], point[1])
    coords = [(cell.p1[0]-1, cell.p1[1]+1),(cell.p2[0]+1, cell.p2[1]+1),(cell.p3[0]+1, cell.p3[1]-1),(cell.p4[0]-1, cell.p4[1]-1)]
    poly = Polygon(coords)
    return p1.within(poly)

### Vizualize
def Vizualize():
    img = np.zeros((img_size, img_size)) # blank image
    reconstruct = np.zeros((img_size, img_size))
    cellPoints = [] # 36 cellpoints > gridcells -> it has to be 121!!!
    newCellPoints = []

    for row in range(img_size):
        cellRow = []
        for col in range(img_size):
            value = math.cos(col * sizeScale) * math.sin(row * sizeScale)

            img[row][col] = value

            #create grid
            if(row % (step) == 0 and col % (step) == 0):
                onepoint = [row + np.random.randint(-sz, sz), col + np.random.randint(-sz, sz)]
                onepoint = checkBoundaries(onepoint)
                cellRow.append(onepoint)
        if(len(cellRow)>0): newCellPoints.append(cellRow)

    i = 0

    for row in range(len(newCellPoints)-1):
        for col in range(len(newCellPoints[row])-1):
            p1 = [newCellPoints[row][col+1][0], newCellPoints[row][col+1][1]]
            p2 = [newCellPoints[row+1][col+1][0], newCellPoints[row+1][col+1][1]]
            p3 = [newCellPoints[row+1][col][0], newCellPoints[row+1][col][1]]
            p4 = [newCellPoints[row][col][0], newCellPoints[row][col][1]]
            cellPoints.append(Cell(i, p1, p2, p3, p4))

    print("Computin cells value")
    # compute cell values
    for cell in cellPoints:
        rndx = np.random.randint(cell.p1[0], cell.p2[0])
        rndy = np.random.randint(cell.p4[1], cell.p1[1])

        vector = computeRS([rndx, rndy], cell.p1, cell.p2, cell.p3, cell.p4)
        val = Tquad(vector[0], vector[1], cell.p1, cell.p2, cell.p3, cell.p4)
        imgvalue = math.cos(val[0] * sizeScale) * math.sin(val[1] * sizeScale)
        cell.value = imgvalue

        for row in range(cell.p1[0], cell.p2[0]):
            for col in range(cell.p4[1], cell.p1[1]):
                if (isInsideCell(cell, [row, col]) == True):
                    reconstruct[row][col] = imgvalue
    
    print("Reconstructing")
    #Color reconstructed image
    # for row in range(img_size):
    #     for col in range(img_size):
    #         for cell in cellPoints:
    #             if(isInsideCell(cell, [row, col])):
    #                 reconstruct[row, col] = cell.value
    #                 continue
    #     if(row%25 == 0): print(row)


    showImg(img, cellPoints)
    showImgWithout(reconstruct)

#print(testOnParameters())
Vizualize()