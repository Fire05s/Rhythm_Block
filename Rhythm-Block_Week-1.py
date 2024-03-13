import pygame,random,time,math
pygame.init ()
from pygame.locals import *
screen = pygame.display.set_mode ((800,800))
pygame.display.set_caption ('Rhythm Block the Game')

screen.fill ((240,240,240))
clock = pygame.time.Clock ()

'''
Errors:
    Lifesteal Points - After Level 1 Lifesteal, self.reward (at least the one added to score) no longer goes up
    Victory - Next Wave,Retry,Main Menu - after winning first time, next wave - doesn't go to next wave + auto-wins; retry - auto-wins; main menu - stays at same wave
        + auto-wins
    Armored I double lives - Cannot kill the Armored I despite absorbing a laser
To-Do:
    2/10 Waves
    Endless Mode
    Shop - Use Score Points (Coins if time) - create utility
    More enemies - Ideas: zig-zag,ranged,feigner
'''

#Variables
bcolor = (240,240,240)
white = (255,255,255)
black = (0,0,0)
tx = -300
ty = 370
skipshow = True
skipt = False
wave = 0
wenemies = 0
enemies1 = []
enemies2 = []
enemies3 = []
enemies4 = []
lives = 3
losec = False
winc = False
score = 0.00
rx = 430
ry = 398.5
ux = 398.5
uy = 350
lx = 350
ly = 398.5
dx = 398.5
dy = 430
rfire = False
ufire = False
lfire = False
dfire = False
lmove = 1
lrange = 20
lccond = False
lcounter = 0
ccond = False
counter = 0 #Approx. 200 ticks = 1 second
wcomplete = [False,False,False,False,False,False,False,False,False,False,False]

#Larger text function
def title (msg,x1,y1,msgcol):
    fontobj = pygame.font.SysFont ('Times New Roman',20)
    msgobj = fontobj.render (msg,False,msgcol)
    screen.blit (msgobj,(x1,y1))
#Smaller text function
def subtext (msg,x1,y1,msgcol):
    fontobj = pygame.font.SysFont ('Times New Roman',17)
    msgobj = fontobj.render (msg,False,msgcol)
    screen.blit (msgobj,(x1,y1))

#Animated introduction to tutorial
def intro ():
    global tx,ty
    for loop in range (1,114,1):
        clock.tick (60)
        screen.fill (bcolor)
        title ('Welcome to Rythm Block the Game!',tx,ty,black)
        tx = tx + 5
        pygame.display.update ()
    screen.fill (bcolor)
    title ('Welcome to Rythm Block the Game!',240,370,black)
    time.sleep (1)
    for loop in range (1,115,1):
        clock.tick (60)
        screen.fill (bcolor)
        title ('Welcome to Rythm Block the Game!',tx,ty,black)
        tx = tx + 5
        pygame.display.update ()
    time.sleep (1)

#Shows center, player square
def player ():
    pygame.draw.rect (screen,(70,120,255),(350,350,100,100))
    pygame.draw.rect (screen,black,(350,350,100,100),2)

#Shows 4 lanes for enemies
def lanes ():
    pygame.draw.line (screen,(100,100,100),(500,400),(775,400),2) #Lane 1
    pygame.draw.line (screen,(100,100,100),(400,25),(400,300),2) #Lane 2
    pygame.draw.line (screen,(100,100,100),(25,400),(300,400),2) #Lane 3
    pygame.draw.line (screen,(100,100,100),(400,500),(400,775),2) #Lane 4

#Shows player and lanes
def refresh ():
    screen.fill (bcolor)
    player ()
    lanes ()

class enemy:
    def __init__ (self,lane,etype,multi):
        self.lane = lane
        self.movex = 0
        self.movey = 0
        self.type = etype
        self.lifesteal = 0
        self.reward = 0
        self.multiplier = multi
        self.life = 1
#Position of enemy
        if self.lane == 1:
            self.x = 850 + round (random.uniform (0,100),2)
            self.y = 347 + round (random.uniform (0,31),2)
        if self.lane == 2:
            self.x = 347 + round (random.uniform (0,31),2)
            self.y = -50 + round (random.uniform (-100,0),2)
        if self.lane == 3:
            self.x = -50 + round (random.uniform (-100,0),2)
            self.y = 347 + round (random.uniform (0,31),2)
        if self.lane == 4:
            self.x = 347 + round (random.uniform (0,31),2)
            self.y = 850 + round (random.uniform (0,100),2)
#Movement speed based on types of enemies
        if self.type == 'basic':
            if self.lane == 1:
                self.movex = round (-random.uniform (0.3,0.7),2)
            if self.lane == 2:
                self.movey = round (random.uniform (0.3,0.7),2)
            if self.lane == 3:
                self.movex = round (random.uniform (0.3,0.7),2)
            if self.lane == 4:
                self.movey = round (-random.uniform (0.3,0.7),2)
        if self.type == 'armored1':
            if self.lane == 1:
                self.movex = round (-random.uniform (0.2,0.6),2)
            if self.lane == 2:
                self.movey = round (random.uniform (0.2,0.6),2)
            if self.lane == 3:
                self.movex = round (random.uniform (0.2,0.6),2)
            if self.lane == 4:
                self.movey = round (-random.uniform (0.2,0.6),2)
    def display (self):
        global lives,losec
        self.x = self.x + self.movex
        self.y = self.y + self.movey
