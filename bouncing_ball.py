
from sys import exit
from math import sqrt, cos, sin, acos, pi, radians
import pygame


WIN_SIZE = (700, 500)
G = 0.01

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
        self.bouncy = 100
        self.line = None
    
    def collide(self, l):
        d1 = distance(self.center, l.pos1)
        d2 = distance(self.center, l.pos2)
        
        P = (d1 + d2 + l.length) / 2
        A = sqrt(P * (P - d1) * (P - d2) * (P - l.length))
        H = (2 * A) / l.length
        
        if H <= self.radius and d1 < l.length and d2 < l.length:
            self.line = l
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
        self.vel *= self.bouncy / 100
    
    def bounce_ball(self, b):
        b_angle = b.angle
        b.angle = self.angle
        self.angle = b_angle
        self.vel *= self.bouncy / 100
    
    def update(self):
        while self.angle > pi:
            self.angle -= 2*pi
        while self.angle < -pi:
            self.angle += 2*pi
        
        for l in lines:
            if l != self.line:
                if self.collide(l):
                    self.bounce(l)
            if not self.collide(l):
                self.line = []
        for b in balls:
            if b != self:
                if self.collide_ball(b):
                    self.bounce_ball(b)
                    
        movement = [self.center[0] + sin(self.angle) * self.vel, self.center[1] - cos(self.angle) * self.vel]
        if Gravity:
            movementG = [movement[0], movement[1] + G]
            future_pos = distance(self.center, movementG)
            cos_angleG = (distance(self.center, movement)**2 + future_pos**2 - G**2) / (2 * distance(self.center, movement) * future_pos)
            if cos_angleG > 1:
                cos_angleG = 1
            if self.angle > 0:
                self.angle += acos(cos_angleG)
            elif self.angle < 0:
                self.angle -= acos(cos_angleG)
            self.vel = future_pos
            movement = movementG
        
        self.center = movement
        
        if not ((-10 < self.center[0] < WIN_SIZE[0] + 10) and (-10 < self.center[1] < WIN_SIZE[1] + 10)):
            balls.remove(self)
            
class Slider():
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.width = 110
        self.height = 10
    
    def update(self):
        if self.y - 10 < mouse_pos[1] < self.y + 10 and self.x + self.width > mouse_pos[0] > self.x:
            self.state = mouse_pos[0] - self.x
            
    def render(self):
        pygame.draw.rect(win, "grey", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, "darkgrey", (self.x + self.state, self.y - 10, 10, 30))
        
class Spawner():
    def __init__(self, pos):
        self.pos = pos
        self.spawnrate = 2000
        self.timer = 0
        
    def update(self):
        self.timer += dt
        if self.timer >= self.spawnrate:
            balls.append(Ball(self.pos))
            self.timer = 0
    
    def render(self):
        pygame.draw.rect(win, "grey", (self.pos[0] - 10, self.pos[1] - 10, 20, 20))

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

def add_spawner():
    global p1
    spawners.append(Spawner(mouse_pos))
    p1 = None

p1 = p2 = None

lines = []
balls = []
sliders = []
spawners = []

Menu = False
Gravity = False
key_timer = 0

sliders.append(Slider(580, 20, 100))
sliders.append(Slider(580, 60, 40))


while True:
    dt = clock.tick(60)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()
        
    if keys[pygame.K_a]:
        Menu = not Menu
        pygame.time.wait(100)
    
    if keys[pygame.K_g]:
        Gravity = not Gravity
        pygame.time.wait(100)
    
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
    
    # place a new spawner
    if keys[pygame.K_z] and key_timer <= 0:
        add_spawner()
        key_timer = 300
    
    # remove the last spawner placed
    if keys[pygame.K_e] and key_timer <= 0:
        spawners.pop(-1)
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
        b.bouncy = sliders[0].state
        b.radius = (sliders[1].state/10) + 4
        b.update()
        pygame.draw.circle(win, 'white', b.center, b.radius)
        
    for s in spawners:
        s.update()
        s.render()
    
    if Menu:
        for s in sliders:
            s.update()
            s.render()
    if Gravity:
        pygame.draw.rect(win, "green", (0, 0, 40, 40))
    
    pygame.display.flip()
