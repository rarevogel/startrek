#   trek.bas   27-Jul-73   Aron K. Insinga   Project Delta
#
#   http://pdp-11.trailing-edge.com/rsts11/rsts-11-020/
#
# Converted to python 26 Aug 2024, Mike Markowski, mike.ab3ap@gmail.com
#
# Conversion included introduction of subroutines and converting arrays to
# start at 0 rather 1 and math changes that that required.  I also converted
# output text from all upper to mixed case and even discovered a bug (noted
# in warp().

from numpy.random import randint, random
from numpy import arctan2, cos, pi, sin, sqrt, where, zeros
import numpy as np

ds = ['Warp Engines', 'S.R. Sensors', 'L.R. Sensors',
    'Phaser Cntrl', 'Photon Tubes', 'Damage Cntrl', 'Computer']
d = zeros(7, dtype=int)     # Damage control status.
g = zeros((8,8), dtype=int) # Galaxy, 8x8 quadrants.
m = zeros((8,8), dtype=int) # Galaxy explored.
q = zeros((8,8), dtype=int) # Quadrant, 8x8 sectors.
k = zeros((9,3), dtype=int) # Klingons, sector location and energy level.

t = t0 = 100*randint(20, 39) # Current and start Stardate.
t9 = 40          # Solar years to complete mission.
e = e0 = 3000    # Current and initial Enterprise energy level.
p = p0 = 10      # Current and initial number of photon torpedos.
a = 0            # 0 to allow Klingon attack.
b9 = k3 = k9 = 0 # Number of Klingons in quadrant and galaxy.
q1 = q2 = 0      # Current quadrant.
s1 = s2 = 0      # Current sector.
s9 = 200         # Klingon initial energy level.
c = 'Green'

def adjCells(a, rLoc, cLoc):
    r0 = max(0, rLoc-1)
    r1 = min(7, rLoc+1) + 1
    c0 = max(0, cLoc-1)
    c1 = min(7, cLoc+1) + 1
    return a[r0:r1, c0:c1]

def chartPrint():
    print('\n    ', end='')
    for i in range(8):
        print('%d   ' % (i+1), end='')
    print('\n  ' + 33*'-')
    for i in range(8):
        print('%d ' % (i+1), end='')
        print(8*':   ' + ':')
        print('  ' + 33*'-')

def computer():
    global b9,k,k9,d,ds,q1,q2,s1,s2,t,t0,t9
    if d[6] < 0:
        print('Computer is disabled')
        return
    while True:
        a = input('Computer active and awaiting command: ').strip()
        if a != '':
            a = a[0]
        if a in ['0', '1', '2', '3']:
            break
        print('Functions available from computer')
        print('   0 = Cumulative galactic record')
        print('   1 = Status report')
        print('   2 = Photon torpedo data')
        print('   3 = Direction calculator')
    if a == '0':
        mapPrint(m, q1, q2)
    elif a == '1':
        print('\n   Status Report\n')
        print('Number of Klingons left = %d' % k9)
        print('Number of Stardates left = %d' % (t0+t9-t))
        print('Number of Starbases left = %d' % b9)
        damageRpt()
    elif a == '2':
        for i in range(9):
            if k[i,2] <= 0:
                continue
            rng, theta = vec(s2, s1, k[i,1], k[i,0])
            print(' Range %.1f, bearing %.1f' % (rng, theta))
    else:
        print('You are at quadrant (%d,%d) sector (%d,%d)'
            % (q1+1, q2+1, s1+1, s2+1))
        line = input('Ship\'s & target\'s coordinates are: ')
        try:
            line = line.replace(',', ' ').split()
            line = map(int, line)
            y0, x0, y1, x1 = line
        except ValueError:
            return
        rng, theta = vec(y0, x0, y1, x1)
        print(' Range %.1f, bearing %.1f (sector warp %.2f)'
            % (rng, theta, 0.125*rng))

def damageRpt():
    # Damage control report
    global d,ds
    if d[5] < 0:
        return
    print('\n%-13s%s\n' % ('Device','State'))
    for i in range(6):
        print('%-8s%6d' % (ds[i], d[i]))