#Stats and displays based on types of enemies
        if self.type == 'basic':
            pygame.draw.rect (screen,(255,45,75),(math.ceil (self.x),math.ceil (self.y),75,75))
            pygame.draw.rect (screen,(200,200,200),(math.ceil (self.x),math.ceil (self.y),75,75),1)
            self.reward = 10.0
            if 275 <= self.x <= 450 and 275 <= self.y <= 450:
                self.lifesteal = self.lifesteal + 1
                lives = lives - 1
    #Lifesteal Buffs I (Just for Basic Enemies)
                if self.lane == 1:
                    self.movex = self.movex - 0.2
                    self.x = 850 + round (random.uniform (0,100),2)
                    self.y = 347 + round (random.uniform (0,31),2)
                if self.lane == 2:
                    self.movey = self.movey + 0.2
                    self.x = 347 + round (random.uniform (0,31),2)
                    self.y = -50 + round (random.uniform (-100,0),2)
                if self.lane == 3:
                    self.movex = self.movex + 0.2
                    self.x = -50 + round (random.uniform (-100,0),2)
                    self.y = 347 + round (random.uniform (0,31),2)
                if self.lane == 4:
                    self.movey = self.movey - 0.2
                    self.x = 347 + round (random.uniform (0,31),2)
                    self.y = 850 + round (random.uniform (0,100),2)
        if self.type == 'armored1':
            pygame.draw.rect (screen,(255,45,75),(math.ceil (self.x),math.ceil (self.y),85,85))
            pygame.draw.rect (screen,(150,150,150),(math.ceil (self.x),math.ceil (self.y),85,85),1)
            self.reward = 15.0
            self.life = 2
            if 265 <= self.x <= 450 and 265 <= self.y <= 450:
                self.lifesteal = self.lifesteal + 1
                lives = lives - 1
                if self.lane == 1:
                    self.movex = self.movex - 0.2
                    self.x = 850 + round (random.uniform (0,110),2)
                    self.y = 347 + round (random.uniform (0,31),2)
                if self.lane == 2:
                    self.movey = self.movey + 0.2
                    self.x = 347 + round (random.uniform (0,31),2)
                    self.y = -50 + round (random.uniform (-110,0),2)
                if self.lane == 3:
                    self.movex = self.movex + 0.2
                    self.x = -50 + round (random.uniform (-110,0),2)
                    self.y = 347 + round (random.uniform (0,31),2)
                if self.lane == 4:
                    self.movey = self.movey - 0.2
                    self.x = 347 + round (random.uniform (0,31),2)
                    self.y = 850 + round (random.uniform (0,110),2)
#Losing Condition
        if lives <= 0:
            losec = True
#Lifesteal Buffs II
        if self.type == 'basic':
            if self.lifesteal == 1:
                pygame.draw.circle (screen,(165,42,42),(math.ceil (self.x+37),math.ceil (self.y+38)),20)
                self.reward = self.reward * self.multiplier
                #print (self.reward) #Only this seems to work
            if self.lifesteal == 2:
                pygame.draw.circle (screen,(165,42,42),(math.ceil (self.x+37),math.ceil (self.y+38)),20)
                pygame.draw.line (screen,(150,150,150),(math.ceil (self.x+37),math.ceil (self.y+10)),(math.ceil (self.x+37),math.ceil (self.y+65)),3)
                pygame.draw.line (screen,(150,150,150),(math.ceil (self.x+10),math.ceil (self.y+38)),(math.ceil (self.x+65),math.ceil (self.y+38)),3)
                self.reward = self.reward * self.multiplier
                #print (self.reward)
            if self.lifesteal >= 3:
                pygame.draw.circle (screen,(165,42,42),(math.ceil (self.x+37),math.ceil (self.y+38)),20)
                pygame.draw.line (screen,(150,150,150),(math.ceil (self.x+37),math.ceil (self.y+10)),(math.ceil (self.x+37),math.ceil (self.y+65)),3)
                pygame.draw.line (screen,(150,150,150),(math.ceil (self.x+10),math.ceil (self.y+38)),(math.ceil (self.x+65),math.ceil (self.y+38)),3)
                pygame.draw.circle (screen,(255,215,0),(math.ceil (self.x+37),math.ceil (self.y+38)),5)
                self.reward = self.reward * self.multiplier
                #print (self.reward)
        if self.type == 'armored1':
            if self.lifesteal == 1:
                pygame.draw.circle (screen,(165,42,42),(math.ceil (self.x+42),math.ceil (self.y+43)),30)
                self.reward = self.reward * self.multiplier
                #print (self.reward) #Only this seems to work
            if self.lifesteal == 2:
                pygame.draw.circle (screen,(165,42,42),(math.ceil (self.x+42),math.ceil (self.y+43)),30)
                pygame.draw.line (screen,(150,150,150),(math.ceil (self.x+42),math.ceil (self.y+10)),(math.ceil (self.x+42),math.ceil (self.y+75)),3)
                pygame.draw.line (screen,(150,150,150),(math.ceil (self.x+10),math.ceil (self.y+43)),(math.ceil (self.x+75),math.ceil (self.y+43)),3)
                self.reward = self.reward * self.multiplier
                #print (self.reward)
            if self.lifesteal >= 3:
                pygame.draw.circle (screen,(165,42,42),(math.ceil (self.x+42),math.ceil (self.y+43)),30)
                pygame.draw.line (screen,(150,150,150),(math.ceil (self.x+42),math.ceil (self.y+10)),(math.ceil (self.x+42),math.ceil (self.y+75)),3)
                pygame.draw.line (screen,(150,150,150),(math.ceil (self.x+10),math.ceil (self.y+43)),(math.ceil (self.x+75),math.ceil (self.y+43)),3)
                pygame.draw.circle (screen,(255,215,0),(math.ceil (self.x+42),math.ceil (self.y+43)),10)
                self.reward = self.reward * self.multiplier
                #print (self.reward)


