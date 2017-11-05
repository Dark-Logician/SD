import pygame
from math import *
from pylygon import Polygon
from numpy import array

wall_l = Polygon([(0,0), (0,400)])
wall_t = Polygon([(0,0), (400,0)])
wall_b = Polygon([(0,400), (400,400)])
wall_r = Polygon([(400,0), (400,400)])


pygame.init
icon = pygame.image.load("C:\Users\Evan\Desktop\Code Projects\ShuttleDefender\SD - Sprites\Shuttle.PNG")
pygame.display.set_icon(icon)

robot_colour = (127,255,0)
laser_colour = (176, 0, 255)
screen = pygame.display.set_mode((400,400))
end = False
e3_laser_list = []

def magnitude(vector):
    magnitude = sqrt(vector[0]**2 + vector[1]**2)
    return magnitude

def angle(vector):
    return atan2(vector[1],vector[0])
    
def pnt_proj(position, angle, magnitude):
    pnt_x = position[0] + magnitude*cos(angle)
    pnt_y = position[1] + magnitude*sin(angle)
    return (pnt_x,pnt_y)

def pnt_move(position, x_d = 0, y_d = 0):
    pnt_x = position[0] + x_d
    pnt_y = position[1] + y_d
    return (pnt_x, pnt_y)

    # add argument 'direction' that creates rect on direction
    # parallel translation will be +/- sin(angle) +/-cos(angle)
    # perp. translation will be -sin(angle + pi), -cos(angle + pi)
    #I think
    
def rect_gen(position, width, height, move = (0,0)):
    pnt_0 = (position[0] - width + move[0], position[1] - height + move[1])
    pnt_1 = (position[0] - width + move[0], position[1] + height + move[1])
    pnt_2 = (position[0] + width + move[0], position[1]- height + move[1])
    pnt_3 = (position[0] + width + move[0], position[1] + height + move[1])
    return Polygon([pnt_0, pnt_1, pnt_2, pnt_3])
    
    # also add argument 'direction' that creates line on direction
    # from the start, project second point along direction
    # y comp is length * sin(direction) x comp is length * cos(direction)
    
def line_gen(position, length, direction = pi/2, move = 0, para = True):
    pnt_0 = (position[0] + move[0], position[1] + move[1])
    if para:
        pnt_1 = (position[0] + move[0], position[1] + length + move[1])
    else:
        pnt_1 = (position[0] + length + move[0], position[1] + move[1])
    return Polygon([pnt_0, pnt_1])

    # rotate_body takes a list of polygons, a point of rotation and some angle theta
    # and gives another list of polygons that have been rotated about
    # the point.
def rotate_body(body, pnt, theta):
    new_body = []
    for poly in body:
        new_poly = []
        for p in poly.P:
            dx = p[0] - pnt[0]
            dy = p[1] - pnt[1]
            mag = magnitude([dx, dy])
            angle = atan2(dy,dx)
            new_x = pnt[0] + mag*cos(theta + angle)
            new_y = pnt[1] + mag*sin(theta + angle)
            new_p = (new_x, new_y)
            new_poly.append(new_p)
        new_body.append(Polygon(new_poly))
    return new_body
            
class Body:
    def __init__(self, poly_list, direction, position):
        self.poly_list = poly_list
        self.direction = direction
        self.position = position
    
    def rotate(self, theta):
        new_body = []
        for poly in self.poly_list:
            new_poly = []
            for pnt in poly.P:
                dx = pnt[0] - self.position[0]
                dy = pnt[1] - self.position[1]
                mag = magnitude([dx, dy])
                angle = atan2(dy,dx)
                new_x = self.position[0] + mag*cos(theta + angle)
                new_y = self.position[1] + mag*sin(theta + angle)
                new_pnt = (new_x, new_y)
                new_poly.append(new_pnt)
            new_body.append(Polygon(new_poly))
        self.direction = self.direction + theta
        self.poly_list = new_body
        
        
    def draw(self, display):
        for poly in self.poly_list:
            pygame.draw.lines(display, robot_colour, True, poly.P)
    
    def move(self, new_position):
        self.position = new_position
    
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return '[' + str(self.x) + ',' + str(self.y) + ']'
        
    def add(self, v2):
        v3 = Vector(self.x + v2.x, self.y + v2.y)
        return v3
        
    def magnitude(self):
        magnitude = sqrt(self.x**2 + self.y**2)
        return magnitude
        
    def mult(self, c):
        v2 = Vector(self.x*c , self.y*c)
        return v2
        
    def angle(self):
        return atan2(self.y,self.x)

