import threading
import time
import visual as vs
from visual.graph import *


class TSPScoreViewer(threading.Thread):
    '''
    Some score (route length) curves for each solvers are drawn in a graph.
    At least one solver have to be set to the instance of this class.
    '''
    def __init__(self, draw_interval=1.0):
        super(TSPScoreViewer, self).__init__()
        self.solvers = []
        self.score_curves = []
        self.score_window = gdisplay(title='TSP Score Viewer',
                                     xtitle='iteration', ytitle='Score(Route Length)' )
        self.setDaemon(True)
        self.stop_event = threading.Event()
        self.draw_interval = draw_interval
        return

    # This is for stopping the thread from outsides, but this doesn't work correct.
    def stop(self):
        self.stop_event.set()
        self.join()

    def add_solver(self, solver):
        self.solvers.append[solver]

    def run(self):
        self.score_graph = gcurve(color=vs.color.white)
        x_score = 0
        while not self.stop_event.is_set():
            route_points_list = self.solver.gen_route_points_list()
            self.draw_route(route_points_list)
            self.score_graph.plot(display=self.score_window,
                                  pos=(x_score, self.solver.cur_score))
            x_score += 1
            vs.rate(1.0/self.draw_interval)
        #self.route_window.visible = False
        #del self.route_window
        exit(0)


if __name__ == '__main__':
    nodes = [None, (0,0), (0,1), (1,1), (1,0)]
    route_points_list = [(0,0), (0,1), (1,1), (1,0), (0,0)]
    viewer = TSPViewer()
    viewer.set_node_list(nodes)
    viewer.draw_node_list(.1)
    viewer.draw_route(route_points_list)
    time.sleep(3)
    route_points_list = [(0,0), (1,1), (0,1), (1,0), (0,0)]
    viewer.draw_route(route_points_list)