#Shows scoreboard stats
def scoreboard ():
    global score,wenemies,wave,lives
    subtext ('Score: ' + str (round (score,2)),700,0,(255,215,0))
    subtext ('Enemies Incoming: ',612,20,black)
    title (str (wenemies),750,19,(255,0,0))
    subtext ('Wave # ' + str (wave),0,0,black)
    subtext ('Lives: ',0,20,black)
    title (str (lives),47,19,(0,255,0))

#Creates a certain number of enemies in random lanes
def ecreate (num = 1,etype = 'basic',multi = 1.5):
    for loop in range (0,num,1):
        lane = random.randint (1,4)
        if lane == 1:
            enemies1.append (enemy (lane,etype,multi))
        if lane == 2:
            enemies2.append (enemy (lane,etype,multi))
        if lane == 3:
            enemies3.append (enemy (lane,etype,multi))
        if lane == 4:
            enemies4.append (enemy (lane,etype,multi))

#Displays all enemies
def runenemies ():
    for loop in range (0,len (enemies1),1):
        enemies1 [loop].display ()
    for loop in range (0,len (enemies2),1):
        enemies2 [loop].display ()
    for loop in range (0,len (enemies3),1):
        enemies3 [loop].display ()
    for loop in range (0,len (enemies4),1):
        enemies4 [loop].display ()

#Lasers/Projectiles Display
def rlaser ():
    global rfire,ufire,lfire,dfire
    pygame.draw.rect (screen,(50,150,255),(rx,ry,lrange,5))
    pygame.draw.rect (screen,(100,100,100),(rx,ry,lrange,5),1)
    rfire = True
    ufire = False
    lfire = False
    dfire = False
def ulaser ():
    global rfire,ufire,lfire,dfire
    pygame.draw.rect (screen,(255,69,0),(ux,uy,5,lrange))
    pygame.draw.rect (screen,(100,100,100),(ux,uy,5,lrange),1)
    ufire = True
    rfire = False
    lfire = False
    dfire = False
def llaser ():
    global rfire,ufire,lfire,dfire
    pygame.draw.rect (screen,(50,150,255),(lx,ly,lrange,5))
    pygame.draw.rect (screen,(100,100,100),(lx,ly,lrange,5),1)
    lfire = True
    rfire = False
    ufire = False
    dfire = False
def dlaser ():
    global rfire,ufire,lfire,dfire
    pygame.draw.rect (screen,(255,69,0),(dx,dy,5,lrange))
    pygame.draw.rect (screen,(100,100,100),(dx,dy,5,lrange),1)
    dfire = True
    rfire = False
    ufire = False
    lfire = False

#Shot Charges and Bar Animation
def lcharge (sec = 1):
    global rfire,ufire,lfire,dfire,lccond,lcounter
    time = sec * 200
    subtext ('Cooldown',660,780,(100,100,100))
    if lcounter == 0:
#3/3 Finished, shows 3 parts full - "Laser" is charged
        pygame.draw.rect (screen,(255,0,255),(735,779,20,20))
        pygame.draw.rect (screen,(255,0,255),(755,779,20,20))
        pygame.draw.rect (screen,(255,0,255),(775,779,20,20))
        pygame.draw.rect (screen,black,(735,779,20,20),1)
        pygame.draw.rect (screen,black,(755,779,20,20),1)
        pygame.draw.rect (screen,black,(775,779,20,20),1)
    elif round (time*2/3) <= lcounter <= time:
#2/3 Finished, shows 2 parts full
        pygame.draw.rect (screen,(255,0,255),(735,779,20,20))
        pygame.draw.rect (screen,(255,0,255),(755,779,20,20))
        pygame.draw.rect (screen,black,(735,779,20,20),1)
        pygame.draw.rect (screen,black,(755,779,20,20),1)
        pygame.draw.rect (screen,black,(775,779,20,20),1)
    elif round (time*1/3) <= lcounter < round (time*2/3):