class Projectile:
    def __init__(self, position, velocity, length, colour):
        self.velocity = velocity
        self.position = position
        self.length = length
        self.colour = colour
        
    def __str__(self):
        return str(self.position) + str(self.velocity)
        
    def update(self, delta_t):
        self.position[0] = self.position[0]+(self.velocity[0]*delta_t)
        self.position[1] = self.position[1]+(self.velocity[1]*delta_t)
        
    def check_bounds(self):
        if (self.position[0] > 410) or (self.position[0] < -10) or (self.position[1] > 410) or (self.position[1] < -10):
            return False
        else:
            return True

class Enemy_3:

    def __init__(self, direction, position, velocity, health, state):
        self.direction = direction
        self.position = position
        self.velocity = velocity
        self.health = health
        self.state = state
        
        barrel_3 = line_gen(self.position, 25, move = (0, - 7))
        hull_left_3 = rect_gen(self.position, 2.5, 2, move = (- 5.5,- 2))
        hull_right_3 = rect_gen(self.position, 2.5, 2, move = (5.5,- 2))
        self.body = Body([barrel_3, hull_left_3, hull_right_3], self.direction, self.position)
        self.body.rotate(direction - pi/2)
    
    def __str__(self):
        return str(self.direction) + str(self.position) + str(self.velocity)    
    
    def update(self,delta_t):
        for poly in self.body.poly_list: 
            poly.move_ip(self.velocity[0]*(delta_t), self.velocity[1]*(delta_t))
        self.position = self.position + (self.velocity * (delta_t))
        self.velocity = self.velocity * (1-1.0*delta_t)
        if abs(self.velocity[0]) < 0.2: self.velocity[0] = 0
        if abs(self.velocity[1]) < 0.2: self.velocity[1] = 0
        self.body.move(self.position)
        
    def turn(self, angle, delta_t):
        self.direction = self.direction + angle*delta_t
        self.body.rotate(angle*delta_t)
        if self.direction > 2*pi:
            self.direction = self.direction-2*pi
        if self.direction < 0:
            self.direction = self.direction+2*pi
    
    def  move(self, speed):
        delta_v = array([cos(self.direction)*speed, sin(self.direction)*speed])
        self.velocity = self.velocity + (delta_v)
        if magnitude(self.velocity) > 10:
            self.velocity[0] = 10*cos(self.direction)
            self.velocity[1] = 10*sin(self.direction)
            
    def fire_laser(self):
        laser = Projectile(array([self.position[0] + 18*cos(self.direction), self.position[1]+ 18*sin(self.direction)]), array([cos(self.direction)*700,sin(self.direction)*800]), 10.0, laser_colour)
        return laser
            

pos_3 = (200, 200)
barrel_3 = line_gen(pos_3, 25, move = (0, - 7))
hull_l_3 = rect_gen(pos_3, 2.5, 2, move = (- 5.5,- 2))
hull_r_3 = rect_gen(pos_3, 2.5, 2, move = (5.5,- 2))

AAA = Enemy_3(0, array([200,200]), array([0,0]), 0, 0)
clock = pygame.time.Clock()

while not end:
    #events, keys, etc.
    
    tick = clock.get_time()/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True

            
    #Graphics
    
    screen.fill((0,0,0))
    AAA.turn(pi/2, tick)
    AAA.move(100)
    AAA.update(tick)
    e3_laser_list.append(AAA.fire_laser())
    
    AAA.body.draw(screen)
    
    
    for laser in e3_laser_list:
        if laser.check_bounds():
            laser.update(tick)
            pygame.draw.lines(screen, laser.colour ,False ,[(laser.position[0], laser.position[1]),(laser.position[0] + laser.length*cos(angle(laser.velocity)), laser.position[1] + laser.length*sin(angle(laser.velocity)))])
        else:
            e3_laser_list.remove(laser)

    clock.tick(60)
    pygame.display.update()
pygame.quit()