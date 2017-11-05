import pygame
import math
from pylygon import Polygon
from Entity import *
from Projectile import *
from Vector import *
import numpy

wall_l = Polygon([(0,0), (0,400)])
wall_t = Polygon([(0,0), (400,0)])
wall_b = Polygon([(0,400), (400,400)])
wall_r = Polygon([(400,0), (400,400)])


pygame.init
#icon = pygame.image.load("C:\Users\Evan\Desktop\Code Projects\ShuttleDefender\SD - Sprites\Shuttle.PNG")
#pygame.display.set_icon(icon)

screen = pygame.display.set_mode((200,200))
end = False
ship_laser_list = []

def magnitude(x, y):
        magnitude = math.sqrt(x**2 + y**2)
        return magnitude

def pnt_proj(position, angle, magnitude):
    pnt_x = position.x + magnitude*math.cos(angle)
    pnt_y = position.y + magnitude*math.sin(angle)
    return (pnt_x,pnt_y)

def pnt_move(position, x_d = 0, y_d = 0):
    pnt_x = position.x + x_d
    pnt_y = position.y + y_d
    return (pnt_x, pnt_y)

def poly_gen(position, points, move = (0,0)):
	newPoints = []
	for point in points:
		x = point[0] + position[0] + move[0]
		y = point[1] + position[1] + move[1]
		newPoints.append((x,y))
	return Polygon(newPoints)
    
def line_gen(position, length, move = (0,0), para = True):
    pnt_0 = (position[0] + move[0], position[1] + move[1])
    if para:
        pnt_1 = (position[0] + move[0], position[1] + length + move[1])
    else:
        pnt_1 = (position[0] + length + move[0], position[1] + move[1])
    return Polygon([pnt_0, pnt_1])

    # takes a list of polygons, a point of rotation and some angle theta
    # and gives another list of polygons that have been rotated about
    # the point.
	
def bodyrot(body, pnt, theta):
    new_body = []
    for poly in body:
        new_poly = []
        for p in poly.P:
            dx = p[0] - pnt[0]
            dy = p[1] - pnt[1]
            mag = magnitude(dx, dy)
            angle = math.atan2(dy,dx)
            new_x = pnt[0] + mag*math.cos(theta + angle)
            new_y = pnt[1] + mag*math.sin(theta + angle)
            new_p = (new_x, new_y)
            new_poly.append(new_p)
        new_body.append(Polygon(new_poly))
    return new_body
	
#changed just to figure out the shuttle shape below =======

def shuttlerot(shape, cnt, theta):
    new_shape = []
    for p in shape:
        dx = p[0] - cnt[0]
        dy = p[1] - cnt[1]
        mag = magnitude(dx, dy)
        angle = math.atan2(dy,dx)
        new_x = cnt[0] + mag*math.cos(theta + angle)
        new_y = cnt[1] + mag*math.sin(theta + angle)
        new_p = (new_x, new_y)
        new_shape.append(new_p)
    return new_shape


#==========================================================


#Shuttle
pos = (100, 100)
#left_wing = poly_gen(pos, 4, 1, (- 5, 0))
hull = poly_gen(pos, [(0,8), (6,4), (6,-4), (0,-8), (-6,-4), (-6,4)])
right_wing = poly_gen(pos, [(-3,-8), (3,-4), (3,4), (-3,-0)], (-9, 0))
left_wing = poly_gen(pos, [(3,-8), (-3,-4), (-3,4), (3,-0)], (9, 0))
proper_aesthetic = [(0,8),(12,0),(12,-8),(6,-4),(0,-8),(-6,-4),(-12,-8),(-12,0),(0,8), (0,-8)]
line = line_gen(pos, 16, (0,-8))

shuttle = []
for i in proper_aesthetic:
			shuttle.append((i[0] + 100, i[1] + 100))

shuttle_pol = [hull, right_wing, left_wing, line]
# main


enemy_list = [[shuttle_pol, pos]]
clock = pygame.time.Clock()
while not end:
    #events, keys, etc.
    
    tick = clock.get_time()/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
    
    #Graphics
    
    screen.fill((0,0,0))
    
    for enemy in enemy_list:
        #enemy[0] = bodyrot(enemy[0], enemy[1], math.pi/180)
        #for i in enemy[0]:
		shuttle = shuttlerot(shuttle, (100,100), math.pi/180)
		
		pygame.draw.lines(screen, (255,255,255), True, shuttle)
        
    # Laser Manipulation and Graphics
    
    clock.tick(60)
    pygame.display.update()
pygame.quit()

    