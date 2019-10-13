#!/usr/bin/python3

class Job:
    def __init__(self, id, app, procs, nodes, cores, time=0):
        """
        Basic Constructor of Job Class
        """
        self.id = id
        self.app = app
        self.procs = procs
        self.nodes = nodes
        self.cores = cores
        self.time = time
        self.type = None

    def __str__(self):
        return str(self.id)+"\t: "+self.app+"\t: "+str(self.procs)+\
        "\t  \t: "+str(self.nodes)+"\t: "+str(self.cores)+"\t: "+str(self.time)
