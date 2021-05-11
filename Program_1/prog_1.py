# COPY THIS CODE TO CREATE A .py FILE TO RUN or COPY TO A JUPYTER (NOT COLAB) NOTEBOOK AND RUN
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:04:11 2020
CSE 30 Spring 2020 Program 1 helper code
@author: Fahim
"""

import math
import turtle
import random

# Note: For this example, we are using hardcoded points/vertices to test the functionalities of the viewer and animation.
# For Program 1, you need to replace the code between the tags # BEGIN and # END with your code.
# Your code should generate the VERTICES and TRIANGLES using your recursive "midpoint_displacement" function.
# This setup is optimized for points values generated in the range -1.00 to 1.00.
# You may need the adjust the value of FOV to generate points with higher ranges.


# BEGIN
# =====================================================================
# Level 0 terrain (1 triangle)
# VERTICES = [(-1, 0, 0), ( 1, 0, 0), ( 0, 1, 0)]

# TRIANGLES = [(0, 1, 2)]

# Level 1 terrain (4 pregenerated triangles)
VERTICES = []
TRIANGLES = []

num = 0


def prep(terrain, how_many = 0, length = 0):
    terrain.penup()
    terrain.forward(length)
    pt_1 = (0, 0)
    pt_2 = (terrain.pos())
    terrain.left(120)
    terrain.forward(length)
    pt_3 = (terrain.pos())
    terrain.setheading(terrain.towards(0, 0))
    terrain.forward(terrain.distance(0, 0))
    recur_tri(terrain, pt_1, pt_2, pt_3, 0, how_many, length)

def recur_tri(terrain, pt_1, pt_2, pt_3, level, end, length):
    if level >= end:
        temp_1 = int(length * -100)
        temp_2 = int(length * 100)
        global num
        is_in = False
        for i in VERTICES:
            if pt_1[0] == i[0] and pt_1[1] == i[1]:
                z = i[2]
                is_in = True
        if not is_in:
            z = random.choice(range(temp_1, temp_2, 5)) / 100
            #random.random()
        temp = list(pt_1)
        temp.append(z)
        pt_1 = tuple(temp)
        is_in = False
        for i in VERTICES:
            if pt_2[0] == i[0] and pt_2[1] == i[1]:
                x = i[2]
                is_in = True
        if not is_in:
            x = random.choice(range(temp_1, temp_2, 5)) / 100
        temp = list(pt_2)
        temp.append(x)
        pt_2 = tuple(temp)
        is_in = False
        for i in VERTICES:
            if pt_3[0] == i[0] and pt_3[1] == i[1]:
                y = i[2]
                is_in = True
        if not is_in:
            y = random.choice(range(temp_1, temp_2, 5)) / 100
        temp = list(pt_3)
        temp.append(y)
        pt_3 = tuple(temp)
        TRIANGLES.append((num, num + 1, num + 2))
        VERTICES.append(pt_1)
        VERTICES.append(pt_2)
        VERTICES.append(pt_3)
        num += 3
        return
    terrain.penup()
    terrain.setpos(pt_1)
    terrain.setheading(terrain.towards(pt_2))
    terrain.forward(terrain.distance(pt_2) / 2)
    new_pt_1 = terrain.pos()
    terrain.setpos(pt_2)
    terrain.setheading(terrain.towards(pt_3))
    terrain.forward(terrain.distance(pt_3) / 2)
    new_pt_2 = terrain.pos()
    terrain.setpos(pt_3)
    terrain.setheading(terrain.towards(pt_1))
    terrain.forward(terrain.distance(pt_1) / 2)
    new_pt_3 = terrain.pos()
    level += 1
    recur_tri(terrain, new_pt_1, new_pt_2, new_pt_3, level, end, length)
    recur_tri(terrain, pt_1, new_pt_1, new_pt_3, level, end, length)
    recur_tri(terrain, new_pt_1, pt_2, new_pt_2, level, end, length)
    recur_tri(terrain, new_pt_3, new_pt_2, pt_3, level, end, length)



# =====================================================================
# END

def transform(x, y, z, angle, tilt):
    # Animation control (around y-axis)
    s, c = math.sin(angle), math.cos(angle)
    x, y = x * c - y * s, x * s + y * c

    # Camera tilt  (around x-axis)
    s, c = math.sin(tilt), math.cos(tilt)
    z, y = z * c - y * s, z * s + y * c

    # Setting up View Parameters
    y += 5  # Fixed Distance from top
    FOV = 1000  # Fixed Field of view
    f = FOV / y
    sx, sy = x * f, z * f
    return sx, sy


def main():
    # Create terrain using turtle
    terrain = turtle.Turtle()
    terrain.pencolor("blue")
    terrain.pensize(2)

    # Turn off move time for instant drawing
    turtle.tracer(0, 0)
    terrain.speed(1)
    angle = 0

    how_many = int(input("How many Levels of Recursion: "))
    length = float(input("Enter Length of Triangle: "))
    prep(terrain, how_many, length)

    while True:
        # Clear the screen
        terrain.clear()

        # Transform the terrain
        VERT2D = []
        for vert3D in VERTICES:
            x, y, z = vert3D
            sx, sy = transform(x, y, z, angle, 0.25)
            VERT2D.append((sx, sy))

        # Draw the terrain
        for triangle in TRIANGLES:
            points = []
            points.append(VERT2D[triangle[0]])
            points.append(VERT2D[triangle[1]])
            points.append(VERT2D[triangle[2]])

            # Draw the trangle
            terrain.goto(points[0][0], points[0][1])
            terrain.down()

            terrain.goto(points[1][0], points[1][1])
            terrain.goto(points[2][0], points[2][1])
            terrain.goto(points[0][0], points[0][1])
            terrain.up()
        # Update screen
        turtle.update()

        # Control the speed of animation
        angle += 0.0005


if __name__ == "__main__":
    main()
