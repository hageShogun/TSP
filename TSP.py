'''
- Parse TSPLib problem and store it (Problem name, dimension, node list)
- If you want to store optimum route, run 'parse_opt_route' method
- Format assumption is below.
  ---------------------
  NAME: att48
  COMMENT : xxx
  TYPE : TSP
  DIMENSION : 48
  EDGE_WEIGHT_TYPE : ATT
  NODE_COORD_SECTION
  1 x1 y1
  2 x2 y2
  ...
  48 x48 y48
  EOF
  ---------------------
'''

import re
import math

class TSP:
    def __init__(self):
        self.name = None
        self.dim = None
        self.nodes = None # CAUTION: nodes[0] has no meaning. [(x1,y1), (x2,y2),...(xn,yn)]
        self.opt_route = []
        self.opt_route_length = None
        self.max_x = -1
        self.max_y = -1
        return

    def parse_problem(self, problem_name):
        pattern_name = re.compile('NAME\s*: (.+)')
        pattern_dim = re.compile('DIMENSION\s*: (.+)')
        pattern_node_coord = re.compile('(\d+) (\d+\.*\d*) (\d+\.*\d*)')

        line_num = 0
        with open(problem_name + '.tsp') as tsp:
            line = tsp.readline() # NAME:
            line_num += 1
            # parse NAME tag
            m = pattern_name.match(line)
            if m:
                self.name = m.group(1)
            else:
                print self.print_parse_error("NAME", line_num)
            # skip COMMENT tag
            line = tsp.readline() # COMMENT:
            line_num += 1
            # skip TYPE tag
            line = tsp.readline() # TYPE:
            line_num += 1
            # parse DIMENSION tag
            line = tsp.readline() # DIMENSION:
            line_num += 1
            m = pattern_dim.match(line)
            if m:
                self.dim =  int(m.group(1))
                self.nodes = ['None'] * (self.dim + 1) # +1 for discarding nodes[0]
            else:
                print self.print_parse_error("DIMENSION", line_num)

            line = tsp.readline() # EDGE_WEIGHT_TYPE:
            line_num += 1
            line = tsp.readline() # NODE_COORD_SECTION:
            line_num += 1

            # CAUTION:
            # node id start from '1',  NOT '0' !!
            while True:
                line = tsp.readline()
                line_num += 1
                if line == "EOF\n": break
                m = pattern_node_coord.match(line)
                if m:
                    i, x, y = int(m.group(1)), float(m.group(2)), float(m.group(3))
                    self.nodes[i] = ( x, y )
                    if self.max_x < x:
                        self.max_x = x
                    if self.max_y < y:
                        self.max_y = y
                else:
                    print self.print_parse_error("num num num", line_num)                
                    
        return True


    def parse_opt_route(self, problem_name):
        with open(problem_name + '.opt.tour') as tsp_opt:
            # skip header lines
            buf = None
            while buf != 'TOUR_SECTION\n':
                buf = tsp_opt.readline()
            '''
            if buf != 'TOUR_SECTION\n':
                print "ERROR: Opt route file may be unexpected format."
                exit(1)                
            '''
            # parse optimum node list
            for i in range(self.dim):
                line = tsp_opt.readline()
                if line == -1 or line == "EOF":
                    print "ERROR: Opt route file may be unexpected format."
                    exit(1)
                self.opt_route.append(int(line))
        if len(self.opt_route) != self.dim:
            print "ERROR: Opt route file may be unexpected format."
            exit(1)
        self.opt_route_length = self.calc_route_length(self.opt_route)
        return True

    # The 'route_order' is a traveling node order list, such as [1,3,4,5,2]
    def calc_route_length(self, route_order):
        route_length = 0
        for i in range(self.dim-1):
            x = self.nodes[route_order[i]][0] - self.nodes[route_order[i+1]][0]
            y = self.nodes[route_order[i]][1] - self.nodes[route_order[i+1]][1]
            route_length += math.sqrt(x*x + y*y)
        # path from end to start point
        x = self.nodes[route_order[self.dim-1]][0] - self.nodes[route_order[0]][0]
        y = self.nodes[route_order[self.dim-1]][1] - self.nodes[route_order[0]][1]
        route_length += math.sqrt(x*x + y*y)        
        return route_length

    def dump_tsp(self):
        print "NAME: %s" % self.name
        print "DIM: %d" % self.dim
        self.dump_nodes()

    def dump_nodes(self):
        for node in self.nodes:
            print node

    def print_parse_error(self, expected, line_num):
        print "parse error: %s is expected in line %d" % (expected, line_num)

### END OF CLASS ###

if __name__ == '__main__':
    import sys

    argv = sys.argv
    argc = len(argv)
    if argc != 2:
        print "Usage: python %s <tsp_name>" % argv[0]
        exit(1)

    tsp = TSP()
    tsp.parse_problem(argv[1])
    tsp.parse_opt_route(argv[1])
    tsp.dump_tsp()
    print tsp.opt_route
    