def emptySector():
    # Find an empty sector in this quadrant.
    global q
    while True:
        r1,r2 = randint(0,8,2)
        if q[r1,r2] == 0:
            return r1,r2

def galaxySetup():
    global b9,g,k0,k3,k9,q1,q2,s1,s2

    # If random number < r[i], there are i+1 Klingons in quadrant.
    r = np.array([13.28, 6.28, 3.28, 1.28, 0.28, 0.08, 0.03, 0.01, 0.0001])/64
    q1,q2,s1,s2 = randint(0,8,4) # Start in random quadrant and sector.
    # Set up galaxy
    b9 = k9 = 0
    for i in range(8):
        for j in range(8):
            k3 = where(random()<r)[0].size # Klingons in quadrant.
            k9 += k3                       # Klingons in galaxy.
            b3 = 1 if random()<0.1 else 0  # Star base in quadrant.
            b9 += b3                       # Star bases in galaxy.
            g[i,j] = k3*100 + b3*10 + randint(1,8) # Klingon/Base/Stars
    k0 = k9                  # Original number of Klingons.
    if b9 == 0:              # Ensure at least 1 star base exists.
        i,j = randint(0,8,2)
        g[i,j] += 10
        b9 = 1

def inputSafe(dtype, prompt):
    '''Keep trying for correct input until user does it right!  This prevents
    the game from dying on incorrect type of response, e.g., accidentally
    entering a text command when a number is expected.
    '''

    while True:
        try:
            return dtype(input(prompt))
        except ValueError:
            pass

def klingonAttack():
    # Klingon attack
    global e,k,k3,s1,s2

    if k3 == 0:      # No Klingons in this quadrant.
        return False # Game not over.
    if c == 'Docked':
        print('Starbase shields protect Enterprise')
        return False
    print('')
    for i in range(9):
        if k[i,2] > 0: # Look for Klingon.
            # Hit is Klingon health reduced by distance.
            dist = sqrt((k[i,0] - s1)**2 + (k[i,1] - s2)**2)
            h = int((k[i,2]/dist)*(2 + random())) + 1
            e = max(0, e-h) # Reduce Enterpise health.
            print('%s unit hit from Klingon at sector %d - %d'
                % (h, 1+k[i,1], 1+k[i,0]))
            print('   (%d units left)' % e)
            if e == 0:
                return lose() # Enterprise destroyed.
    return False # Game not over.

def longRange():
    # Long range sensor scan
    global d,g,m,q1,q2

    if d[2] < 0:
        print('Long range sensors are inoperable')
        return
    print('Long range sensor scan for quadrant %d - %d\n' % ((q2+1), (q1+1)))
    for i in range(q1-1, q1+2):
        for j in range(q2-1, q2+2):
            print('  ', end='')                 # Indent output.
            if (0 <= i <= 7) and (0 <= j <= 7): # Quadrant is in galaxy.
                print('%03d' % g[i,j], end='')
                m[i,j] = g[i,j]                 # Remember explored regions.
            else:                               # Quadrant is outside galaxy.
                print('000', end='')
        print('')

def lose():
    # You lose.
    global k9,t

    print('\n\tIt is Stardate %d\n' % t)
    print('The Enterprise has been destroyed.')
    print('The Federation will be conquered.')
    print('There are still %d Klingon battle cruisers.' % k9)
    print('You are dead.')
    return True # Game over. :-(

def mapPrint(map, row=-1, col=-1):

    print('\n    ', end='')
    for i in range(8):
        print('%d   ' % (i+1), end='') # Print column numbers.
    print('\n  ' + 33*'-')             # Dashed lines.
    for i in range(8):
        print('%d ' % (i+1), end='')   # Print row number.
        for j in range(8):
            sep = '>' if i==row and j==col else '|'
            info = ' - ' if map[i,j]==0 else '%03d'%map[i,j]
            print('%s%s' % (sep, info), end='')
        print('|')                     # Close row.
    print('  ' + 33*'-')               # Dashed lines.

