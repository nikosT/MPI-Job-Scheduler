#!/usr/bin/python

from collections import OrderedDict
import sys, os, time, subprocess
sys.path.append('/home/users/ntriantafyl/python_scheduler/src')

import cluster
import generator



if __name__ == "__main__":


    cl=cluster.Cluster(['clone1', 'clone2', 'clone3', 'clone4', \
                'clone13', 'clone14', 'clone15', 'clone16'], 2, 4)


    cl.read_queue()
    cl.print_jobs()
    cl.generate_rankfiles(cl.jqueue)


        #print 'Starting to run in "' + policy + '" mode...'
        #start_time = time.time()
        #cl.run(policy)
        #cl.print_jobs()
        #print 'End of run. Total time: ' + str(round(time.time() - start_time,2))


