import numpy as np, pygame, pymunk, sys, os
import tkinter as tk # tkinter for name input only
from tkinter import *
from tkinter import ttk
#Libraries. Pymunk for physics engine to save time
# i did not add graphiclly designed sprites but feel free to do so py -m PyInstaller myfile.py
###########################################
#TO DO: get rid of magic numbers, add highscore
###########################################

name = None # used for saving highscores
hasEntered = False
gameOver = False
# CONSTANTS
WIDTH = 570
HEIGHT = 770
BACKGROUND = (25, 255, 55)
PADDING = (24, 160)
FRUIT_COLORS = ["cherry.png","berry.png", "grape.png", "dekopon.png", "orange.png", "apple.png", "pear.png", "plum.png", "pineapple.png", "melon.png", "watermelon.png"] #all are images under the public domain on wikimedia commonss
FRUIT_RADIUS = [17, 25, 32, 38, 50, 63, 75, 87, 100, 115, 135] # Multiple by 2 to get the dimensons (width and height) of images. 
WALL_THICKNESS = 14
rng = np.random.default_rng() # numpy has a better random number generator

menusSel = [True, False, False] # Main, highscore, game
highscores = dict() # dict
def GETFNAME(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_hscore(): # render highscore screen
    screen.fill((5, 70, 70))
    global menusSel
    pygame.display.update()
    mainClock.tick(60)
    menusSel = [False, False, True]
    while menusSel[2]:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
    
def getHs():
    with open(GETFNAME("highscores.txt")) as hs: # format str "Name, Highscore"
        for line in hs:
            dat = line.split()
            highscores[dat[0]] = dat[1]
def gentri(n): # triangular numbers. I made a function because why not? Math is cool
    for i in range(n, n + 1):
        return (i ** 2 + i)//2
def writeScore(score, player):
    f = open(GETFNAME("highscores.txt")) # tuples
class Game():
    def __init__(self, name):
        self.name = name 
        self.score = 0
    def gameOver(self):
        return
    def evalScore(self, score):
        if score > highscores[self.name]:
            highscores[self.name] = score
    def drawscoreBanner(self): # when game over
        return
    def backToMenu(self):
        loadMenu()
    def init(self): #draw the game
        menusSel[2] = True
        showGame()
def showGame():
    space = pymunk.Space()
    
    PAD = (24, 160)
    A = (PAD[0], PAD[1])
    B = (PAD[0], HEIGHT - PAD[0]-20)
    C = (WIDTH - PAD[0], HEIGHT - PAD[0])
    D = (WIDTH - PAD[0], PAD[1])
    scoreFont = pygame.font.SysFont("Monospace", 32)
    overfont = pygame.font.SysFont("Monospace", 62)
    pygame.display.update()
    space.gravity = (0, pys.gravity)
    space.damping = pys.dampining
    space.collision_bias = pys.bias
    pad = 20
    left = Border(A, B, space, 30)
    bottom = Border((PAD[0], HEIGHT - PAD[0]-70), (WIDTH - PAD[0], HEIGHT - PAD[0]-70), space, 30)
    right = Border(C, D, space, 30)
    walls = [left, bottom, right]
    wait_for_next = 240
    next_particle = GhostFruit(WIDTH//2, rng.integers(0, 5))
    particles = []

# Collision Handler
    handler = space.add_collision_handler(1, 1)
    handler.begin = collide
    handler.data["mapper"] = shape_to_fruit
    handler.data["particles"] = particles
    handler.data["score"] = 0
    while menusSel[2]:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    particles.append(next_particle.drop(space, shape_to_fruit))
                    wait_for_next = 240

            elif event.type == MOUSEBUTTONDOWN and wait_for_next == 0:
                particles.append(next_particle.drop(space, shape_to_fruit))
                wait_for_next = 240
        next_particle.set_x(pygame.mouse.get_pos()[0])
        if wait_for_next > 1:
            wait_for_next-=1
        elif wait_for_next == 1:
            next_particle = GhostFruit(next_particle.x, rng.integers(0, 5))
            wait_for_next-=1
        screen.fill((10, 170, 120))

        if wait_for_next == 0:
            next_particle.draw(screen)
        for x in walls:
            x.draw(screen)
        for y in particles:
            y.draw(screen)
            if y.pos[1] < PAD[1] and y.has_collided:
                label = overfont.render("Game Over!", 1, (0, 10, 0))
                screen.blit(label, pad)
                gameOver = True
        label = scoreFont.render(f"Score: {handler.data['score']}", 1, (0, 0, 255))
        screen.blit(label, (10, 10))
        space.step(1/240)
        pygame.display.update()
        mainClock.tick(240)



                
shape_to_fruit = dict()

def collide(arbiter, space, data): # DETERMINES IF COLLIDES
    sh1, sh2 = arbiter.shapes
    _mapper = data["mapper"]
    pa1 = _mapper[sh1]
    pa2 = _mapper[sh2]
    cond = bool(pa1.n != pa2.n)
    pa1.has_collided = cond
    pa2.has_collided = cond
    if not cond:
        new_particle = onCollision(pa1, pa2, space, data["particles"], _mapper)
        data["particles"].append(new_particle)
        data["score"] += pys.points[pa1.n]
    
    return cond
class Physics(): #physics related constants. Ideally a data structure would work, however python lacks them, so i went for a class
    def __init__(self):
        self.density = 0.001
        self.elast = 0.01
        self.impulse = 100
        self.gravity = 20000
        self.dampining = 0.8
        self.delay = 240
        self.nextSteps = 20
        self.bias =  .00001
        self.points = [gentri(z) for z in range(1,11)]


class Fruit(): # manage all physical properties of the fruit here
    def __init__(self, pos, n, space, mapper):
        self.n = n % 11 # get the type of fruit as int
        self.radius = FRUIT_RADIUS[self.n] * 1.5
        self.phyBod = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.phyBod.position = tuple(pos)
        self.shape = pymunk.Circle(body=self.phyBod, radius=self.radius/3) # apply the physics of a circle
        self.shape.density = pys.density
        self.shape.elast = pys.elast
        self.shape.collision_type = 1
        self.shape.friction = 0.2
        self.has_collided = False 
        mapper[self.shape] = self
        # create a physical space
        space.add(self.phyBod, self.shape)
        self.alive = True
    def draw(self, screen):
        if self.alive:
            image = pygame.transform.scale(pygame.image.load(GETFNAME(FRUIT_COLORS[self.n])), (self.radius, self.radius)) # we dont actully use a color, im using real images of fruit 
            screen.blit(image, self.phyBod.position)
    def kill(self, space):
        space.remove(self.phyBod, self.shape)
        self.alive = False
    @property
    def pos(self): # retrive an array we can easily work with
        return np.array(self.phyBod.position)

class GhostFruit():
    def __init__(self, x, n):
        self.n = n % 11 # what fruit?
        self.radius = FRUIT_RADIUS[self.n]
        self.x = x
    def draw(self, screen):
        image = pygame.transform.scale(pygame.image.load(GETFNAME(FRUIT_COLORS[self.n])), (self.radius, self.radius)) # we dont actully use a color, im using real images of fruit 
        screen.blit(image, (self.x, 30))
    def set_x(self, x):
        lim = (self.radius + WALL_THICKNESS // 2)+30
        self.x = np.clip(x, lim, WIDTH - lim)
    def drop(self, space, mapper):
        return Fruit((self.x, PADDING[1]//2),self.n, space, mapper)

class Border():
    def __init__(self, a, b, space, offset):
        self.a = a
        self.b = b
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (a[0], a[1]-offset), (b[0], b[1]-offset), WALL_THICKNESS // 2)
        self.shape.friction = 6
        space.add(self.body, self.shape)
    def draw(self, screen):
        pygame.draw.line(screen, 'green', self.a, self.b, WALL_THICKNESS)

def onCollision(fruit1, fruit2, space, fruits, mapper): # handle collision
    if fruit1.n == fruit2.n:
        dist = np.linalg.norm(fruit1.pos - fruit2.pos)
        if dist < (2 * fruit1.radius):
            fruit1.kill(space)
            fruit2.kill(space)
            newp = Fruit(np.mean([fruit1.pos, fruit2.pos+30], axis=0), fruit1.n+1, space, mapper)
            for f in fruits:
                if f.alive:
                    vector = f.pos - newp.pos
                    dist = np.linalg.norm(vector)
                    if dist < newp.radius + f.radius:
                        impulse = pys.impulse * vector / (dist ** 2)
                        f.phyBod.apply_impulse_at_local_point(tuple(impulse))
            return newp
    return None
def loadMenu():
    click = False
    global hasEntered
    while menusSel[0]:
        if hasEntered:
            break
        screen.fill((200,200,222))
        draw_text('Main Menu - Suika Clone', font, (25,255,10), screen, 200, 40)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(200, 100, 200, 50)
        button_2 = pygame.Rect(200, 180, 200, 50)
        button_3 = pygame.Rect(200, 260, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                newGame()
                menusSel[0] = False
        if button_2.collidepoint((mx, my)):
            if click:
                load_hscore()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, (25, 222, 50), button_1)
        pygame.draw.rect(screen, (25, 222, 50), button_2)
        pygame.draw.rect(screen, (25, 222, 50), button_3)

 
        #writing text on top of button
        draw_text('PLAY', font, (255,255,255), screen, 270, 115)
        draw_text('HIGHSCORES', font, (255,255,255), screen, 250, 195)
        draw_text('QUIT GAME', font, (255,255,255), screen, 230, 275)


    # draw images  
        myimage = pygame.image.load(GETFNAME('watermelon.png'))
        myimage = pygame.transform.scale(myimage, (128, 120))
        imagerect = myimage.get_rect()

        myimage1 = pygame.image.load(GETFNAME('melon.png'))
        myimage1 = pygame.transform.scale(myimage, (128, 120))
        imagerect1 = myimage.get_rect()
        screen.blit(myimage, imagerect)
        screen.blit(myimage1, (470, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)
 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
def newGame():
    prompt = Tk()
    prompt.geometry("180x100+3+3")
    prompt.eval('tk::PlaceWindow . center')

    prompt.title("Enter a name")
    e = Entry(prompt)
    b = Button(prompt, text="Submit", command=lambda:onNameEnter(prompt, e))
    e.pack()
    b.pack()
    e.focus_set()
    prompt.mainloop()
def onNameEnter(prompt, e):
    global hasEntered, name
    name = str(e.get())
    prompt.destroy()
    hasEntered = True
    game = Game(name)
    game.init()

if __name__ == '__main__':
# init pygame
    pys = Physics()
    mainClock = pygame.time.Clock()
    from pygame.locals import *
    pygame.init()
    pygame.display.set_caption('Suika Clone! - Non Commerical')
    screen = pygame.display.set_mode((600, 700),0,32)
    font = pygame.font.SysFont(None, 30)
    getHs()
    loadMenu()
