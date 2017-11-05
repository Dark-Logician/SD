import pygame
import math
from pylygon import Polygon
import numpy

wall_l = Polygon([(0,0), (0,400)])
wall_t = Polygon([(0,0), (400,0)])
wall_b = Polygon([(0,400), (400,400)])
wall_r = Polygon([(400,0), (400,400)])


pygame.init
#icon = pygame.image.load("C:\Users\Evan\Desktop\Code Projects\ShuttleDefender\SD - Sprites\Shuttle.PNG")
#pygame.display.set_icon(icon)

screen = pygame.display.set_mode((180,130))
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

def rect_gen(position, width, height, move = (0,0)):
    pnt_0 = (position[0] - width + move[0], position[1] - height + move[1])
    pnt_1 = (position[0] - width + move[0], position[1] + height + move[1])
    pnt_2 = (position[0] + width + move[0], position[1]- height + move[1])
    pnt_3 = (position[0] + width + move[0], position[1] + height + move[1])
    return Polygon([pnt_0, pnt_1, pnt_2, pnt_3])
    
def line_gen(position, length, move = 0, para = True):
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
        return math.atan2(self.y,self.x)

class Projectile():
    def __init__(self, position, velocity, length, colour):
        self.velocity = velocity
        self.position = position
        self.length = length
        self.colour = colour
        
    def __str__(self):
        return str(self.position) + str(self.velocity)
        
    def update(self, delta_t):
        self.position.x = self.position.x+(self.velocity.x*delta_t)
        self.position.y = self.position.y+(self.velocity.y*delta_t)
        
    def check_bounds(self):
        if (self.position.x > 410) or (self.position.x < -10) or (self.position.y > 410) or (self.position.y < -10):
            return False
        else:
            return True

class Entity:

    def __init__(self, direction, position, health, mode, velocity, friction, maxspeed, points):
        self.direction = direction
        self.position = position
        self.health = health
        self.mode = mode
        self.velocity = velocity
        self.friction = friction
        self.maxspeed = maxspeed
        pnts_list = []
        for i in points:
            pnts_list.append(pnt_proj(self.position, self.direction+i[0], i[1]))
        self.body = Polygon(pnts_list)
    
    def __str__(self):
        return str(self.direction) + str(self.position) + str(self.velocity)
        
    def _rect(self):
        return self.body.get_rect()
        
    
    def update(self,delta_t):
        self.body.move_ip(self.velocity.x*(delta_t), self.velocity.y*(delta_t))
        self.position = self.position.add(self.velocity.mult(delta_t))
        self.velocity = self.velocity.mult(1-self.friction*delta_t)
        if abs(self.velocity.x) < 0.2: self.velocity.x = 0
        if abs(self.velocity.y) < 0.2: self.velocity.y = 0
        self.body.C = (self.position.x, self.position.y)
        
    def turn(self, angle, delta_t):
        self.direction = self.direction + angle*delta_t
        self.body.rotate_ip(angle*delta_t)
        if self.direction > 2*math.pi:
            self.direction = self.direction-2*math.pi
        if self.direction < 0:
            self.direction = self.direction+2*math.pi
    
    def  move(self, speed):
        delta_v = Vector(math.cos(self.direction)*speed, math.sin(self.direction)*speed)
        self.velocity = self.velocity.add(delta_v)
        if self.velocity.magnitude > self.maxspeed:
            self.velocity.x = self.maxspeed*math.cos(self.direction)
            self.velocity.y = self.maxspeed*math.sin(self.direction)
            
    def check_bounds(self):
        rect =  self.body.get_rect()
    
        if rect.right > 400:
            self.position.x = 400 - abs(rect.right - self.position.x)
            self.velocity.x = 0
            
        if rect.left < 0:
            self.position.x = 0 + abs(rect.left - self.position.x)
            self.velocity.x = 0
        
        if rect.top < 0:
            self.position.y = 0 + abs(rect.top - self.position.y)
            self.velocity.y = 0
            
        if rect.bottom > 400:
            self.position.y = 400 - abs(rect.bottom - self.position.y)
            self.velocity.y = 0

