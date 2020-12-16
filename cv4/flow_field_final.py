import cv2
import os
import numpy as np
import math

data_path = "C:/VDData/cv4_flowfield/"
num_points = 500
size = 256

### Function to draw points on canvas
def DrawPoints(img, points):
    for point in points:
        img = cv2.circle(img, (int(point[0]), int(point[1])), 1, (255,255,255), -1)
    
    return img

### Function to draw glyphs on canvas
def DrawGlyphs(img, glyphs):
    # for glyph in glyphs:
    #     plt.plot([glyph[0][0], glyph[0][1]], [glyph[1][0], glyph[1][1]])
    for glyph in glyphs:
        p = (int(glyph[0][0]), int(glyph[0][1]))
        q = (int(glyph[1][0]), int(glyph[1][1]))
        img = cv2.line(img, p, q, (100,100,100), thickness=1, lineType=8)
    return img

### Function to create blank image of specified size
def CreateImg():
    blank_image = np.zeros((size, size,1), np.uint8)
    return blank_image

### Function to generate random points on canvas
def GeneratePoints():
    points = np.random.randint(size, size=(num_points, 2))
    return points

### Curl function - presentation page 6
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
    im_color = cv2.applyColorMap(u8, cv2.COLORMAP_MAGMA)

    return calculatedMat, im_color

### Function to vizualize flow matrix loaded from file
def vizFlow(flowMat):
    calculatedMat = np.zeros((size, size, 1))
    for x in range(size): #row
        for y in range(size): #col
            calculatedMat[y][x] = np.linalg.norm(flowMat[y][x])

    norm = np.zeros((size, size, 1))
    norm = cv2.normalize(calculatedMat, norm, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    u8 = norm.astype('uint8')
    im_color = cv2.applyColorMap(u8, cv2.COLORMAP_VIRIDIS)

    return im_color

### Function to record frames to video
def CaptureImage(videowriter, frame):
    videowriter.write(frame)

### New Euler method
def VizualizeGlyphs():
    # Create img
    image = CreateImg()
    writer = cv2.VideoWriter("cv4/output2.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30,(size,size))

    # Generate points
    points = GeneratePoints()
    points = points.astype(np.float64)
    i = 0

    # Loop over files
    for filename in os.listdir(data_path):
        u = cv2.FileStorage(data_path + filename, cv2.FILE_STORAGE_READ)
        mat = u.getNode("flow").mat() # (256, 256, 2) * 1000 iterations

        delta_t = 1
        
        # Calculate glyphs positions
        glyphs = []
        for x in range(0, size, 10):
            for y in range(0, size, 10):
                #hedgehogs
                velocity = mat[y][x]
                glyphs.append([(x, y), tuple(np.array([x, y]) + (delta_t * velocity))])



        for point in range(len(points)):
            velocityAddition = mat[int(points[point][1])][int(points[point][0])] * delta_t
            points[point] = points[point] + velocityAddition
            points[point][0] = size - 1 if points[point][0] > size - 1 else points[point][0]
            points[point][1] = size - 1 if points[point][1] > size - 1 else points[point][1]
            points[point][0] = 0 if points[point][0] < 0 else points[point][0]
            points[point][1] = 0 if points[point][1] < 0 else points[point][1]


        # calculatedMat, im_color_flow = Curl(mat)
        im_color_flow = vizFlow(mat)

        # Draw points
        im_color_flow = DrawPoints(im_color_flow, points)
        im_color_flow = DrawGlyphs(im_color_flow, glyphs)
        cv2.putText(im_color_flow, str(i), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

        # Record
        CaptureImage(writer, im_color_flow)

        cv2.imshow("image", im_color_flow)
        cv2.waitKey(1)
        i = i + 1




VizualizeGlyphs()