def phasers():
    # Phaser control
    global d,e,g,k,k3,k9,m,q1,q2,s1,s2

    if d[3] < 0:
        print('Phaser control is disabled')
        return False # Game not over.
    # print('Phasers locked in on target.  Energy available  = %d' % e)
    print('Phasers locked on target.  Energy available = %d' % e)
    while True:
        x = inputSafe(float, 'Number of units to fire? ')
        if x <= 0: # Never mind, leave.
            return False # Game not over.
        elif x > e: # Can't use more than you have.  Try again.
            continue
        else:
            break
    e -= x # Reduce Enterprise health.
    for i in range(9): # Fire on all Klingons in quadrant.
        if k[i,2] <= 0:
            continue
        dist = sqrt((k[i,0] - s1)**2 + (k[i,1] - s2)**2)
        h = int(x/dist*(2 + random()))
        k[i,2] -= h # Reduce Klingon health.
        print('%d unit hit on Klingon at sector %d - %d'
            % (h, 1+k[i,1], 1+k[i,0]))
        if k[i,2] > 0:
            # print('   (%d left)' % k[i,2])
            print('   (%d units left)' % k[i,2])
            continue
        # print('Klingon at sector %d - %d destroyed!' % (1+k[i,1], 1+k[i,0]))
        print('   Klingon destroyed!')
        k3 -= 1               # One less Klingon in quadrant.
        k9 -= 1               # One less Klingon in galaxy.
        q[k[i,0], k[i,1]] = 0 # Remove Klingon from quadrant.
        g[q1,q2] -= 100       # Remove Klingon from galaxy.
        m[q1,q2] -= 100       # Remove Klingon from explored map.
        if k9 == 0:           # All Klingons destroyed!
            return win()      # Game over, we win.
    return False              # Game not over.

def quadrantSetup():
    # Set up quadrant

    global a,b3,k,k3,q,q1,q2,s1,s2,s3,s9

    print('You are currently in quadrant %d - %d ' % ((q2+1), (q1+1)))
    k3,b3,s3 = list(map(int,list('%03d' % g[q1,q2]))) # Klingons/base/stars.
    q[:,:] = 0             # Clear old quadrant layout.
    q[s1,s2] = 1           # Place Enterprise in its sector.
    k[:,:] = 0             # Clear old Klingons.
    for i in range(k3):    # Place Klingons randomly.
        r1,r2 = emptySector()
        q[r1,r2] = 2       # Place Klingon.
        k[i,0] = r1        # Record sector.
        k[i,1] = r2
        k[i,2] = s9        # Initial energy level.
    if b3 == 1:            # Place star base randomly.
        r1,r2 = emptySector()
        q[r1,r2] = 3       # Place star base.
    for i in range(s3):    # Place stars randomly.
        r1,r2 = emptySector()
        q[r1,r2] = 4       # Place star.
    a = 0                  # Allow Klingon attack.

def shortRange():
    # Short range sensor scan
    global a,c,d,e,e0,g,k3,k9,m,p,p0,q,q1,q2

    if np.any(adjCells(q, s1, s2) == 3):
        c = 'Docked' # Star base in an adjacent sector.
        e = e0       # Refill energy.
        p = p0       # Refill photon torpedos.
    elif k3 > 0:     # Klingons are here.
        c = 'Red'
    elif e <= e0/10:
        c = 'Yellow' # Enterprise under 10% energy.
    elif np.any(adjCells(g, q1, q2) >= 100):
        c = 'Yellow' # Klingon in an adjacent quadrant.
    else:
        c = 'Green'  # Beam down for shore leave!

    if d[1] < 0:
        print('Short range sensors are inoperable')
    else:
        m[q1,q2] = g[q1,q2] # Remember this quadrant.
        print('\n ---------------')
        for i in range(8):
            print(' ', end='')
            for j in range(8):
                print('.EKB*'[q[i,j]] + ' ', end='')
            print('')
        print(' ---------------\n')
        s = 'Stardate: %d' % t
        print('%-25sCondition: %s' % (s, c))
        s = 'Quadrant: %d - %d' % ((q2+1), (q1+1))
        print('%-25sSector: %d - %d' % (s, (s2+1), (s1+1)))
        s = 'Energy: %d' % e
        print('%-25sPhoton Torpedos: %d' % (s, p))
        print('Klingons: %d' % k9)
    return

