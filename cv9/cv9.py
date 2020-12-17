import numpy as np
import math
import matplotlib.pyplot as plt
import re
import pandas as pd

pathCSV = "C:/Users/Pinkie/Desktop/VD/DataVisualisation/cv9/dimred/data/menu20.csv"
pathTXT = "C:/Users/Pinkie/Desktop/VD/DataVisualisation/cv9/dimred/data/menu.txt"
pathRES = "C:/Users/Pinkie/Desktop/VD/DataVisualisation/cv9/dimred/data/result.txt"

badMeals = [32, 33, 34, 81, 31, 82, 252, 254]
healthyMeals = [42, 49, 50, 79, 85, 87, 88, 102, 103]


# Result
def VizualizeRES():
    file = open(pathRES, "r")
    lines = file.readlines()

    for line in lines:
        tmp = line.rstrip()
        numbers = tmp.split(" ")
        x = numbers[0]
        y = numbers[len(numbers)-1]
        plt.scatter(float(x), float(y), s=2)
    
    plt.show()

# Vizualize bad and good health food
def Vizualize15():
    # too bad = 34, 35, 36, 37, 

    file = open(pathRES, "r")
    lines = file.readlines()

    count = 0
    for line in lines:
        if (count in healthyMeals or count in badMeals):
            tmp = line.rstrip()
            numbers = tmp.split(" ")
            x = float(numbers[0])
            y = float(numbers[len(numbers)-1])
            if(count in badMeals):
                plt.scatter(x, y, s=10, c="blue")
            if(count in healthyMeals):
                plt.scatter(x, y, s=10, c="red")
            plt.text(x, y, str(count))
            
        count = count + 1
    
    plt.ylabel("Bad meal")
    plt.xlabel("Healthy meal")
    plt.show()

###
VizualizeRES()
Vizualize15()