#1/3 Finished, shows 1 part full
        pygame.draw.rect (screen,(255,0,255),(735,779,20,20))
        pygame.draw.rect (screen,black,(735,779,20,20),1)
        pygame.draw.rect (screen,black,(755,779,20,20),1)
        pygame.draw.rect (screen,black,(775,779,20,20),1)
    elif 0 < lcounter < round (time*1/3):
        pygame.draw.rect (screen,black,(735,779,20,20),1)
        pygame.draw.rect (screen,black,(755,779,20,20),1)
        pygame.draw.rect (screen,black,(775,779,20,20),1)
    for event in pygame.event.get ():
        if event.type == KEYDOWN:
            if (event.key == K_RIGHT or event.key == K_d) and ufire == False and lfire == False and dfire == False:
                if lcounter == 0:
                    rlaser ()
            if (event.key == K_UP or event.key == K_w) and rfire == False and lfire == False and dfire == False:
                if lcounter == 0:
                    ulaser ()
            if (event.key == K_LEFT or event.key == K_a) and rfire == False and ufire == False and dfire == False:
                if lcounter == 0:
                    llaser ()
            if (event.key == K_DOWN or event.key == K_s) and rfire == False and ufire == False and lfire == False:
                if lcounter == 0:
                    dlaser ()
    if lccond == True:
        subtext ('Miss!',610,780,(255,0,0))
        lcounter = lcounter + 1
        if lcounter == time:
            lcounter = 0
            lccond = False

#Laser Animation and Hit Conditions
def lanim (num = 2,etype = 'basic',multi = 1.5):
    global rx,ry,ux,uy,lx,ly,dx,dy,lmove,lrange,rfire,ufire,lfire,dfire,wenemies,winc,ccond,counter,lccond,score
    if ccond == True:
        counter = counter + 1
        if counter == 200:
            winc = True
            counter = 0
    if rfire == True:
        rlaser ()
        rx = rx + lmove
        for loop in enemies1:
            if loop.x <= rx + lrange:
                if loop.type == 'basic':
                    enemies1.remove (loop)
                    score = score + loop.reward
                    if wenemies == 0 and len (enemies1) == 0 and len (enemies2) == 0 and len (enemies3) == 0 and len (enemies4) == 0:
                        ccond = True
                    elif wenemies == 1:
                        ecreate (1,etype,multi)
                        wenemies = wenemies - 1
                    elif wenemies >= 2:
                        ecreate (num,etype,multi)
                        wenemies = wenemies - num
                    rfire = False
                if loop.type == 'armored1':
                    loop.life = loop.life - 1
                    if loop.life == 0:
                        enemies1.remove (loop)
                        score = score + loop.reward
                        if wenemies == 0 and len (enemies1) == 0 and len (enemies2) == 0 and len (enemies3) == 0 and len (enemies4) == 0:
                            ccond = True
                    rfire = False
        if rx >= 480:
            rfire = False
            lccond = True
            rx = 430
            ry = 398.5
            ux = 398.5
            uy = 350
            lx = 350
            ly = 398.5
            dx = 398.5
            dy = 430
    if ufire == True:
        ulaser ()
        uy = uy - lmove
        for loop in enemies2:
            if loop.y + 75 >= uy:
                if loop.type == 'basic':
                    enemies2.remove (loop)
                    score = score + loop.reward
                    if wenemies == 0 and len (enemies1) == 0 and len (enemies2) == 0 and len (enemies3) == 0 and len (enemies4) == 0:
                        ccond = True
                    elif wenemies == 1:
                        ecreate (1,etype,multi)
                        wenemies = wenemies - 1
                    elif wenemies >= 2:
                        ecreate (num,etype,multi)
                        wenemies = wenemies - num
                    ufire = False
                if loop.type == 'armored1':
                    loop.life = loop.life - 1
                    if loop.life == 0:
                        enemies2.remove (loop)
                        score = score + loop.reward
                        if wenemies == 0 and len (enemies1) == 0 and len (enemies2) == 0 and len (enemies3) == 0 and len (enemies4) == 0:
                            ccond = True
                    ufire = False
        if uy <= 300:
            ufire = False
            lccond = True
            rx = 430
            ry = 398.5
            ux = 398.5
            uy = 350
            lx = 350
            ly = 398.5
            dx = 398.5
            dy = 430
    if lfire == True:
        llaser ()
        lx = lx - lmove
        for loop in enemies3:
            if loop.x + 75 >= lx:
                if loop.type == 'basic':
                    enemies3.remove (loop)
                    score = score + loop.reward
                    if wenemies == 0 and len (enemies1) == 0 and len (enemies2) == 0 and len (enemies3) == 0 and len (enemies4) == 0:
                        ccond = True
                    elif wenemies == 1:
                        ecreate (1,etype,multi)
                        wenemies = wenemies - 1
                    elif wenemies >= 2:
                        ecreate (num,etype,multi)
                        wenemies = wenemies - num
                    lfire = False
                if loop.type == 'armored1':
                    loop.life = loop.life - 1
                    if loop.life == 0:
                        enemies3.remove (loop)
                        score = score + loop.reward
                        if wenemies == 0 and len (enemies1) == 0 and len (enemies2) == 0 and len (enemies3) == 0 and len (enemies4) == 0:
                            ccond = True
                    lfire = False
        if lx <= 300:
            lfire = False
            lccond = True
            rx = 430
            ry = 398.5
            ux = 398.5
            uy = 350
            lx = 350
            ly = 398.5
            dx = 398.5
            dy = 430
    if dfire == True:
        dlaser ()
        dy = dy + lmove
        for loop in enemies4:
            if loop.y <= dy + lrange:
                if loop.type == 'basic':
                    enemies4.remove (loop)
                    score = score + loop.reward
                    if wenemies == 0 and len (enemies1) == 0 and len (enemies2) == 0 and len (enemies3) == 0 and len (enemies4) == 0:
                        ccond = True
                    elif wenemies == 1:
                        ecreate (1,etype,multi)
                        wenemies = wenemies - 1
                    elif wenemies >= 2:
                        ecreate (num,etype,multi)
                        wenemies = wenemies - num
                    dfire = False
                if loop.type == 'armored1':
                    loop.life = loop.life - 1
                    if loop.life == 0:
                        enemies4.remove (loop)
                        score = score + loop.reward
                        if wenemies == 0 and len (enemies1) == 0 and len (enemies2) == 0 and len (enemies3) == 0 and len (enemies4) == 0:
                            ccond = True
                    dfire = False
        if dy >= 480:
            dfire = False
            lccond = True
            rx = 430
            ry = 398.5
            ux = 398.5
            uy = 350
            lx = 350
            ly = 398.5
            dx = 398.5
            dy = 430

