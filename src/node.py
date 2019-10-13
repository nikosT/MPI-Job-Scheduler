#!/usr/bin/python

class Node:
    def __init__(self, name, sockets=2, cores=4):
        """
        Basic Constructor of Node Class
        """
        self.name=name
        self.sockets=sockets
        self.cores=cores
        self.jobs=[None]*self.sockets
        self.dedicated=False


    def is_empty(self):
        """
        Return True if no jobs are running
        """
        if len([job for job in self.jobs if job==None]) == self.sockets:
            return True
        return False


    def is_half_empty(self):
        """
        Return True if half sockets are empty
        """
        if (len([job for job in self.jobs if job==None]) == (self.sockets/2)) and not self.dedicated:
            return True
        return False


    def free_socket(self):
        """
        Return the index of a free socket
        """
        for i,job in enumerate(self.jobs):
            if job==None:
                return i
        return False


    def __str__(self):
        s=""
        for soc in range(self.sockets):
            s+=self.name + "\t: " + str(soc) + "\t: " + (str(self.jobs[soc] or (self.dedicated and "dedicated") or "")) + '\n'
            
        return s[:-1]

