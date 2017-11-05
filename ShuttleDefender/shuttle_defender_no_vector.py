import pygame
import math
from pylygon import Polygon
from numpy import array

wall_l = Polygon([(0,0), (0,400)])
wall_t = Polygon([(0,0), (400,0)])
wall_b = Polygon([(0,400), (400,400)])
wall_r = Polygon([(400,0), (400,400)])

pygame.init
icon = pygame.image.load("C:\Users\Evan\Desktop\Code Projects\ShuttleDefender\SD - Sprites\Shuttle.PNG")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((400,400))
end = False
ship_laser_list = []

# Creates a polygon given a position a difference in angle, and a magnitude. This difference in angle 
# to be a difference between a 'forward' direction and where this point should be relatively. 
def pnt_proj(position, angle, magnitude):
    pnt_x = position[0] + magnitude*math.cos(angle)
    pnt_y = position[1] + magnitude*math.sin(angle)
    return (pnt_x,pnt_y)

# Similar to pnt_proj, but instead of an angle and magnitude, takes a difference in the x-axis and y-axis.

def pnt_move(position, x_d, y_d):
    pnt_x = position[0] + x_d
    pnt_y = position[1] + y_d
    return (pnt_x, pnt_y)
    
def magnitude(vector):
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    return magnitude
        
def angle(vector):
    return math.atan2(vector[1],vector[0])

# This is a class for projectiles

class Projectile():
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

# This is the class for all ships (currently), enemies, the player ship, and the shuttle.
        
class ShipEntity:

    def __init__(self, direction, position, health, mode, velocity, friction, maxspeed, points):
        self.direction = direction
        self.position = position
        self.health = health
        self.mode = mode
        self.velocity = velocity
        self.friction = friction
        self.maxspeed = maxspeed
        
        
        ship_nose = pnt_proj(self.position, self.direction, 10)
        ship_wing_r = pnt_proj(self.position, self.direction + 7.0/9*math.pi, 10)
        ship_wing_l = pnt_proj(self.position, self.direction - 7.0/9*math.pi, 10)
        ship_tail = pnt_proj(self.position, self.direction, 5.5)
        self.body = Polygon([ship_nose, ship_wing_l, ship_wing_r])
        self.line = Polygon([ship_nose, ship_tail])
    
    def __str__(self):
        return str(self.direction) + str(self.position) + str(self.velocity)
        
    def _rect(self):
        return self.body.get_rect()
        
    
    def update(self,delta_t):
        self.body.move_ip(self.velocity[0]*(delta_t), self.velocity[1]*(delta_t))
        self.position = self.position + (self.velocity * (delta_t))
        self.velocity = self.velocity * (1-self.friction*delta_t)
        if abs(self.velocity[0]) < 0.2: self.velocity[0] = 0
        if abs(self.velocity[1]) < 0.2: self.velocity[1] = 0
        self.body.C = (self.position[0], self.position[1])
        
    def turn(self, angle, delta_t):
        self.direction = self.direction + angle*delta_t
        self.body.rotate_ip(angle*delta_t)
        if self.direction > 2*math.pi:
            self.direction = self.direction-2*math.pi
        if self.direction < 0:
            self.direction = self.direction+2*math.pi
    
    def  move(self, speed):
        delta_v = array([math.cos(self.direction)*speed, math.sin(self.direction)*speed])
        self.velocity = self.velocity + (delta_v)
        if magnitude(self.velocity) > self.maxspeed:
            self.velocity[0] = self.maxspeed*math.cos(self.direction)
            self.velocity[1] = self.maxspeed*math.sin(self.direction)
            
    def check_bounds(self):
        rect =  self.body.get_rect()
    
        if rect.right >= 400 and self.velocity[0] > -1:
            self.position[0] = 400 - abs(rect.right - self.position[0])
            self.velocity[0] = 0
            
        if rect.left <= 0 and self.velocity[0] < 1:
            self.position[0] = 0 + abs(rect.left - self.position[0])
            self.velocity[0] = 0
        
        if rect.top <= 0 and self.velocity[1] < 1:
            self.position[1] = 0 + abs(rect.top - self.position[1])
            self.velocity[1] = 0
            
        if rect.bottom >= 400 and self.velocity[1] > -1:
            self.position[1] = 400 - abs(rect.bottom - self.position[1])
            self.velocity[1] = 0
            
    
    def shoot(self):
        if self.mode == 0:
            laser = Projectile(array([self.position[0], self.position[1]]), array([math.cos(self.direction)*500,math.sin(self.direction)*500]), 5.0, (255, 155, 155))
            return laser
            
        elif self.mode == 1:
            laser_1 = Projectile(array([(self.position[0] + 3 * (math.cos(ship.direction + 90))), self.position[1] + 3 * (math.sin(ship.direction + 90))]), array([math.cos(self.direction)*500,(math.sin(self.direction)*500)]), 10.0, (0, 255, 255))
            
            laser_2 = Projectile((array([self.position[0] + 3 * (math.cos((ship.direction - 90))), self.position[1] + 3 * math.sin(ship.direction - 90)])), array([math.cos(self.direction)*500,math.sin(self.direction)*500]), 10.0, (0, 255, 255))
            
            return [laser_1, laser_2]    
            