#Main Menu Display and Buttons as a Fruitful Function
def menu ():
    global confirm
    confirm = True
    screen.fill (bcolor)
    pygame.draw.rect (screen,black,(125,350,200,50),2)
    pygame.draw.rect (screen,black,(475,350,200,50),2)
    pygame.draw.rect (screen,black,(0,770,100,30),2)
    pygame.draw.rect (screen,black,(700,770,100,30),2)
    title ('Wave Mode',175,364,black)
    title ('Endless Mode',520,364,black)
    subtext ('Settings',23,775,black)
    subtext ('Quit',735,775,black)
    pygame.display.update ()
    for event in pygame.event.get ():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx,my = event.pos
            if 125 <= mx <= 325 and 350 <= my <= 400:
                while confirm == True:
                    screen.fill (bcolor)
                    pygame.draw.rect (screen,(0,255,0),(300,350,200,30))
                    pygame.draw.rect (screen,black,(300,350,200,30),2)
                    pygame.draw.rect (screen,(255,0,0),(387.5,425,25,25))
                    pygame.draw.rect (screen,black,(387.5,425,25,25),2)
                    pygame.draw.line (screen,black,(387.5,425),(412.5,450),2)
                    pygame.draw.line (screen,black,(412.5,425),(387.5,450),2)
                    title ('Confirm Wave Mode?',312,353,black)
                    pygame.display.update ()
                    for event in pygame.event.get ():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mx,my = event.pos
                            if 300 <= mx <= 500 and 350 <= my <= 380:
                                return 1
                            elif 387.5 <= mx <= 412.5 and 425 <= my <= 450:
                                confirm = False
            elif 475 <= mx <= 675 and 350 <= my <= 400:
                while confirm == True:
                    screen.fill (bcolor)
                    pygame.draw.rect (screen,(0,255,0),(290,350,220,30))
                    pygame.draw.rect (screen,black,(290,350,220,30),2)
                    pygame.draw.rect (screen,(255,0,0),(387.5,425,25,25))
                    pygame.draw.rect (screen,black,(387.5,425,25,25),2)
                    pygame.draw.line (screen,black,(387.5,425),(412.5,450),2)
                    pygame.draw.line (screen,black,(412.5,425),(387.5,450),2)
                    title ('Confirm Endless Mode?',305,353,black)
                    pygame.display.update ()
                    for event in pygame.event.get ():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mx,my = event.pos
                            if 290 <= mx <= 510 and 350 <= my <= 380:
                                return 2
                            elif 387.5 <= mx <= 412.5 and 425 <= my <= 450:
                                confirm = False
            elif 0 <= mx <= 100 and 770 <= my <= 800:
                while confirm == True:
                    screen.fill (bcolor)
                    return 3
            elif 700 <= mx <= 800 and 770 <= my <= 800:
                while confirm == True:
                    screen.fill (bcolor)
                    pygame.draw.rect (screen,(0,255,0),(325,350,150,30))
                    pygame.draw.rect (screen,black,(325,350,150,30),2)
                    pygame.draw.rect (screen,(255,0,0),(387.5,425,25,25))
                    pygame.draw.rect (screen,black,(387.5,425,25,25),2)
                    pygame.draw.line (screen,black,(387.5,425),(412.5,450),2)
                    pygame.draw.line (screen,black,(412.5,425),(387.5,450),2)
                    title ('Confirm Quit?',344,353,black)
                    pygame.display.update ()
                    for event in pygame.event.get ():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mx,my = event.pos
                            if 325 <= mx <= 475 and 350 <= my <= 380:
                                pygame.quit ()
                                exit ()
                            elif 387.5 <= mx <= 412.5 and 425 <= my <= 450:
                                confirm = False

