import numpy as np
import math
import matplotlib.pyplot as plt

pathCSV = "/media/pinkie/FA3E8D353E8CEBC7/Users/Pinkie/Desktop/VD/dimred/data/menu.csv"
pathTXT = "/media/pinkie/FA3E8D353E8CEBC7/Users/Pinkie/Desktop/VD/dimred/data/menu.txt"

def VizualizeTXT():
    file = open(pathTXT, "r")
    lines = file.readlines()

    for line in lines:
        print(line)



###
VizualizeTXT()