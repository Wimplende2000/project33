from CS312Graph import *
import time
import math

class NetworkRoutingSolver:
    def __init__( self):
        self.shortestPaths = {}
        self.network = None
        self.source = None
        self.dest = None

    def initializeNetwork(self, network):
        assert(type(network) == CS312Graph)
        self.network = network
    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        dist = {}
        prev = {}
        for node in self.network.nodes:
            dist[node.node_id] = math.inf
            prev[node] = ""
        dist[self.source] = 0

        if use_heap:
            queue = HeapPriorityQueue()
        else:
            queue = ArrayPriorityQueue()

        for node in self.network.nodes:
            queue.insert((dist[node.node_id], node))

        while not queue.is_empty():
            _, origin = queue.delete_min()
            if origin.node_id == -1:
                break
            for neighbor in origin.neighbors:
                alt = dist[origin.node_id] + neighbor.length
                if alt < dist[neighbor.dest.node_id]:
                    dist[neighbor.dest.node_id] = alt
                    prev[neighbor.dest] = neighbor
                    queue.decrease_key(neighbor.dest, alt)

        self.shortestPaths = {"distances": dist, "previous": prev}
        t2 = time.time()
        return (t2-t1)

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.dest]
        prev = self.shortestPaths["previous"]
        edge = prev[node]
        if edge == "":
            total_length = float('inf')
        while edge != "":
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length
            node = edge.src
            edge = prev[node]
        return {'cost':total_length, 'path':path_edges}
class ArrayPriorityQueue:
    def __init__(self):
        self.data = []

    def insert(self, item):
        self.data.append(item)

    def delete_min(self):
        min_index = 0
        for i in range(1, len(self.data)):
            if self.data[i][0] < self.data[min_index][0]:
                min_index = i
        return self.data.pop(min_index)

    def decrease_key(self, node, new_dist):
        for i, (dist, n) in enumerate(self.data):
            if n == node:
                self.data[i] = (new_dist, node)
                break
    def is_empty(self):
        return len(self.data) == 0
class HeapPriorityQueue:
    def __init__(self):
        self.data = []
        self.node_positions = {}
    def insert(self, item):
        self.data.append(item)
        self.node_positions[item[1]] = len(self.data) - 1
        self._sift_up(len(self.data) - 1)

    def delete_min(self):
        min_item = self.data[0]
        last_item = self.data.pop()
        if self.data:
            self.data[0] = last_item
            self.node_positions[last_item[1]] = 0
            self._sift_down(0)
        self.node_positions.pop(min_item[1])
        return min_item

    def decrease_key(self, node, new_dist):
        i = self.node_positions[node]
        self.data[i] = (new_dist, node)
        self._sift_up(i)

    def _sift_up(self, i):
        while i > 0 and self.data[i][0] < self.data[(i - 1) // 2][0]:
            self._swap(i, (i - 1) // 2)
            i = (i - 1) // 2

    def _sift_down(self, i):
        size = len(self.data)
        while 2 * i + 1 < size:
            j = 2 * i + 1
            if j + 1 < size and self.data[j + 1][0] < self.data[j][0]:
                j += 1
            if self.data[i][0] <= self.data[j][0]:
                break
            self._swap(i, j)
            i = j

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.node_positions[self.data[i][1]] = i
        self.node_positions[self.data[j][1]] = j

    def is_empty(self):
        return len(self.data) == 0
