import random
import visual as vs

class TSPViewer:
    def __init__(self):
        self._nodes = None
        self.scene = vs.display(title='Travel Salesman Problem Solver Viewer',
                                autocenter=True)        
        return
        
    def set_node_list(self, node_list):
        self._nodes = node_list

    def draw_node_list(self):
        if self._nodes == None:
            print "ERROR: you have to set/load node list before drawing them."
            exit(1)
        
        
# Genral setting
vs.scene = vs.display(title='Travel Salesman Problem Solver Viewer', autocenter=True)
#scene.center = vector(0,0,0)


def gen_route(x, y):
    random.shuffle(x); random.shuffle(y)
    x.append(x[0]); y.append(y[0])
    return zip(x,y)

z = 0
n = 100
x,y  = range(n), range(n)
random.shuffle(x); random.shuffle(y)

# draw points
for i in range(100):
    vs.sphere(pos=vs.vector(x[i],y[i],0), radius=2, color=vs.color.blue)

while True:
    route_points = gen_route(x,y)
    route = vs.curve(pos=route_points)
    vs.rate(2)
    route.visible = False
    del route
    