def torpedos():
    # Photon torpedos
    global b3,d,k3,k9,p,q,q1,q2,s1,s2,s3

    if d[4] < 0:
        print('Photon tubes are not operational')
        return False # Game not over.
    if p == 0:
        print('All photon torpedos expended')
        return False # Game not over.
    while True:
        c1 = inputSafe(float, 'Torpedo course (1-8.99999)? ')
        if c1 == 0:
            return False # Game not over.
        elif not (1 <= c1 < 9):
            continue
        else:
            break
    x1 = -sin((c1 - 1)*pi/4)
    x2 = cos((c1 - 1)*pi/4) # Unit vector, course c1 is multiple of 45 deg.
    x,y = s1,s2             # Start at current sector.
    p -= 1                  # Use 1 photon torpedo.
    print('\nTorpedo track:')
    while True:
        x += x1
        y += x2             # Move along unit vector.
        z1 = int(x + 0.5)
        z2 = int(y + 0.5)   # Nearest sector.
        if not (0 <= z1 <= 7) or not (0 <= z2 <= 7): # Torpedo left quadrant.
            print('Missed')
            return klingonAttack()
        print(' %3.1f - %3.1f' % (y, x))
        if q[z1,z2] != 0:   # Torpedo hit something.
            break
    # Find out what torpedo hit.
    if q[z1,z2] == 2:       # Hit a Klingon.
        print('*** Klingon destroyed ***')
        for i in range(9):
            if (k[i,0],k[i,1]) == (z1,z2):
                k[i,2] = 0  # Remove destroyed Klingon.
        k3 -= 1             # Klingon count in quadrant.
        k9 -= 1             # Klingon count in galaxy.
        if k9 == 0:
            return win()    # Game over, we won!
    elif q[z1,z2] == 4:     # Hit a star.
        print('Star destroyed')
        s3 -= 1             # Star count in quadrant.
    else:                   # Hit a star base!
        print('*** Starbase destroyed... Congratulations ***')
        b3 = 0              # Star base count in quadrant.
    q[z1,z2] = 0            # Remove destroyed object.
    g[q1,q2] = k3*100 + b3*10 + s3 # Update this quadrant of galaxy.
    m[q1,q2] = k3*100 + b3*10 + s3 # Update explored.
    return klingonAttack()

def trek():
    global a

    over = False # Game is not over.
    galaxySetup()
    welcome()
    quadrantSetup()
    shortRange()
    while not over: # Let's play a game!
        a = 1 # Disallow Klingon attack.
        ans = input('\nCommand? ').strip()
        if ans == '':
            continue
        ans = ans[0].lower() # 1st char to lower case.
        if ans == 'c': # Course set.
            over = warp() # a=0 to allow Klingon attack.
            if not over:
                shortRange()
                if c == 'Red' and a == 0 and klingonAttack():
                    return True # Game over, we lost.
        elif ans == 's': # Short range scan.
            shortRange()
            if c == 'Red' and a == 0 and klingonAttack():
                return True # Game over, we lost.
        elif ans == 'l': # Long range scan.
            longRange()
        elif ans == 'p': # Phaser control.
            over = phasers()
            if not over:
                over = klingonAttack()
        elif ans == 't': # Photon torpedos.
            over = torpedos()
        elif ans == 'd': # Damage control report.
            damageRpt()
        elif ans == 'e': # Exit
            over = True
        elif ans == 'b': # Library Computer, added by Mike to mimic sttr1.
            computer()
        else:
            print('Commands: c, s, l, p, t, d, e, b.')

def vec(ex, ey, tx, ty):
    theta = arctan2(-(ty-ey), tx-ex)/(pi/4)
    if theta <= 0:
        theta += 8
    theta = theta%8 + 1
    dist = sqrt((tx-ex)**2 + (ty-ey)**2)
    return dist, theta

