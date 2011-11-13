# WORKS!!!!!
# Can't believe I managed to pull this off. I'm actually kind of proud of it.

from sys import float_info, exit
from math import sqrt
from time import clock
from copy import copy
import random

class Ball(object):
    def __init__(self, point, radius=0):
        self.center = point
        self.radius = radius
    
    def __setradius(self, value):
        self._radius = float(value)
                
    def __getradius(self):
        return self._radius
    
    #We define radius as a property so as to force it to be a float
    #In future versions of python with a redefined /, this won't be an issue    
    radius = property(__getradius,__setradius)
    
    def __repr__(self):
        return str(self)
     
    def __str__(self):
        return str(self.radius)+" "+str(self.center)

def select_on_coord(balls, split, axis):
    l, h = 0, len(balls)
    while l<h:
        r = random.randrange(l,h)
        balls[r], balls[l] = balls[l], balls[r]
        m = l
        for i in range(l+1, h):
            if balls[i].center[axis] < balls[l].center[axis]:
                m+=1
                balls[m], balls[i] = balls[i], balls[m]
        
        balls[l] , balls[m] = balls[m], balls[l]
        if m < split:
            l = m+1
        else:
            h = m-1
            
    return balls

def build_balltree(points):
    return __build_balltree([Ball(point) for point in points])

       
def __build_balltree(balls):
    if len(balls) == 0:
        return None
    bt = Node()
    if len(balls) == 1:
        bt.ball = balls[0]
        return bt
    
    axis = most_spread_axis(balls)
    midpoint = len(balls)//2
    balls = select_on_coord(balls, midpoint, axis)
    
    
    bt.axis = axis
    
    bt.left_child = __build_balltree(balls[:midpoint])
    bt.right_child = __build_balltree(balls[midpoint:])
    
    if bt.left_child == None:
        bt.ball = bt.right_child.ball
    elif bt.right_child == None:
        bt.ball = bt.left_child.ball
    else:
        bt.ball = bounding_ball(bt.left_child.ball, bt.right_child.ball)
    return bt

def bounding_ball(balla, ballb):
    dist = distance(balla.center, ballb.center)
    if balla.center == (69, 67) or ballb.center == (69, 67):
        print "DEBUG HERE"
    if dist == 0 or 2*dist < balla.radius + ballb.radius:
        if balla.radius > ballb.radius:
            return balla
        else:
            return ballb
    
    #We keep a list of the dimensions for future use
    dim = range(len(balla.center))
    #We find the opposite points on the bounds of the ball
    # radius*(difference between ball center vectors)/magnitude of that difference + center vector
    fara = [((balla.radius*(balla.center[i]-ballb.center[i])/dist)+balla.center[i]) for i in dim]
    farb = [(ballb.center[i]+(ballb.radius*(ballb.center[i]-balla.center[i])/dist)) for i in dim]
    
    newcenter = tuple([(fara[i]+farb[i])/2 for i in dim])
    newradius = distance(fara,farb)/2.0
    
    retball = Ball(newcenter,newradius)
    return retball

def most_spread_axis(balls):
    most_spread = float_info.min
    most_spread_axis = -1
    for axis in range(0, len(balls[0].center)):
        spread = ball_spread_on_axis(balls, axis)
        if spread > most_spread:
            most_spread = spread
            most_spread_axis = axis
    
    return most_spread_axis

def ball_spread_on_axis(balls, axis):
    lowest = float_info.max
    highest = float_info.min
    
    for ball in balls:
        if ball.center[axis] - ball.radius < lowest:
            lowest = ball.center[axis] - ball.radius
        if ball.center[axis] + ball.radius > highest:
            highest = ball.center[axis] - ball.radius
            
    return highest-lowest
    

class Node(object): 
    def __init__(self):
        self.ball = None
        self.axis = None
        self.left_child = None
        self.right_child = None
    
    def __repr__(self):
        if self.ball == None:
            return ""
        retstr = repr(self.ball)+"Over the "+str(self.axis)+' axis\n'
        leaf = True
        if self.left_child != None:
            retstr += "Left:\n"
            for line in repr(self.left_child).split('\n'):
                retstr += "    "+line+'\n'
                
        if self.right_child != None:
            retstr += "Right:\n"
            for line in repr(self.right_child).split('\n'):
                retstr += "    "+line+'\n'
        return retstr
        
    def __str__(self):
        return repr(self)
             