# hit boxes, boundaries, etc.
    
        

# ship object
ship = ShipEntity((3*math.pi/2), array([200,300]), 0, 0, array([0,0]), 1.0, 150, [(0,10),(0,-10*math.cos(2.0/7*math.pi)),(7.0/9*math.pi, 10), (-7.0/9*math.pi, 10)])

movement = False
turnright = False
turnleft = False
const_fire = [0, False]


# main

clock = pygame.time.Clock()
while not end:

    #events, keys, etc.
    
    tick = clock.get_time()/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]: 
                movement = True
            if key[pygame.K_RIGHT]:
                turnright = True
            if key[pygame.K_LEFT]:
                turnleft = True
            if key[pygame.K_z]:
                if ship.mode == 0:
                    ship_laser_list.append(ship.shoot())
                elif ship.mode == 1:
                    const_fire[1] = True
            if key[pygame.K_x]:
                if ship.mode == 1:
                    ship.mode = 0
                    const_fire[1] = False
                elif ship.mode == 0:
                    ship.mode = 1
                        
        if event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_RIGHT:
                turnright = False
            if key == pygame.K_LEFT:
                turnleft = False 
            if key == pygame.K_UP:
                movement = False
            if key == pygame.K_z and ship.mode == 1:
                const_fire[1] = False
    
    #responses to keys; i.e. movement and turning
    
    if movement:
        ship.move(100)
    if turnright:
        ship.turn(+math.pi*3/2.0,tick)
    if turnleft:
        ship.turn(-math.pi*3/2.0, tick)
    ship.check_bounds()
    ship.update(tick)
    if const_fire[1] == True:
        const_fire[0] += 1
        if const_fire[0] == 10:
            for i in ship.shoot():
                ship_laser_list.append(i)
            const_fire[0] = 0
    elif const_fire[0] == False:
                const_fire[0] = 9
    
    
    
    screen.fill((0,0,0))
    
    #Collision test
    
    Square = Polygon([(200,200), (100,200), (100,100), (200,100)])
    pygame.draw.lines(screen, (255,255,255), True ,Square)
    
    print Square.raycast(ship.body, array([-ship.velocity[0]*tick, -ship.velocity[1]*tick]))
    
    
    # Ship Graphics
    shipnose = (ship.position[0] + 10 * math.cos(ship.direction), ship.position[1] + 10 * math.sin(ship.direction))
    shiptail = (ship.position[0] + 5.8 * -math.cos(ship.direction), ship.position[1] + 5.8 * -math.sin(ship.direction))
    pygame.draw.lines(screen, (255,255,255),True,ship.body.P)
    pygame.draw.lines(screen, (255,255,255),False, [shipnose, shiptail])
    #shipline = ship.body.project((ship.direction))

    #pygame.draw.lines(screen, (255,255,255), True, ship.body.project((0,1)))
    # Laser Manipulation and Graphics
    
    # For projectile objects
    for laser in ship_laser_list:
        if laser.check_bounds():
            laser.update(tick)
            pygame.draw.lines(screen, laser.colour ,False ,[(laser.position[0], laser.position[1]),(laser.position[0] + laser.length*math.cos(angle(laser.velocity)), laser.position[1] + laser.length*math.sin(angle(laser.velocity)))])
        else:
            ship_laser_list.remove(laser)
    
    clock.tick(60)
    pygame.display.update()
pygame.quit()

    
    
    
    
    
    