# Enemy_1
# Standard Enemy, average speed, fire, power
pos_1 = (30,30)
hull_1 = rect_gen(pos_1, 5, 2)
nose_1 = line_gen(pos_1, 18, (0,- 5))
wing_r_1 = line_gen(pos_1, 9,(- 5, -3))
wing_l_1 = line_gen(pos_1, 9,(5, -3))

enemy_1_pol = [hull_1, nose_1, wing_r_1, wing_l_1]

    
#Enemy_2
#Standard Advanced Enemy, Enemy_1 but better
pos_2 = (30, 90)
hull_l_2 = rect_gen(pos_2, 3, 2, (-5,0))
hull_r_2 = rect_gen(pos_2, 3, 2, (5,0))
wing_l_2 = line_gen(pos_2, 12, (-8, -3))
wing_r_2 = line_gen(pos_2, 12, (8, -3))
barrel_l_2 = line_gen(pos_2, 24, (- 2, -5))
barrel_r_2 = line_gen(pos_2, 24, (2, -5))

enemy_2_pol = [hull_l_2, hull_r_2, wing_l_2, wing_r_2, barrel_l_2, barrel_r_2]

#Enemy_3
#Sniper Enemy, Stronger shot, less frequent fire
pos_3 = (90, 30)
barrel_3 = line_gen(pos_3, 25, (0, - 5))
hull_l_3 = rect_gen(pos_3, 2.5, 2, (- 5.5,0))
hull_r_3 = rect_gen(pos_3, 2.5, 2, (5.5,0))

enemy_3_pol = [hull_l_3, hull_r_3, barrel_3]

#Enemy_4
#Large barrel, Super Strong Fire
pos_4 = (90, 90)
barrel_4 = line_gen(pos_4, 32,(0,-8))
hull_I_4 = rect_gen(pos_4, 1, 5, (- 9, - 1))
hull_II_4 = rect_gen(pos_4, 1, 5, (- 4, + 1))
hull_III_4 = rect_gen(pos_4, 1, 5, (4, + 1))
hull_IV_4 = rect_gen(pos_4, 1, 5, (9, - 1))

enemy_4_pol = [barrel_4, hull_I_4, hull_II_4, hull_III_4, hull_IV_4]

#Enemy_5
#Bulky, shoots large square projectile
pos_5 = (150, 30)
hull_5 = rect_gen(pos_5, 6, 1, (0,0))
ray_l_5 = line_gen(pos_5, 25, (- 6, - 5))
ray_r_5 = line_gen(pos_5, 25, (6, - 5))


enemy_5_pol = [hull_5, ray_l_5, ray_r_5]

#Enemy_6
pos_6 = (150, 90)
hull_l_6 = rect_gen(pos_6, 4, 1, (- 5, 0))
hull_r_6 = rect_gen(pos_6, 4, 1, (5, 0))
ray_l_6 = line_gen(pos_6, 38, (-9, -8))
core_l_6 = line_gen(pos_6, 8, (-1, -2))
ray_r_6 = line_gen(pos_6, 38, (9, -8))
core_r_6 = line_gen(pos_6, 8, (1, -2))


enemy_6_pol = [hull_l_6, hull_r_6, ray_l_6, core_l_6, core_r_6, ray_r_6]
# main


enemy_list = [[enemy_1_pol, pos_1], [enemy_2_pol, pos_2], [enemy_3_pol, pos_3], [enemy_4_pol, pos_4], [enemy_5_pol, pos_5], [enemy_6_pol, pos_6]]
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
        enemy[0] = bodyrot(enemy[0], enemy[1], math.pi/180)
        for i in enemy[0]:
            pygame.draw.lines(screen, (127,255,0), True, i)
        
    # Laser Manipulation and Graphics
    
    clock.tick(60)
    pygame.display.update()
pygame.quit()

    