"""
this example demonstrates how to implement continuous collision detection using
raycasting method
"""
  
  
  
from operator import mul
  
from numpy import array, dot
from pylygon import Polygon
from pylygon.polygon import _MACHEPS
import pygame
from pygame import display, draw, event, mouse, Surface
from pygame.locals import *
  
  
  
from numpy import seterr
seterr(divide='raise')
  
  
  
_prod = lambda X: reduce(mul, X)                        # product
  
  
  
if __name__ == '__main__':
    pygame.init()
  
    SCREEN_SIZE = (800, 600)               # initialize screen size
    SCREEN = display.set_mode(SCREEN_SIZE) # load screen
  
    square1 = Polygon([(50, 100), (100, 50), (100, 100), (50, 50)])

    square2 = Polygon([(0, 30), (30, 0), (0, 0), (30, 30)])
  
    square1.move_ip(200, 200)
    square2.move_ip(300, 300)
  
    grab, other, theta = None, None, 0
    while 1:
        print "yo"
        SCREEN.fill((0, 0, 0))
        draw.polygon(SCREEN, (255, 0, 0), square1.P, 1)
        draw.polygon(SCREEN, (0, 0, 255), square2.P, 1)
        mouse_pos = array(mouse.get_pos())
        for ev in event.get():
            if ev.type == KEYDOWN:
                if ev.key == K_q: exit()
                if ev.key == K_LEFT: theta = -0.01
                if ev.key == K_RIGHT: theta = 0.01
            if ev.type == KEYUP:
                if ev.key == K_LEFT: theta = 0
                if ev.key == K_RIGHT: theta = 0
            if ev.type == MOUSEBUTTONDOWN:
                if grab: grab, other = None, None
                elif square2.collidepoint(mouse_pos):
                    grab = square2
                    other = square1
                elif square1.collidepoint(mouse_pos):
                    grab = square1
                    other = square2
  
        Y_square1 = square1.project((0, 1))
        Y_square2 = square2.project((0, 1))
        draw.line(SCREEN, (255, 0, 0), (2, Y_square1[0]), (2, Y_square1[1]), 2)
        draw.line(SCREEN, (0, 0, 255), (7, Y_square2[0]), (7, Y_square2[1]), 2)
  
        X_square1 = square1.project((1, 0))
        X_square2 = square2.project((1, 0))
        draw.line(SCREEN, (255, 0, 0), (X_square1[0], 2), (X_square1[1], 2), 2)
        draw.line(SCREEN, (0, 0, 255), (X_square2[0], 7), (X_square2[1], 7), 2)
  
        draw.circle(SCREEN, (255, 255, 255), square1.C.astype(int), 3)
        draw.circle(SCREEN, (255, 255, 255), square2.C.astype(int), 3)
  
        # NOTES on GJK:
        # ray r provided to the raycast algorithm must be towards the origin
        #   with respect to the movement direction; that is -r
        if grab:
            r = grab.C - mouse_pos # r is neg what mouse.get_rel() should return
            print r
            results = grab.raycast(other, r, self_theta = theta)
            if results:
                # if the objects are already intersecting, the results will be
                # zeros for everything.
                if results[0] == 0:
                    # use the hit normal to ensure the object is moving away
                    # from the intersection
                    if dot(r, n) > 0:
                        grab.move_ip(*-r)
                        # rotate?
                else:
                    lambda_, q, n = results
                    # does this shrink lambda_ and q by just enough to prevent contact?
                    s = 1 - _MACHEPS # at what magnitude of number will q be reducing movement by a couple of pixels?
                    lambda_ *= s
                    q *= s
                    grab.move_ip(*-q)
                    grab.rotate_ip(lambda_ * theta)
            else:
                grab.move_ip(*-r)
                grab.rotate_ip(theta)
        display.update()