def warp():
    # Warp drive

    global d,ds,e,k3,q,q1,q2,s1,s2,t

    while True:
        c1 = inputSafe(float, 'Course (1-8.99999)? ')
        w1 = inputSafe(float, 'Warp factor (0-12)? ')
        if w1*c1 == 0:
            return False # Decided against warping.
        elif not (1 <= c1 < 9) or not (0 < w1 <= 12):
            continue # Bad input.
        if d[0] < 0 and w1 > 0.2:
            print('Warp engines are damaged, maximum speed = warp 0.2')
            continue
        break # Break on valid input.
    if k3 > 0: # Klingons in quadrant attack as Enterprise moves.
        if klingonAttack():
            return True # Game over, we lost.
    for i in range(6): # Recover a little from past damage.
        d[i] = min(0, d[i]+1)
    r = random()
    if r < 0.1: # Damage is repaired.
        for i in range(6):
            if d[i] == 0: # Undamaged.
                continue
            d[i] += randint(1, -d[i]) # Repair damage.
            d[i] = min(0, d[i])
            print('*** Truce, %s state of repair improved ***' % ds[i])
    elif r < 0.2: # Equipment is damaged.
        i = randint(6)       # Randomly pick equipment to damage.
        d[i] -= randint(1,6) # Damage by random amount.
        d[i] = min(0, d[i])
        print('*** Space storm, %s damaged ***' % ds[i])
    t += 1 # A Solar year passes.
    n = int(8*w1) # Number of sectors to move.
    e -= n # Travel reduces Enterprise energy.
    if e <= 0 or t > t0+t9: # Outta gas or outta time.
        return lose() # Game over.
    q[s1,s2] = 0 # Enterprise leaves sector.
    x,y = s1,s2  # Enterprise current sector is (x,y).
    x1 = -sin((c1 - 1)*pi/4) # Unit vector, course c1 is multiple of 45 deg.
    x2 = cos((c1 - 1)*pi/4)
    for _ in range(n): # Sector at a time, check for objects in the way.
        x += x1 # Update position along unit vector.
        y += x2
        z1 = round(x) # Nearest sector.
        z2 = round(y)
        if not (0 <= z1 <= 7) or not (0 <= z2 <= 7): # Left quadrant.
            # dest = posQuad + posSect + speed*time.
            x = q1 + s1/8 + w1*x1 # Destination quadrant, real.
            y = q2 + s2/8 + w1*x2
            if    x < 0: x = s1 = 0
            elif  x > 7: x = s1 = 7
            else: s1 = int((8*(x - int(x)))%8) # Sector, integer.
            if    y < 0: y = s2 = 0
            elif  y > 7: y = s2 = 7
            else: s2 = int((8*(y - int(y)))%8)
            z1 = int(x) # Quadrant, integer.
            z2 = int(y)
            if (q1,q2) != (z1,z2):
                q1,q2 = z1,z2
                quadrantSetup() # Enables Klingon attack.
            q[s1,s2] = 1 # Enterprise arrives here.
            return False # Game not over.
        if q[z1,z2] != 0:
            print('Enterprise blocked by object at sector %d - %d'
                % (z2+1, z1+1))
            x -= x1
            y -= x2 # Back up along unit vector.
            break
    s1 = int(x)
    s2 = int(y)
    q[s1,s2] = 1 # Enterprise arrives here.
    return False # Game not over.

def welcome():
    global k9,t,t0,t9

    print('\nOrders:   Stardate %d\n' % t)
    print('As commander of the United Starship Enterprise, your mission')
    print('is to rid the galaxy of the deadly Klingon menace.  To do this,')
    print('you must destroy the Klingon invasion force of %d battle' % k9)
    print('cruisers.  You have %d Solar Years to complete your mission.' % t9)
    print('(I.e., until Stardate %d.)\n' % (t0+t9))
    print('Give command \'end\' to stop the game early.')
    ans = input('Do you require further instructions? ')
    if ans.lower() == 'y':
        f = open('trek.doc', 'r')
        while True:
            line = f.readline()
            if line == '':
                break
            print(line.rstrip())
        f.close()
    ans = input('Do you want a chart? ')
    if ans.lower() == 'y':
        chartPrint()

def win():
    global t,t0,k0

    print('\n\tIt is Stardate %d\n' % t)
    print('The last Klingon battle cruiser in the galaxy has been destroyed.')
    print('The Federation has been saved.')
    print('You have been promoted to Admiral.')
    print('%d Klingons in %d years.  Rating = %d'
        % (k0, t-t0, int(k0/(t-t0)*1000)))
    return True # Game over. :-)

if __name__ == '__main__':
    trek()