def distance(pointx, pointy):
    k = len(pointx)
    return sqrt(sum([(pointx[i] - pointy[i]) ** 2 for i in range(k)]))

def near_ball_distance(ball, point):
    return distance(ball.center, point)-ball.radius

def nearest_neighbor(balltree, point, candidate=None, max_dist=float_info.max):
    if balltree == None:
        return candidate, max_dist  
    s = balltree.axis
    best_guess = candidate
    best_distance = max_dist
    
    
    #We will set this variable to the child we don't search in case we have to search it
    remaining_child = None
    
    #If we're a leaf, we end the recursion here.
    if s == None:
        my_distance = near_ball_distance(balltree.ball, point)
        if my_distance < best_distance:
            best_guess = balltree.ball.center
            best_distance = my_distance
    else:
        left_dist = float_info.max
        right_dist = float_info.max
        if(balltree.left_child != None):
            left_dist = near_ball_distance(balltree.left_child.ball, point)
        if(balltree.right_child != None):
            right_dist = near_ball_distance(balltree.right_child.ball, point)
            
        if (left_dist <= max_dist or right_dist <= max_dist):
            if left_dist <= right_dist:
                best_guess, best_distance = nearest_neighbor(balltree.left_child, point, best_guess, best_distance)
                if right_dist <= best_distance:
                    best_guess, best_distance = nearest_neighbor(balltree.right_child, point, best_guess, best_distance)
                    
            else:
                best_guess, best_distance = nearest_neighbor(balltree.right_child, point, best_guess, best_distance)
                if left_dist <= best_distance:
                    best_guess, best_distance = nearest_neighbor(balltree.left_child, point, best_guess, best_distance)
       
    return best_guess, best_distance
    
    
    
        
def brute_nn(point_list, point):
    current_distance = float_info.max
    for p in point_list:
        if distance(point,p) < current_distance:
            current_distance = distance(point,p)
            closest = p
            
    return closest, current_distance     
    
    
       
    
def test():
    
    random.seed(12345)
    point_list1 = [(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)]
    bt = build_balltree(point_list1)
    
    print "3d Distance test"
    print distance((1, 2, 3), (1, 3, 2))
    print "Should have been ~1.4"
    
    print bt
    nearest = nearest_neighbor(bt,(1,9))
    print nearest
    print "Should have been", brute_nn(point_list1, (1,9))
    print
    point_list2 = [(2,2),(3,8),(6,7),(7,4)]
    kdt2 = build_balltree(point_list2)
    nearest = nearest_neighbor(kdt2,(7,3))
    print nearest
    print "Should have been", brute_nn(point_list2, (7,3))
    
    
    nummax = 100
    
    data = []
    for numvars in xrange(100,10000,100):
        print
        print
        print "Trying %d points" % numvars
        point_list_random = [(random.randrange(nummax), random.randrange(nummax)) for x in range(numvars)]
        test_points = [(random.randrange(nummax), random.randrange(nummax)) for x in range(100)]
        
        kdt3 = build_balltree(point_list_random)
        total_kdtree_time = 0.0
        total_brute_time = 0.0
        for point in test_points:
            if point != (68, 66) or numvars != 100:
                continue
            start = clock()
            nearest = nearest_neighbor(kdt3,point)
            end = clock()
            total_kdtree_time += end-start
            
            start = clock()
            verified_nearest = brute_nn(point_list_random, point)
            end = clock()
            total_brute_time += end-start
            
            #We should never get to this point. But we dump out our state so that we can figure out what happened
            if nearest[0] != verified_nearest[0] and nearest[1] != verified_nearest[1]:
                print kdt3
                print point, nearest, verified_nearest
                exit()
        
        data.append((numvars, total_kdtree_time, total_brute_time))
        print "Total time spent in balltree searches", total_kdtree_time
        print "Total time spent in bf searches", total_brute_time
    
    
    print "CSV for pretty graphs"    
    for point in data:
        print "%d,%f,%f" % point
        
if __name__=="__main__":
    test()