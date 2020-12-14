import cv2
import os
import numpy as np
import math

data_path = "/media/pinkie/FA3E8D353E8CEBC7/VDData/cv4_flowfield/"
num_points = 100
size = 256


def DrawPoints(img, points):
    for point in points:
        img = cv2.circle(img, (int(point[0]), int(point[1])), 1, (255,255,255), 0)
    
    return img

def CreateImg():
    blank_image = np.zeros((size, size,1), np.uint8)
    return blank_image

def GeneratePoints():
    points = np.random.randint(size, size=(num_points, 2))
    return points

def Curl(flowMat): #(256, 256, 2)
    calculatedMat = np.zeros((size, size, 1))
    norm = np.zeros((size, size, 1))

    for x in range(size): #row
        for y in range(size): #col
            if(x > 0 and y > 0 and x < size - 1 and y < size - 1):
                dy = flowMat[x][y - 1][1] - flowMat[x][y + 1][1]
                dx = flowMat[x - 1][y][0] - flowMat[x + 1][y][0]   
                calculatedMat[x][y] = dy - dx
            else:
                calculatedMat[x][y] = 0.0

    norm = cv2.normalize(calculatedMat, norm, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    u8 = norm.astype('uint8')
    im_color = cv2.applyColorMap(u8, cv2.COLORMAP_BONE)

    return calculatedMat, im_color

def getVal(flowMat, point):
    x = int(point[0])
    y = int(point[1])

    x0 = cv2.borderInterpolate(x,size, cv2.BORDER_REPLICATE);
    x1 = cv2.borderInterpolate(x+1,size, cv2.BORDER_REPLICATE);
    y0 = cv2.borderInterpolate(y,size, cv2.BORDER_REPLICATE);
    y1 = cv2.borderInterpolate(y+1,size, cv2.BORDER_REPLICATE);

    a = point[0] - x;
    c = point[1] - y;

    x1_interpolate = (flowMat[y0][x0] * (1.0 - a) + flowMat[y0][x1] * a);
    x2_interpolate = (flowMat[y1][x0] * (1.0 - a) + flowMat[y1][x1] * a);
    target = x1_interpolate * (1.0 - c) + x2_interpolate * c;

    return target[0];

def RungeKutta(flowMat, points):
    deltaT = 0.01

    for point in points:
        k1 = getVal(flowMat, point) * deltaT
        k2 = getVal(flowMat, [point[0] + (k1 / 2), point[1] + (k1 / 2)]) * deltaT
        k3 = getVal(flowMat, [point[0] + (k2 / 2), point[1] + (k2 / 2)]) * deltaT
        k4 = getVal(flowMat, [point[0] + k3, point[1] + k3]) * deltaT

        # flowValue = flowMat[point[0]][point[1]][0]
        
        # k1 = flowValue * deltaT
        # k2 = (flowValue + (k1 / 2)) * deltaT
        # k3 = (flowValue + (k2 / 2)) * deltaT
        # k4 = (flowValue + k3) * deltaT

        sumxy = ((k1 + (2*k2) + (2*k3) + k4) / 6)

        point[0] = point[0] + sumxy
        point[1] = point[1] + sumxy

def Vizualize():
    # Create img
    image = CreateImg()

    #Generate points
    points = GeneratePoints()
    i = 0

    for filename in os.listdir(data_path):
        u = cv2.FileStorage(data_path + filename, cv2.FILE_STORAGE_READ)
        mat = u.getNode("flow").mat() # (256, 256, 2) * 1000 iterations

        # TODO - visualisation of vector field matrix
        # Curl
        calculatedMat, im_color_flow = Curl(mat)

        # Runge Kutta
        RungeKutta(calculatedMat, points)

        # Draw points
        im_color_flow = DrawPoints(im_color_flow, points)
        cv2.putText(im_color_flow, str(i), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

        cv2.imshow("image", im_color_flow)
        cv2.waitKey(1)
        i = i + 1


def VizualizeGlyphs():
    # Create img
    image = CreateImg()

    #Generate points
    points = GeneratePoints()
    points = points.astype(np.float64)
    i = 0

    for filename in os.listdir(data_path):
        u = cv2.FileStorage(data_path + filename, cv2.FILE_STORAGE_READ)
        mat = u.getNode("flow").mat() # (256, 256, 2) * 1000 iterations

        delta_t = 10


        # hedgehogs = []
        
        # for x in range(0, size, 20):
        # for y in range(0, size, 20):
        #     #hedgehogs
        #     velocity = v[frameCounter][y][x]
        #     lineX1 = (x, y)
        #     lineX2 = tuple(np.array([x, y]) + (k * velocity))
        #     hedgehogs.append([lineX1, lineX2])

        # hedgehogs = np.array(hedgehogs)


        for idx in range(len(points)):
            addition = mat[int(points[idx][1])][int(points[idx][0])] * delta_t
            points[idx] = points[idx] + addition

            points[idx][0] = size - 1 if points[idx][0] > size - 1 else points[idx][0]
            points[idx][1] = size - 1 if points[idx][1] > size - 1 else points[idx][1]
            points[idx][0] = 0 if points[idx][0] < 0 else points[idx][0]
            points[idx][1] = 0 if points[idx][1] < 0 else points[idx][1]

        calculatedMat, im_color_flow = Curl(mat)

        # Draw points
        im_color_flow = DrawPoints(im_color_flow, points)
        cv2.putText(im_color_flow, str(i), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

        cv2.imshow("image", im_color_flow)
        cv2.waitKey(1)
        i = i + 1




VizualizeGlyphs()


