import random
import math
import threading
import TSP
import TSPViewer
import visual as vs


class TSPSolver_SA(threading.Thread):
    def __init__(self, gamma=0.99):
        super(TSPSolver_SA, self).__init__()
        self.tsp = TSP.TSP()
        self.cur_state = None # state = [1,3,5,2,4], that is the traveling node order.
        self.cur_score = None
        self.temperature = 1.0
        self.stop_temperature = 0.0001
        self.gamma = gamma
        self.iter_per_temp = 100
        return

    def init_solver(self, problem_name):
        # parse problem and initial state
        self.tsp.parse_problem(problem_name)
        self.tsp.parse_opt_route(problem_name)
        # initialize state
        state = range(1, self.tsp.dim+1) # [1,2,3,...dim] 
        random.shuffle(state)
        self.cur_state = state
        self.cur_score = self.tsp.calc_route_length(self.cur_state)


    # or-opt
    # TODO:state' = f(state)
    def gen_neighborhood(self, mode):
        dim = self.tsp.dim
        tmp_state = self.cur_state[:]
        i = random.randint(0, dim-1)
        j = random.randint(0, dim-1)
        while i == j:
            j = random.randint(0, dim-1)

        if mode == 'or-opt':
            tmp_state[i], tmp_state[j] = tmp_state[j], tmp_state[i]
        elif mode == '2-opt':
            tmp_state[i:j+1] = list(reversed(tmp_state[i:j+1]))
        return tmp_state

    # TODO: maximize or minimize problem
    def accept_state(self, neighborhood_score):
        energy_diff = neighborhood_score - self.cur_score
        if energy_diff < 0:
            return True
        elif self.random_acceptance(energy_diff):
            return True
        else:
            return False

    def random_acceptance(self, energy_diff):
        p = math.exp(-energy_diff/self.temperature)
        if random.random() < p:
            return True
        else:
            return False

    def update_temperature(self):
        self.temperature = self.gamma * self.temperature


    def hill_climbing(self, mode):
        i, i_max= 0, 100000
        while i < i_max:
            neighborhood = self.gen_neighborhood(mode)
            neighborhood_score = self.tsp.calc_route_length(neighborhood)
            if neighborhood_score < self.cur_score:
                self.cur_state = neighborhood[:]
                self.cur_score = neighborhood_score
                print "state is updated at %d, score:%f" % (i, self.cur_score)
            i += 1
        return

    def sa_climbing(self, mode, debug_print=False):
        while self.temperature > self.stop_temperature:
            # search 100 times in an temperature
            for i in range(self.iter_per_temp):
                neighborhood = self.gen_neighborhood(mode)
                neighborhood_score = self.tsp.calc_route_length(neighborhood)
                if self.accept_state(neighborhood_score):
                    self.cur_state = neighborhood[:]
                    self.cur_score = neighborhood_score
                    if debug_print == True:
                        print "state is updated at %d (T=%f), score:%f"\
                            % (i,self.temperature, self.cur_score)
            self.update_temperature()
        return

        
    def dump_state(self, dump_state=False):
        print "score: %f" % self.cur_score,
        if dump_state:
            print "\tstate: %s" % self.cur_state
        else:
            print '\n',

    # Generate the list such as [(x1,y1), (x2,y2), (x3,y3)...] for drawing a route.
    def gen_route_points_list(self, opt=False):
        route_list = None
        if opt == True:
            route_list = self.tsp.opt_route
        else:
            route_list = self.cur_state
        route_points_list = []
        for i in route_list:
            route_points_list.append(self.tsp.nodes[i])
        # make a circle
        route_points_list.append(self.tsp.nodes[route_list[0]])
        return route_points_list

if __name__ == '__main__':
    import sys

    argv = sys.argv
    argc = len(argv)
    if argc != 2:
        print "Usage: python %s <tsp_name>" % argv[0]
        exit(1)

    # initialize solver
    solver = TSPSolver_SA()
    solver.init_solver(argv[1])

    # initialize viewer
    viewer = TSPViewer.TSPViewer(0.05, solver)
    viewer.set_node_list(solver.tsp.nodes)
    viewer.draw_node_list(solver.tsp.max_x/150.0)
    # Draw optimum route
    #opt_route_points_list = solver.gen_route_points_list(True)
    #viewer.draw_opt_route(opt_route_points_list)

    # run main SA and viewer
    viewer.start()
    #solver.hill_climbing('or-opt')
    solver.sa_climbing('2-opt', False)
    print "Final score: {} by {}".format(solver.cur_score, solver.cur_state)
    opt = solver.tsp.opt_route_length
    print "Optimality={}(opt_score={}).".format(1.0 - (solver.cur_score-opt)/opt,opt)

    # The below line don't work correctly. Vpython runs a thread automatically and
    # I can't control it well ... why ?
    viewer.stop() 


