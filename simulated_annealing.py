import math
import random
from functools import reduce
import graphics
import time

class City():
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        

cities = [
    City(0, 0, 0), City(2, 2, 1), 
    City(4, 4, 2), City(8, 2, 3), 
    City(30, 2, 4), City(2, 40, 5),
    City(3, 10, 6), City(0, 19, 7)
]

# cities = [City(0, 0), City(1, 0), City(2, 0)]
# cities = [City(2, 0), City(0, 0), City(1, 0)]

def salesman(permutation):
    total = 0
    c = permutation[0]
    for ind in range(1, len(permutation)):
        c_next = permutation[ind]
        total += city_dist(c, c_next)
        c = c_next
    return total

def city_dist(c1, c2):
    return math.sqrt((c1.x-c2.x)**2 + (c1.y-c2.y)**2)

def energy(s):
    return salesman(s)

def probability(s, s_new, T):
    current_energy = energy(s)
    new_energy = energy(s_new)
    if new_energy < current_energy:
        # print(current_energy, "-->", new_energy)
        return 1
    elif T > 0:
        # if d != 0:
            # print(d)
        delta = (new_energy-current_energy) / T
        if delta > 700 :
            return 0 
        prob = 2 - math.exp(delta)
        # print(prob)
        # return math.exp((d+(T*T))/T)/(1+math.exp((d+(T*T))/T))
        # return math.exp(-(new_energy-current_energy) / T)
        return prob
    else :
        return 0

def generateCities(width, height, count):
    return [City(random.random()*width, random.random()*height, "_") for _ in range(count) ]


def neighbor(s, T):
    rtrn = [c for c in s]
    ind = math.floor(random.random() * (len(s)-1))
    # length = len(s)
    # ind2 = round(random.gauss(ind1, T))
    # ind2 = bind_int(ind2, 0, length)
    # ind2 = math.floor(random.random() * len(s))
    temp = rtrn[ind]
    rtrn[ind] = rtrn[ind+1]
    rtrn[ind+1] = temp
    return rtrn

if __name__ == "__main__":
    width = 500
    height = 500
    win = graphics.GraphWin(width=width, height=(height+20), autoflush=False)
    graph = graphics.GraphWin(width=width, height=(height), autoflush=False)
    # graph.yUp()
    graph_data = []

    s = generateCities(width, height, 18)
    # pt = graphics.Point(100, 50)
    # pt.draw(win)
    # circle = graphics.Circle(pt, 25)
    # circle.draw(win)
    print("beginning annealing")
    print(salesman(s))
    innit_state = salesman(s)
    innit_energy = innit_state*1.5
    k = 100000
    k_min = .1
    reduction_factor = .99
    repeat_num = 100
    loops = 0
    total_loops = math.log(k_min/k)/math.log(reduction_factor)
    last_point = graphics.Point(loops*width/total_loops, height-(salesman(s)*height/innit_energy))
    graphics.update()
    time.sleep(2)
    while (k > k_min):
        loops += 1
        new_graph_point = graphics.Point(loops*width/total_loops, height-(salesman(s)*height/innit_energy))
        graph_line = graphics.Line(last_point, new_graph_point)
        graph_line.draw(graph)
        last_point = new_graph_point

        # CLEAR WINDOW SCREEN
        for item in win.items:
            item.undraw()
        # CREATE DRAWN OBJECTS
        pts = [graphics.Point(city.x, city.y) for city in s]
        circles = [graphics.Circle(pt, 15) for pt in pts]
        lines = []
        pt_last = pts[0]
        for pt in pts[1:]:
            lines.append(graphics.Line(pt_last, pt))
            pt_last = pt
        for circle in circles:
            circle.setFill("black")
            circle.draw(win)
        for line in lines:
            line.setWidth(3)
            line.draw(win)
        for i in range(repeat_num):
            s_new = neighbor(s, k)
            switch_prob = probability(s, s_new, k)
            # print(switch_prob, k)
            if switch_prob > random.random():
                # print(energy(s), "-->", energy(s_new))
                s = s_new
        k *= reduction_factor
        dist = graphics.Text(graphics.Point(width/2, height+10), str(round(salesman(s))))
        dist.draw(win)
        graphics.update()
        time.sleep(.035)

    # for k in reversed(range(2, 1000)):
    #     # print(s)
    #     s_new = neighbor(s, k)
    #     if probability(s, s_new, math.log(k)) > random.random():
    #         s = s_new
    # print(s)
    print("annealing finished")
    print(salesman(s))
    diff = innit_state-salesman(s)
    print("improvement = ", diff)
    print("percent improvement = ", (100-((salesman(s) / innit_state)*100)))
    time.sleep(5)
    win.close()
    graph.close()