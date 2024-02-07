
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
        
        alpha = acos((P2T**2 + P1P2**2 - P1T**2) / (2 * P2T * P1P2))
        if P1[1] < P2[1]:
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
        
        if self.radius - 1 <= H <= self.radius and d1 < l.length and d2 < l.length:
            return True
        else:
            return False
    
    def bounce(self, l):
        self.angle = l.angle / 2 + self.angle
    
    def update(self):
        for l in lines:
            if self.collide(l):
                self.bounce(l)
        
        self.center[0] += sin(self.angle) * self.vel
        self.center[1] -= cos(self.angle) * self.vel
        
        if not ((-10 < self.center[0] < WIN_SIZE[0] + 10) and (-10 < self.center[1] < WIN_SIZE[1] + 10)):
            balls.remove(self)


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
            
            if event.button == 1:
                p1 = mouse_pos
                if p2 is not None:
                    lines.append(Line(p1, p2))
                    p1 = p2 = None
               
            elif event.button == 3:
                p2 = mouse_pos
                if p1 is not None:
                    lines.append(Line(p1, p2))
                    p1 = p2 = None
            
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    if keys[pygame.K_SPACE] and key_timer <= 0:
        balls.append(Ball(mouse_pos))
        p1 = p2 = None
        key_timer = 300
    
    win.fill('black')
    
    for l in lines:
        pygame.draw.line(win, 'white', l.pos1, l.pos2, 4)
    
    if p1 is not None:
        pygame.draw.line(win, 'gray', p1, mouse_pos, 3)
    elif p2 is not None:
        pygame.draw.line(win, 'gray', p2, mouse_pos, 3)
    
    for b in balls:
        b.update()
        pygame.draw.circle(win, 'red', b.center, b.radius)
    
    pygame.display.flip()
