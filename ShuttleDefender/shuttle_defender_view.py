import pygame
import math
from pylygon import Polygon
import numpy

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

viewerPosition = [0,0]

def pnt_proj(position, angle, magnitude):
    pnt_x = position.x + magnitude*math.cos(angle)
    pnt_y = position.y + magnitude*math.sin(angle)
    return (pnt_x,pnt_y)

def pnt_move(position, x_d, y_d):
    pnt_x = position.x + x_d
    pnt_y = position.y + y_d
    return (pnt_x, pnt_y)
    
    
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
        self.vposition = position.x - viewerPosition[0], position.y - viewerPosition[1]
        
    def __str__(self):
        return str(self.position) + str(self.velocity)
        
    def update(self, delta_t):
        self.position.x = self.position.x+(self.velocity.x*delta_t)
        self.position.y = self.position.y+(self.velocity.y*delta_t)
        self.vposition = self.position.x - viewerPosition[0], self.position.y - viewerPosition[1]
        
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
        self.vposition = (position.x -viewerPosition[0], position.y - viewerPosition[1])
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
    
        if rect.right >= 400 and self.velocity.x > -1:
            self.position.x = 400 - abs(rect.right - self.position.x)
            self.velocity.x = 0
            
        if rect.left <= 0 and self.velocity.x < 1:
            self.position.x = 0 + abs(rect.left - self.position.x)
            self.velocity.x = 0
        
        if rect.top <= 0 and self.velocity.y < 1:
            self.position.y = 0 + abs(rect.top - self.position.y)
            self.velocity.y = 0
            
        if rect.bottom >= 400 and self.velocity.y > -1:
            self.position.y = 400 - abs(rect.bottom - self.position.y)
            self.velocity.y = 0
            
    
    def shoot(self):
        if self.mode == 0:
            laser = Projectile(Vector(self.position.x, self.position.y), Vector(math.cos(self.direction)*500,(math.sin(self.direction)*500)), 5.0, (255, 155, 155))
            return laser
            
        elif self.mode == 1:
            laser_1 = Projectile(Vector((self.position.x + 3 * (math.cos(ship.direction + 90))), self.position.y + 3 * (math.sin(ship.direction + 90))), Vector(math.cos(self.direction)*500,(math.sin(self.direction)*500)), 10.0, (0, 255, 255))
            
            laser_2 = Projectile((Vector(self.position.x + 3 * (math.cos((ship.direction - 90))), self.position.y + 3 * math.sin(ship.direction - 90))), Vector(math.cos(self.direction)*500,math.sin(self.direction)*500), 10.0, (0, 255, 255))
            
            return [laser_1, laser_2]
            
class Player_Ent(Entity):
    def __init__(self, direction, position, health, mode, velocity, friction, maxspeed, body):
        Entity.__init__(self, direction, position, health, mode, velocity, friction, maxspeed, body)
    
        
            
# hit boxes, boundaries, etc.
    
        

# ship object
ship = Entity((3*math.pi/2), Vector(200,300), 0, 0, Vector(0,0), 1.0, 150, [(0,10),(0,-10*math.sin(2.0/7*math.pi)),(7.0/9*math.pi, 10), (-7.0/9*math.pi, 10)])

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
    viewerPosition = ship.position
    if const_fire[1] == True:
        const_fire[0] += 1
        if const_fire[0] == 10:
            for i in ship.shoot():
                ship_laser_list.append(i)
            const_fire[0] = 0
    elif const_fire[0] == False:
                const_fire[0] = 9
    
    
    
    screen.fill((0,0,0))
    
    #Powerup Graphics
    
    pow_pos = Vector(200,100)
    pow_vpos = pow_pos.x - viewerPosition.x, pow_pos.y - viewerPosition.y
    pow_rgt = (pow_pos.x + 5, pow_pos.y)
    pow_bot = (pow_pos.x, pow_pos.y + 5)
    pow_lft = (pow_pos.x - 5, pow_pos.y)
    pow_top = (pow_pos.x, pow_pos.y - 5)
    pow_body = Polygon([pow_rgt, pow_bot, pow_lft, pow_top])
    pow_geom_list = [[pow_top, pow_bot], [pow_rgt, pow_lft], [pow_top, pow_rgt], [pow_top, pow_lft], [pow_bot, pow_lft], [pow_bot, pow_rgt]]
    #for i in pow_geom_list:
        #pygame.draw.lines(screen, (150,255,255),True,i)

        
    
    
    # Ship Graphics
    
    pygame.draw.lines(screen, (255,255,255),True,ship.body.P)
    pygame.draw.lines(screen, (255,255,255),False, [pnt_proj(ship.position, ship.direction, 10), pnt_proj(ship.position, ship.direction, -1 *math.sin(2.0/9*math.pi))])
    shipline = ship.body.project((0,1))

    
    # Laser Manipulation and Graphics
    
    # For projectile objects
    for laser in ship_laser_list:
        if laser.check_bounds():
            laser.update(tick)
            pygame.draw.lines(screen, laser.colour ,False ,[(laser.vposition.x, laser.vposition.y),(laser.position.x + laser.length*math.cos(laser.velocity.angle()), laser.position.y + laser.length*math.sin(laser.velocity.angle()))])
        else:
            ship_laser_list.remove(laser)
    
    
    
    
    
    # Tests go here
    print pow_vpos
    
    
    
    
    
    clock.tick(60)
    pygame.display.update()
pygame.quit()

    
    
    
    
    
    