#Infocard + Button, use \n to denote new lines even for the screen
def icard (heading,message,symbol = 'i',x1 = 770,y1 = 80):
    pygame.draw.circle (screen,white,(x1,y1),25)
    pygame.draw.circle (screen,(150,150,150),(x1,y1),25,3)
    title (symbol,x1 - 2.5,y1 - 11,black)
    ishow = True
    for event in pygame.event.get ():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx,my = event.pos
            if x1 - 25 <= mx <= x1 + 25 and y1 - 25 <= my <= y1 + 25: #Delay?
                while ishow == True:
                    pygame.draw.polygon (screen,white,((200,300),(600,300),(600,570),(550,480),(550,500),(200,500)))
                    pygame.draw.polygon (screen,(150,150,150),((200,300),(600,300),(600,570),(550,480),(550,500),(200,500)),3)
                    pygame.draw.line (screen,(180,180,180),(205,325),(595,325),2)
                    title (heading,205,305,black)
                    message = message + '\n\n\n\n\n\n\n\n\n\n'
                    list1 = message.split ('\n')
                    subtext (list1[0],205,330,black) #11 lines of Possible Text
                    subtext (list1[1],205,345,black)
                    subtext (list1[2],205,360,black)
                    subtext (list1[3],205,375,black)
                    subtext (list1[4],205,390,black)
                    subtext (list1[5],205,405,black)
                    subtext (list1[6],205,420,black)
                    subtext (list1[7],205,435,black)
                    subtext (list1[8],205,450,black)
                    subtext (list1[9],205,465,black)
                    subtext (list1[10],205,480,black)
                    pygame.display.update ()
                    for event in pygame.event.get ():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mx,my = event.pos
                            if not (200 <= mx <= 600 and 300 <= my <= 570):
                                ishow = False
    ishow = True

#Resets the current wave the player was on
def retry (enemynum,num = 1,etype = 'basic',multi = 1.5,livesnum = 3):
    global confirm,winc,losec,wenemies,enemies1,enemies2,enemies3,enemies4,lives,score,save
    confirm = False
    winc = False
    losec = False
    enemies1 = []
    enemies2 = []
    enemies3 = []
    enemies4 = []
    ecreate (num,etype,multi)
    wenemies = enemynum
    lives = livesnum
    score = save

#Sends the player to the main menu
def mainmenu ():
    global confirm,winc,losec,wenemies,enemies1,enemies2,enemies3,enemies4,lives,score,save,wave,selection
    confirm = False
    winc = False
    losec = False
    enemies1 = []
    enemies2 = []
    enemies3 = []
    enemies4 = []
    wenemies = 0
    lives = 3
    score = save
    wave = 0
    selection = 0

#Skips the wave if they have already completed it (in their session)
def skip ():
    global wcomplete,wave
    for loop in range (0,len (wcomplete),1):
        if wcomplete [loop] == True:
            if wave == loop:
                pygame.draw.rect (screen,(0,255,0),(0,770,50,30))
                for event in pygame.event.get ():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx,my = event.pos
                        if 0 <= mx <= 50 and 770 <= my <= 800:
                            wave = wave + 1
                break
            else:
                pygame.draw.rect (screen,(255,0,0),(0,770,50,30))
        else:
            pygame.draw.rect (screen,(255,0,0),(0,770,50,30))
    pygame.draw.rect (screen,black,(0,770,50,30),2)
    title ('Skip',8,774,black)

#Victory condition and buttons
def victory (wave,enemynum,num = 1,etype = 'basic',multi = 1.5,livesnum = 3):
    global confirm,winc,bcolor,enemies1,enemies2,enemies3,enemies4,wcomplete
    if winc == True:
        while confirm == True:
            screen.fill (bcolor)
            title ('Wave ' + str(wave) + ' Complete!',330,350,(0,255,0))
            pygame.draw.rect (screen,(0,255,0),(150,420,100,30))
            pygame.draw.rect (screen,black,(150,420,100,30),2)
            title ('Next Wave',157,424,black)
            pygame.draw.rect (screen,(255,255,0),(350,420,100,30))
            pygame.draw.rect (screen,black,(350,420,100,30),2)
            title ('Retry?',376,424,black)
            pygame.draw.rect (screen,(255,0,0),(550,420,100,30))
            pygame.draw.rect (screen,black,(550,420,100,30),2)
            title ('Main Menu',555,424,black)
            pygame.display.update ()
            for event in pygame.event.get ():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx,my = event.pos
                    if 150 <= mx <= 250 and 420 <= my <= 450:
                        confirm = False
                        winc = False
                        enemies1 = []
                        enemies2 = []
                        enemies3 = []
                        enemies4 = []
                        wenemies = 0
                        lives = 3
                        save = score
                        wave = wave + 1
                        wcomplete [wave] = True
                    if 350 <= mx <= 450 and 420 <= my <= 450:
                        retry (enemynum,num,etype,multi,livesnum)
                    if 550 <= mx <= 650 and 420 <= my <= 450:
                        mainmenu ()
                        wcomplete [1] = True

