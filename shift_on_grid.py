"""
This file takes an .xyz file and shifts all the points onto a grid set by the first point.
Outputs it to shifted_points.xyz
"""

from matplotlib import pyplot as plt
import numpy as np
import math
from scipy.spatial.distance import cdist
file = open('gc_coords.xyz', 'r')
# xfile = open('x.xyz', 'a')
# yfile = open('y.xyz', 'a')
# zfile = open('z.xyz', 'a')
ofile = open('shifted_points.xyz', 'a')

# examplefile = open()

Lines = file.readlines()


# base_x = float(Lines[100].split()[0]) # single point that everything will be gridded on

# distances = []


# curr_z = Lines[0].split()[2]
curr_z = 0

# print("first z: " + str(curr_z))

def parse_z(curr_z):
    x_cords = []
    y_cords = []
    z_cords = []

    for line in Lines:
        if (float(line.split()[2]) == curr_z):
            x_cords.append(float(line.split()[0]))
            y_cords.append(float(line.split()[1]))

            # ofile.write(str(line.split()[0]) + " " + str(line.split()[1]) + " 1240.00 128 128 128")
            # ofile.write('\n')



    ####################################################
            
    # parse into y rows with x values   
    backupx = x_cords.copy()
    backupy = y_cords.copy()
    dimensions = []
    curr_y = y_cords[0]
    found_indices = []
    unique_y = []
    index = 0;


    for l in range(len(y_cords)):
        if (y_cords[l] != -1):
            curr_y = y_cords[l]
            for j in range(len(y_cords)):
                if (y_cords[j] == curr_y):
                    found_indices.append(j)
                    y_cords[j] = -1 # done with it
            dimensions.append([])
            unique_y.append(curr_y) # unique y
            for ix in found_indices:
                dimensions[index].append(x_cords[ix]) # add x cords
            index += 1
            found_indices = []


    # sort lists in ascending order
    for y in range(len(dimensions)):
        dimensions[y].sort()

    # shifting points
    base_x = dimensions[0][0] # grid will be based on this
    # print("base point x, y: ")
    # print (dimensions[0][0])
    # print (unique_y[0])
    difference = 0
    # print("---------")
    for y in range(len(dimensions)):
        # print("now working on layer " + str(y) + " " + str(unique_y[y]) + " and x" + str(dimensions[y][0]))
        if (((base_x - dimensions[y][0]) % 16 <= 8) and (base_x < dimensions[y][0])):
            # closest bin is left
            difference = ((abs(base_x - dimensions[y][0])) % 16)
            # print("difference is " + str(difference))
            for x in range(len(dimensions[y])):
                dimensions[y][x] = dimensions[y][x] - difference
            
        elif (((base_x - dimensions[y][0]) % 16 > 8) and (base_x < dimensions[y][0])):
            # closest bin is right
            difference = (abs(base_x - dimensions[y][0]) % 16)
            for x in range(len(dimensions[y])):
                dimensions[y][x] = dimensions[y][x] + (16-difference)

        if (((base_x - dimensions[y][0]) % 16 <= 8) and (base_x > dimensions[y][0])):
            # closest bin is left
            difference = ((abs(base_x - dimensions[y][0])) % 16)
            # print("difference is " + str(difference))
            for x in range(len(dimensions[y])):
                dimensions[y][x] = dimensions[y][x] + difference
        
        elif (((base_x - dimensions[y][0]) % 16 > 8) and (base_x > dimensions[y][0])):
            # closest bin is right
            difference = (abs(base_x - dimensions[y][0]) % 16)
            for x in range(len(dimensions[y])):
                dimensions[y][x] = dimensions[y][x] - (16-difference)
        

    # print("base point is " + str(unique_y[y]) + "," + str(dimensions[y][x]))
    # shift outliers


    # in case it is still not on a grid, keep gridding
    for random in range(100):
        for y in range(len(dimensions)):
            for x in range(len(dimensions[y])):
                difference = (base_x - dimensions[y][x]) % 16
                if (difference != 0):
                    # print("Layer: " + str(y) + ", ("  + str(dimensions[y][x]) + "," + str(unique_y[y]) + ")") 
                    # print("difference:  " + str(difference))

                    if (((base_x - dimensions[y][x]) % 16 <= 8) and (base_x < dimensions[y][x])):
                        dimensions[y][x] = dimensions[y][x] + difference
                    if (((base_x - dimensions[y][x]) % 16 > 8) and (base_x < dimensions[y][x])):
                        dimensions[y][x] = dimensions[y][x] - (16-difference)
                    if (((base_x - dimensions[y][x]) % 16 <= 8) and (base_x > dimensions[y][x])):
                        dimensions[y][x] = dimensions[y][x] - difference
                    if (((base_x - dimensions[y][x]) % 16 > 8) and (base_x > dimensions[y][x])):
                        dimensions[y][x] = dimensions[y][x] + (16-difference)
                
                
                




    # putting back into plottable lists
    backupx = []
    backupy = []
    for y in range(len(dimensions)):
        for m in range(len(dimensions[y])):
            backupy.append(unique_y[y])
            backupx.append(dimensions[y][m])

    # output to file
    for y in range(len(dimensions)):
        for m in range(len(dimensions[y])):
            # x y z 128 128 128 
            ofile.write(str(dimensions[y][m]) + " " + str(unique_y[y]) + " " + str(curr_z) + " 128 128 128")
            ofile.write('\n')











    # print("unique y list: ")
    # print(unique_y)

    # print("x as well: ")
    # for i in range(len(unique_y)):
    #     print(str(unique_y[i]) + ": ")
    #     print(dimensions[i])


    # print("num of pts: ")
    # sum = 0
    # for i in range(len(unique_y)):
    #     sum += len(dimensions[i])














    # plt.scatter(backupx, backupy, marker='s')
    # # array of (x, y) coords
    # points = np.column_stack((backupx, backupy))
    # # numpy :
    # # Take a sequence of 1-D arrays and 
    # # stack them as columns to make a single 2-D array

    # # Calculate distances
    # distances = cdist(points, points)

    # # Set distance to self to infinity 
    # np.fill_diagonal(distances, np.inf)

    # # Find minimum distance for each point
    # min_distances = np.min(distances, axis=1)


    # # Find the minimum distance for each point
    # min_distances = np.min(distances, axis=1)
    # # print("Minimum distances for each point:", min_distances)
    # # for x in min_distances:
    # #     # print(x)
    # #     if (x != 16.0):
    # #         print("found outlier" + str(x))
    # #         print()




    # # outliers = []
    # # for i in range(len(min_distances)):
    # #     if (min_distances[i] != 16.0):
    # #         # print("Found outlier: " + str(min_distances[i]))
    # #         ofile.write("Found outlier: (" + str(x_cords[i]) + ", " +  str(y_cords[i]) + ")" + " with distance " + str(min_distances[i]) + "\n")
    # #         outliers.append(i)

    # # for i in outliers:
    # #     plt.plot(x_cords[i], y_cords[i], 'g*')


    # ax = plt.gca()
    # ax.set_aspect('equal', adjustable='box')


    # # closest_indices = np.argmin(distances, axis=1)
    # # for i, idx in enumerate(closest_indices):
    # #     plt.plot([x_cords[i], x_cords[idx]], [y_cords[i], y_cords[idx]], 'r--')

    # # for x in min_distances:
    # #     print(x)

    # # plt.hist(min_distances, bins=7, edgecolor='black')

    # plt.show()


