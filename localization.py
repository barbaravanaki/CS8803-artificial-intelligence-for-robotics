# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

# localize: initializes p to a uniform distribution over a grid of the same dimensions as colors
def localize(colors, measurements, motions, sensor_right, p_move):

    pinit = 1.0 / float(len(colors)) / float(
        len(colors[0]))  # initially, you have an equal likelihood of being at any spot

    p = [[pinit for row in range(len(colors[0]))] for col in
         range(len(colors))]  #and that 1/n value gets printed at each spot

    for k in range(len(measurements)): #for each measurement, the robot needs ot move and recalibrate
        p = move(p, motions[k], p_move)
        p = sense(p, colors, measurements[k], sensor_right)

    return p #return the new, normalized distribution showing the most likely location of the bot

#sense: takes in the bot's observations of its surroundings, and measures it against the chance the sensor is actually accurate
def sense(p, colors, measurement, sensor_right):
    sensor_wrong = 1.0 - sensor_right

    distro = [[0.0 for col in range(len(p[0]))] for row in range(len(p))] #again, make another distribution table

    for i in range(len(p)):
        for j in range(len(p[i])):

            hit = (measurement == colors[i][j]) #if what you see is equal to the environment, it's a hit

            if measurement == colors[i][j]:
                hit = 1
                distro[i][j] = p[i][j] * sensor_right #now compare that to the likelihood the sensor is right

            else:
                hit = 0
                distro[i][j] = p[i][j] * sensor_wrong #otherwise, if it's a miss, compare it to the likelihood the sensor is wrong just in case

                s = sum(sum(distro, [])) #now sum the distribution to prepare to normalize it

    for i in range(len(distro)):
        for j in range(len(p[i])):
            distro[i][j] /= s #now actually normalize it using the regular normalization equation

    return distro


#move: move the robot according to the steps it took
def move(p, motion, p_move):
    p_malfunction = 1.0 - p_move #o_malfunction accounts for the chance that perhaps something happened and the robot stayed in place for some reason

    distro = [[0.0 for col in range(len(p[0]))] for row in range(len(p))]

    for i in range(len(p)):
        for j in range(len(p[i])):
            distro[i][j] = p_move * p[(i - motion[0]) % len(p)][(j - motion[1])] + p_malfunction * p[i][j] #now create the new distribution for moving

    return distro

#show: print the new distribution
def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'




#############################################################
# Sample test case: for the following test case, your output should be
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R', 'G', 'G', 'R', 'R'],
          ['R', 'R', 'G', 'R', 'R'],
          ['R', 'R', 'G', 'G', 'R'],
          ['R', 'R', 'R', 'R', 'R']]
measurements = ['G', 'G', 'G', 'G', 'G']
motions = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]
p = localize(colors, measurements, motions, sensor_right=0.7, p_move=0.8)
show(p)