#Losing condition and buttons
def defeat (enemynum,num = 1,etype = 'basic',multi = 1.5,livesnum = 3):
    global bcolor,confirm
    if losec == True:
        while confirm == True:
            screen.fill (bcolor)
            title ('You Lost!',360,350,(255,0,0))
            pygame.draw.rect (screen,(255,255,0),(200,420,100,30))
            pygame.draw.rect (screen,black,(200,420,100,30),2)
            title ('Retry?',226,424,black)
            pygame.draw.rect (screen,(255,0,0),(500,420,100,30))
            pygame.draw.rect (screen,black,(500,420,100,30),2)
            title ('Main Menu',505,424,black)
            pygame.display.update ()
            for event in pygame.event.get ():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx,my = event.pos
                    if 200 <= mx <= 300 and 420 <= my <= 450:
                        retry (enemynum,num,etype,multi,livesnum)
                    if 500 <= mx <= 600 and 420 <= my <= 450:
                        mainmenu ()

#Main Program:

intro ()
screen.fill (bcolor)
pygame.display.update ()

#Skip Tutorial Button Display
while skipshow == True:
    pygame.draw.rect (screen,(240,240,0),(317,377,160,25))
    pygame.draw.rect (screen,black,(317,377,160,25),2)
    subtext ('Click to Skip Tutorial',325,380,black)
    subtext ('To continue with Tutorial, click anywhere else.',240,420,black)
    pygame.display.update ()
    for event in pygame.event.get ():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx,my = event.pos
            if 317 <= mx <= 477 and 377 <= my <= 402:
                skipt = True
                skipshow = False
            else:
                skipshow = False

#Tutorial
if skipt == False:
    refresh ()
    subtext ('These gray lines resemble the lanes',430,230,black)
    subtext ('which enemies will be coming from.',450,260,black)
    subtext ('(Note: This is a tutorial for the',50,230,black)
    subtext ('default wave mode settings of the game.)',70,260,black)
    pygame.display.update ()
    time.sleep (8)
    refresh ()
    subtext ('This is a basic enemy.',475,250,black)
    pygame.draw.rect (screen,(255,45,75),(515,290,75,75))
    pygame.display.update ()
    time.sleep (2)
    refresh ()
    subtext ('Use the Arrow Keys or the \'WASD\' keys to',430,230,black)
    subtext ('shoot in the respective lane in the areas',450,260,black)
    subtext ('around your player, the blue square.',470,290,black)
    pygame.display.update ()
    time.sleep (6)
    refresh ()
    subtext ('The spaces around your player are where you',430,230,black)
    subtext ('can actually hit the enemy.',450,260,black)
    pygame.display.update ()
    time.sleep (4)
    refresh ()
    lcharge ()
    subtext ('A  hit instantly refills the bar.',430,220,black)
    subtext ('If you attack too early, a 1 second cooldown',430,260,black)
    subtext ('(noted in the bottom right) will activate',450,290,black)
    subtext ('with no parts of the bar filled.',470,320,black)
    pygame.display.update ()
    time.sleep (7)
    refresh ()
    lcharge ()
    scoreboard ()
    subtext ('Wave # is denoted in the top left with the',30,230,black)
    subtext ('number of lives you have left until it\'s gameover.',50,260,black)
    pygame.display.update ()
    time.sleep (5)
    refresh ()
    lcharge ()
    scoreboard ()
    subtext ('Your score is denoted in the top right; it',430,230,black)
    subtext ('increases as you destroy enemies.',450,260,black)
    subtext ('At the same time, the "uncalled" number of',430,290,black)
    subtext ('enemies is tracked below the score.',450,320,black)
    pygame.display.update ()
    time.sleep (6)
    refresh ()
    lcharge ()
    scoreboard ()
    subtext ('If an enemy block makes it all the way',430,230,black)
    subtext ('to your block, you will lose a life and',450,260,black)
    subtext ('that specific enemy will be buffed.',470,290,black)
    pygame.display.update ()
    time.sleep (6)
    refresh ()
    lcharge ()
    scoreboard ()
    subtext ('These "life-stealing" enemies have special',430,230,black)
    subtext ('symbols on them to show the level of life-steal.',450,260,black)
    subtext ('Here are the basic enemy Life-Steal levels 1-3.',430,480,black)
    pygame.draw.rect (screen,(255,45,75),(465,520,75,75)) #Sample 1
    pygame.draw.rect (screen,(255,45,75),(545,520,75,75)) #Sample 2
    pygame.draw.rect (screen,(255,45,75),(625,520,75,75)) #Sample 3
    pygame.draw.circle (screen,(165,42,42),(math.ceil (465+37),math.ceil (520+38)),20) #Sample 1
    pygame.draw.circle (screen,(165,42,42),(math.ceil (545+37),math.ceil (520+38)),20) #Sample 2
    pygame.draw.line (screen,(150,150,150),(math.ceil (545+37),math.ceil (520+10)),(math.ceil (545+37),math.ceil (520+65)),3)
    pygame.draw.line (screen,(150,150,150),(math.ceil (545+10),math.ceil (520+38)),(math.ceil (545+65),math.ceil (520+38)),3)
    pygame.draw.circle (screen,(165,42,42),(math.ceil (625+37),math.ceil (520+38)),20) #Sample 3
    pygame.draw.line (screen,(150,150,150),(math.ceil (625+37),math.ceil (520+10)),(math.ceil (625+37),math.ceil (520+65)),3)
    pygame.draw.line (screen,(150,150,150),(math.ceil (625+10),math.ceil (520+38)),(math.ceil (625+65),math.ceil (520+38)),3)
    pygame.draw.circle (screen,(255,215,0),(math.ceil (625+37),math.ceil (520+38)),5)
    pygame.display.update ()
    time.sleep (8)
    refresh ()
    lcharge ()
    scoreboard ()
    subtext ('These buffed enemies are also worth extra points.',430,230,black)
    subtext ('This is due to their increased difficulty, but it',450,260,black)
    subtext ('isn\'t recommended to sacrifice lives for points',470,290,black)
    subtext ('at least 90% of the time.',490,320,black)
    pygame.display.update ()
    time.sleep (8)
    refresh ()
    lcharge ()
    scoreboard ()
    subtext ('There will be different enemies introduced throughout',420,230,black)
    subtext ('the game, and they will have varying stats, rewards,',450,260,black)
    subtext ('and more... You\'ll just have to play and see.',470,290,black)
    pygame.display.update ()
    time.sleep (8)
    refresh ()
    lcharge ()
    scoreboard ()
    subtext ('Now that that\'s done...',525,230,black)
    subtext ('Let\'s try out a mock-wave against 10 basic enemies.',430,260,black)
    pygame.display.update ()
    time.sleep (5)

