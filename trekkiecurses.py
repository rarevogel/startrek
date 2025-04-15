import string
import random
import curses

class ObjEnterprise:
    def __init__(self):
        self.energy = 3000
        self.torpedos = 10
        self.shields = 0
        while True:
            qx = random.randint(0,7)
            qy = random.randint(0,7)
            sx = random.randint(0,7)
            sy = random.randint(0,7)
            if sector[qx,qy,sx,sy].occupant == ' ':
                sector[qx,qy,sx,sy].occupant = 'E'
                self.qxpos = qx
                self.qypos = qy
                self.sxpos = sx
                self.sypos = sy
                break

class ObjSector:
    def __init__(self, quadrant, xpos, ypos, occupant=' '):
        self.quadrant = quadrant
        self.xpos = xpos
        self.ypos = ypos
        self.occupant = occupant
        self.name = 'S' + str(xpos) + str(ypos) + '-' + generator() 

class ObjQuadrant:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.name = 'Q' + str(xpos) + str(ypos) + '-' + generator()
        self.numk = 0
        self.numb = 0
        self.nums = 0
    def decrease_klingons(self):
        self.numk -= 1
        galaxy.decrease_klingons()

class ObjGalaxy:
    def __init__(self, numk, numb, nums):
        self.numk = numk
        self.numb = numb
        self.nums = nums
    def decrease_klingons(self):
        self.numk -= 1

def generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def display_galaxy(galaxy, quadrant):
    scr.addstr(0,0,'GALAXY:')
    scr.addstr(1,0,'+---+---+---+---+---+---+---+---+')
    for qy in range(0,8):
        scr.addstr(qy+2,0,'|')
        for qx in range(0,8):
            if qy == enterprise.qypos and qx == enterprise.qxpos:
                scr.addstr(qy+2,1+qx*4,str(quadrant[qx,qy].numk) + str(quadrant[qx,qy].numb) + str(quadrant[qx,qy].nums), curses.A_REVERSE)
                scr.addstr(qy+2,4+qx*4,'|')
            else:    
                scr.addstr(qy+2,1+qx*4,str(quadrant[qx,qy].numk) + str(quadrant[qx,qy].numb) + str(quadrant[qx,qy].nums) + '|')
    scr.addstr(qy+3,0,'+---+---+---+---+---+---+---+---+')
    scr.addstr(qy+4,0,'Klingons: ' + str(galaxy.numk))
    scr.addstr(qy+5,0,'Bases:    ' + str(galaxy.numb))
    scr.addstr(qy+6,0,'Stars:    ' + str(galaxy.nums))
    
def display_quadrant(quadrant):
    scr.addstr(0,44,'QUADRANT: ' + quadrant[enterprise.qxpos,enterprise.qypos].name)
    scr.addstr(1,44,'+---+---+---+---+---+---+---+---+')
    for sy in range(0,8):
        scr.addstr(sy+2,44,'|')
        for sx in range(0,8):
            scr.addstr(sy+2,45+sx*4,' ' + sector[enterprise.qxpos,enterprise.qypos,sx,sy].occupant + ' |')
    scr.addstr(sy+3,44,'+---+---+---+---+---+---+---+---+')

# Generate Quadrants and Sectors
sector = {}
quadrant = {}
for qx in range(8):
    for qy in range(8):
        quadrant[qx,qy] = ObjQuadrant(qx, qy)
        for sx in range(8):
            for sy in range(8):
                sector[qx,qy,sx,sy] = ObjSector(quadrant[qx,qy], sx, sy)

# Populate Sectors
numklingons = random.randint(15,30)
numbases = random.randint(4,7)
numstars = random.randint(50,100)
galaxy = ObjGalaxy(numklingons, numbases, numstars)
for b in range(numbases + 1):
    while True:
        qx = random.randint(0,7)
        qy = random.randint(0,7)
        sx = random.randint(0,7)
        sy = random.randint(0,7)
        if sector[qx,qy,sx,sy].occupant == ' ':
            sector[qx,qy,sx,sy].occupant = 'B'
            quadrant[sector[qx,qy,sx,sy].quadrant.xpos,sector[qx,qy,sx,sy].quadrant.ypos].numb += 1
            break

for b in range(numklingons + 1):
    while True:
        qx = random.randint(0,7)
        qy = random.randint(0,7)
        sx = random.randint(0,7)
        sy = random.randint(0,7)
        if sector[qx,qy,sx,sy].occupant == ' ':
            sector[qx,qy,sx,sy].occupant = 'K'
            quadrant[sector[qx,qy,sx,sy].quadrant.xpos,sector[qx,qy,sx,sy].quadrant.ypos].numk += 1
            break

for b in range(numstars + 1):
    while True:
        qx = random.randint(0,7)
        qy = random.randint(0,7)
        sx = random.randint(0,7)
        sy = random.randint(0,7)
        if sector[qx,qy,sx,sy].occupant == ' ':
            sector[qx,qy,sx,sy].occupant = 'S'
            quadrant[sector[qx,qy,sx,sy].quadrant.xpos,sector[qx,qy,sx,sy].quadrant.ypos].nums += 1
            break

enterprise = ObjEnterprise()

scr = curses.initscr()
display_galaxy(galaxy, quadrant)
display_quadrant(quadrant)
scr.refresh()

while True:
    k = scr.getch()
    if chr(k) == 'S':
        enterprise.qypos += 1
    if chr(k) == 'W':
        enterprise.qypos -= 1               
    if chr(k) == 'D':
        enterprise.qxpos += 1               
    if chr(k) == 'A':
        enterprise.qxpos -= 1
    if chr(k) == 'Q':
        quit()
    display_galaxy(galaxy, quadrant)
    display_quadrant(quadrant)
    scr.refresh()
