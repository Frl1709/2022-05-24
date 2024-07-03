import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.listGeneri = []

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.idMap = {}

        self.bestPath = []

        self.loadGeneri()

    def getBestPath(self, v0, memoriaMax):
        self.bestPath = []

        parziale = [v0]
        rimanenti = []
        connessa = self.getConnessa(v0)
        tmp = DAO.getRimanenti(v0.GenreId, v0.MediaTypeId)
        for t in tmp:
            if t in connessa and t != v0:
                rimanenti.append(t)

        self._ricorsione(parziale, rimanenti, memoriaMax)

        return self.bestPath

    def _ricorsione(self, parziale, rimanenti, memoriaMax):
        if self.getSize(parziale) > memoriaMax:
            return

        if len(parziale) > len(self.bestPath):
            self.bestPath = copy.deepcopy(parziale)

        for n in rimanenti:
            if n not in parziale and self.getSize(parziale) + n.Bytes <= memoriaMax:
                parziale.append(n)
                self._ricorsione(parziale, rimanenti, memoriaMax)
                parziale.pop()

    def getSize(self, lista):
        size = 0
        for i in lista:
            size += i.Bytes
        return size

    def loadGeneri(self):
        self.listGeneri = DAO.getGeneri()

    def builGraph(self, genere):
        self.graph.clear()
        self.nodes = DAO.getNodes(genere.GenreId)
        self.graph.add_nodes_from(self.nodes)
        for n in self.nodes:
            self.idMap[n.TrackId] = n

        tmp = DAO.getEdge(genere.GenreId, self.idMap)
        for edge in tmp:
            delta = abs(edge[2] - edge[3])
            self.edges.append((edge[0], edge[1], delta))
            self.graph.add_edge(edge[0], edge[1], weight=delta)

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)

    def getMaxDelta(self):
        tmp = sorted(self.edges, key=lambda x: x[2], reverse=True)
        maxDelta = tmp[0][2]
        tmp2 = []
        for e in tmp:
            if e[2] == maxDelta:
                tmp2.append(e)
        return tmp2

    def getConnessa(self, v0):
        conn = list(nx.node_connected_component(self.graph, v0))
        return conn