#Tutorial Wave (0)
    tutlost = False
    ecreate ()
    wenemies = 9#+1 for starter
    while wave == 0:
        refresh ()
        runenemies ()
        scoreboard ()
        lcharge ()
        lanim ()
        if winc == True and not tutlost:
            screen.fill (bcolor)
            title ('You\'ve finished the Tutorial!',280,360,(0,255,0))
            subtext ('There are more features to the game, but these were just the basics.',180,410,black)
            pygame.display.update ()
            time.sleep (3)
            wave = wave + 1
            counter = 0
        if winc == True and tutlost:
            screen.fill (bcolor)
            title ('Ha! I knew you had it in you.',285,340,(255,215,0))
            title ('You\'ve finished the (Harder) Tutorial!',245,375,(0,255,0))
            subtext ('There are more features to the game, but these were just the basics.',180,410,black)
            pygame.display.update ()
            time.sleep (5)
            wave = wave + 1
            counter = 0
        if losec == True and not tutlost:
            screen.fill (bcolor)
            title ('Wait you weren\'t supposed to lose the Tutorial...',215,360,(255,0,0))
            pygame.display.update ()
            time.sleep (3)
            screen.fill (bcolor)
            title ('Well I assume your audacity means something, so why not try this?',140,360,(255,0,0))
            pygame.display.update ()
            time.sleep (3)
            refresh ()
            enemies1 = []
            enemies2 = []
            enemies3 = []
            enemies4 = []
            wenemies = 9
            ecreate (6)
            losec = False
            lives = 5
            tutlost = True
        if losec == True and tutlost == True:
            screen.fill (bcolor)
            title ('Oh, I guess you are just bad at this game...',235,360,(255,0,0))
            subtext ('Well, better luck next time.',310,380,black)
            subtext ('Make sure to set some of the settings to "Easy" to make it easier on yourself.',140,400,black)
            pygame.display.update ()
            time.sleep (6)
            wave = 1
            wcomplete [0] = True
        pygame.display.update ()
    winc = False
    losec = False
    score = 0

#Main Menu First Selection

confirm = True
save = 0
selection = 1 #Remove after wave mode is finished
while True:
    selection = menu ()
    if selection == 1:
        lives = 3
        wave = 1 #Remove When Complete (RWC)
        ecreate ()
        wenemies = 14
        while wave == 1:
            refresh ()
            runenemies ()
            scoreboard ()
            lcharge ()
            lanim ()
            skip ()
            icard ('Information Card','This is where you\'ll find information on enemies and\nother new game mechanics.\nAnd don\'t worry, the game is paused while in this screen.\nClick off this info card, to resume game.')
            pygame.display.update ()
            victory (1,14)
            defeat (14)
            confirm = True
        lives = 3
        wave = 2 #RWC
        ecreate ()
        wenemies = 15
        while wave == 2:
            refresh ()
            runenemies ()
            scoreboard ()
            lcharge ()
            lanim ()
            skip ()
            icard ('New Enemy!','In this level, you will encounter an "Armored I" enemy.\nThey can be distinguished as being larger and having\nbolder outlines.\nThese guys take 2 hits to kill, but generally move slower \nthan the basic enemy.\nTheir lifesteal skill is the same as the basic enemy\n(i.e. moving faster).\nThey do not regenerate lives.','!')
            pygame.display.update ()
            victory (2,15)
            defeat (15)
            confirm = True
            if wenemies == 3:
                ecreate (3,'armored1',1.5)
                wenemies = 0

pygame.display.update ()
