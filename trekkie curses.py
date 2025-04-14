import string
import random

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

def display_grids(galaxy, quadrant):
    # Print galaxy map
    print('+---+---+---+---+---+---+---+---+')
    for qy in range(0,8):
        print('|', end='')
        for qx in range(0,8):
            print(str(quadrant[qx,qy].numk) + str(quadrant[qx,qy].numb) + str(quadrant[qx,qy].nums) + '|', end='')
        print()    
    print('+---+---+---+---+---+---+---+---+')
    print('Klingons: ' + str(galaxy.numk))
    print('Bases:    ' + str(galaxy.numb))
    print('Stars:    ' + str(galaxy.nums))
    
    # Print current quadrant
    print('QUADRANT: ', quadrant[enterprise.qxpos,enterprise.qypos].name)
    print('+---+---+---+---+---+---+---+---+')
    for sy in range(8):
        print('|', end='')
        for sx in range(8):
            print(' ' + sector[enterprise.qxpos,enterprise.qypos,sx,sy].occupant + ' |', end='')
        print()    
    print('+---+---+---+---+---+---+---+---+')


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

# Print all sectors
# for qx in range(0,8):
#     for qy in range(0,8):
#         print('QUADRANT: ', quadrant[qx,qy].name)
#         print('+---+---+---+---+---+---+---+---+')
#         for sy in range(8):
#             print('|', end='')
#             for sx in range(8):
#                 print(' ' + sector[qx,qy,sx,sy].occupant + ' |', end='')
#             print()    
#         print('+---+---+---+---+---+---+---+---+')

enterprise = ObjEnterprise()
display_grids(galaxy, quadrant)
while True:
    key = input('Command: ')
    if key == '1':
        enterprise.qypos += 1
    if key == '2':
        enterprise.qypos -= 1               
    if key == '3':
        enterprise.qxpos += 1               
    if key == '4':
        enterprise.qxpos -= 1
    if key == '9':
        quit()
    display_grids(galaxy, quadrant)            