def get_ranges():

    x_max = 0
    x_min = float(Lines[0].split()[0])
    y_max = 0
    y_min = float(Lines[0].split()[1])
    z_max = 0
    z_min = float(Lines[0].split()[2])
    for line in Lines:
        if (float(line.split()[0]) < x_min):
            x_min = float(line.split()[0])
        if (float(line.split()[1]) < y_min):
            y_min = float(line.split()[1])
        if (float(line.split()[2]) < z_min):
            z_min = float(line.split()[2])

        if (float(line.split()[0]) > x_max):
            x_max = float(line.split()[0])
        if (float(line.split()[1]) > y_max):
            y_max = float(line.split()[1])
        if (float(line.split()[2]) > z_max):
            z_max = float(line.split()[2])

    print("x max: " + str(x_max))
    print("y max: " + str(y_max))
    print("z max: " + str(z_max))
    print("-----")

    print("x min: " + str(x_min))
    print("y min: " + str(y_min))
    print("z min: " + str(z_min))



print("parsing each line")
for line in Lines:
    reading_z = line.split()[2]
    if (float(reading_z) != float(curr_z)):
        parse_z(float(reading_z))
        curr_z = float(reading_z)
print("end of parsing each line")
print("-------")
print("getting ranges")
get_ranges()
print("got ranges")


# parse_z(1240.00)
