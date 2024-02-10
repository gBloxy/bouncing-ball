
from sys import exit
from math import sqrt, cos, sin, acos, pi, radians
import pygame


WIN_SIZE = (700, 500)

win = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption('bouncing ball')

clock = pygame.time.Clock()


def distance(pos1, pos2):
    return sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)


class Line():
    def __init__(self, point1, point2):
        self.pos1 = point1 if point1[0] > point2[0] else point2
        self.pos2 = point1 if self.pos1 != point1 else point2
        
        self.length = distance(self.pos1, self.pos2)
        
        T = (self.pos2[0], self.pos1[1])
        P1 = self.pos1
        P2 = self.pos2
        
        P1T = distance(P1, T)
        P2T = distance(P2, T)
        P1P2 = distance(P1, P2)
        
        if P1T == 0:
            alpha = pi
        elif P2T == 0:
            alpha = pi / 2
        else:
            alpha = acos((P2T**2 + P1P2**2 - P1T**2) / (2 * P2T * P1P2))
        if P1[1] > P2[1]:
            alpha = pi - alpha
        
        self.angle = alpha


class Ball():
    def __init__(self, center, angle=180):
        self.center = list(center)
        self.angle = radians(angle)
        self.radius = 8
        self.vel = 1
    
    def collide(self, l):
        d1 = distance(self.center, l.pos1)
        d2 = distance(self.center, l.pos2)
        
        P = (d1 + d2 + l.length) / 2
        A = sqrt(P * (P - d1) * (P - d2) * (P - l.length))
        H = (2 * A) / l.length
        
        if H <= self.radius and d1 < l.length and d2 < l.length:
            return True
        else:
            return False
    
    def collide_ball(self, b):
        if distance(self.center, b.center) < self.radius + b.radius:
            return True
        else:
            return False
    
    def bounce(self, l):
        self.angle = l.angle * 2 - self.angle
    
    def bounce_ball(self, b):
        b_angle = b.angle
        b.angle = self.angle
        self.angle = b_angle
    
    def update(self):
        for l in lines:
            if self.collide(l):
                self.bounce(l)
        for b in balls:
            if b != self:
                if self.collide_ball(b):
                    self.bounce_ball(b)
        
        self.center[0] += sin(self.angle) * self.vel
        self.center[1] -= cos(self.angle) * self.vel
        
        if not ((-10 < self.center[0] < WIN_SIZE[0] + 10) and (-10 < self.center[1] < WIN_SIZE[1] + 10)):
            balls.remove(self)


def add_line():
    global p1, p2
    line = Line(p1, p2)
    if line.length > 10:
        lines.append(line)
    p1 = p2 = None


def add_ball():
    global p1
    balls.append(Ball(mouse_pos))
    p1 = None


p1 = p2 = None

lines = []
balls = []

key_timer = 0


while True:
    dt = clock.tick(60)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()
    
    mouse_pos = pygame.mouse.get_pos()
    
    if key_timer > 0:
        key_timer -= dt
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # add a new line
            if event.button == 1:
                if p1 is None:
                    p1 = mouse_pos
                elif p2 is None:
                    p2 = mouse_pos
                    add_line()
            
            # spawn a new ball at the mouse position by right clicking
            elif event.button == 3:
                add_ball()
        
        # close the program
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    win.fill('black')
    
    # spawn a new ball at the mouse position by pressing the spacebar
    if keys[pygame.K_SPACE] and key_timer <= 0:
        add_ball()
        key_timer = 300
    
    # remove the last line placed
    if keys[pygame.K_BACKSPACE] and key_timer <= 0 and lines:
        lines.pop(-1)
        key_timer = 400
    
    # render lines
    for l in lines:
        pygame.draw.line(win, 'white', l.pos1, l.pos2, 4)
    
    # render line preview
    if p1 is not None:
        pygame.draw.line(win, 'gray', p1, mouse_pos, 3)
    
    # render balls
    for b in balls:
        b.update()
        pygame.draw.circle(win, 'red', b.center, b.radius)
    
    pygame.display.flip()
