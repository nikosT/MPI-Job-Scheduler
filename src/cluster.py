#!/usr/bin/python
import node
import job
import os

class Cluster:
    def __init__(self, names, sockets=2, cores=4):
        """
        Basic Constructor of Cluster Class
        """
        self.cores=cores # cores per socket
        self.sockets=sockets # sockets per node
        self.jqueue=[] # list of submitted jobs
        self.rmanager='torque'
        self.queue_file='/home/users/ntriantafyl/python_scheduler/queue'
        self.app_dir='/home/users/ntriantafyl/NPB3.3.1/NPB3.3-MPI/bin/'
        self.rank_dir='/home/users/ntriantafyl/python_scheduler/rankfiles/'
        self.log_dir='/home/users/ntriantafyl/python_scheduler/log/'
        self.pid_dir='/home/users/ntriantafyl/python_scheduler/pid/'

        self.nodes=[]
        for name in names:
            self.nodes.append(node.Node(name, sockets, cores))

        # 3 temp lines:
        #self.queue_file='./queue'
        #self.rank_dir='./rankfiles/'
        #self.pid_dir='./pid/'


    def __str__(self):
        s="Cluster of [" + str(len(self.nodes)) + "] nodes with [" + str(self.sockets) + "] sockets, each of [" + str(self.cores) + "] cores\n"

        s+="-"*23+'\n'
        s+="Node\t: " + "Socket: " + "Job\n"
        s+="-"*23+'\n'

        for node in self.nodes:
            s+=str(node)+'\n\n'

        return s[:-1]


    def print_jobs(self):

        print "ID\t: Application\t: Processes\t: Nodes\t: Cores\t: Estimation Time"
        for job in self.jqueue:
            print job


    def read_queue(self):
        # read and return queue of submitted apps
        # e.g.: bt.A.16 16 4 4 30
        with open(self.queue_file) as f:
            lines = f.readlines()

        # for the time being, read only the name of the app
        # not number of requested nodes and cores (per node)
        for i,line in enumerate(lines):
            if line[0]=='\n':
                continue
            arr=line.split()
            if not arr[0][0]=='#':
                self.jqueue.append(job.Job(i, arr[0], arr[1], int(arr[2]), int(arr[3]), int(arr[4])))


    def map2rankfile(self, procs):
        """
        Generate the respective mpirun rankfiles
        according to cluster's infrastructure (nodes, cores, sockets)
        and application's size requested (procs)
        Important: Currently supports EXACTLY 2 sockets ONLY!
        Ranfile format:
        rankfile(avail_nodes)x(cores)_(slots with the 2nd socket) or F
        F: Full node, means that both sockets where used
        """    
        # create rankdir folder
        if not os.path.exists(self.rank_dir):
            os.makedirs(self.rank_dir)
    
        # if the cluster has only 1 socket per node
        # this means FULL Node case
        if self.sockets==1:
        
            # Case: FULL Node
            # Rankfile has the format name:
            # rankfile(avail_nodes)x(cores)_F
            node=0
            # find the size of neeeded nodes
            avail_nodes=procs/(self.sockets*self.cores)
            if avail_nodes <= self.nodes:
                rankfile='rankfile'+str(avail_nodes)+'x'+str(self.cores*self.sockets)+'_F'
                with open(os.path.join(self.rank_dir,rankfile), 'w') as f:  
                    for i in range(0,procs):
                        f.write("rank " + str(i) + "=+n" + str(node) + " slot=" + str(0) + ":" + str(i%self.cores)+'\n')
                        if (i+1)%(self.cores*self.sockets)==0:
                            node+=1
    
        # if the cluster has exactly 2 sockets per node
        else:
            # for the both cases
            # FULL or HALF Node
            for socket in range(1,self.sockets+1):
        
                # find the size of neeeded nodes
                avail_nodes=procs/(socket*self.cores)
        
                # check if the cluster is able to support the app size
                if avail_nodes <= self.nodes:
        
                        # Case: HALF Node
                        if socket==1:
                            # Create all the cases where the 2nd slot is used
                            # Rankfile has the format name:
                            # rankfile(avail_nodes)x(cores)_(slots with the 2nd socket)
                            for j in range(0,avail_nodes+1):
                                node=0
                                slot=0
                                rankfile='rankfile'+str(avail_nodes)+'x'+str(self.cores)+'_'+str(avail_nodes-j)
                                with open(os.path.join(self.rank_dir,rankfile), 'w') as f:  
                                    for i in range(0,procs):
                                        slot = 0 if i > procs-self.cores*j -1 else 1
                                        f.write("rank " + str(i) + "=+n" + str(node) + " slot=" + str(slot) + ":" + str(i%self.cores)+'\n')
                                        if (i+1)%(self.cores*socket)==0:
                                            node+=1
        
                        # Case: FULL Node
                        # Create all the cases where BOTH slots are used
                        # Rankfile has the format name:
                        # rankfile(avail_nodes)x(cores)_F
                        else:
                            node=0
                            slot=0
                            rankfile='rankfile'+str(avail_nodes)+'x'+str(self.cores*self.sockets)+'_F'
                            with open(os.path.join(self.rank_dir,rankfile), 'w') as f:  
                                for i in range(0,procs):
                                    f.write("rank " + str(i) + "=+n" + str(node) + " slot=" + str(slot%self.sockets) + ":" + str(i%self.cores)+'\n')
                                    if (i+1)%(self.cores*socket)==0:
                                        node+=1
                                    if (i+1)%(self.cores)==0:
                                        slot+=1

    def generate_rankfiles(self, job_list=[]):
        """
        Generate all the possible rankfiles needed by mpirun command
        for all applications and for the current cluster's properties
        """
        # if a job list is passed as a parameter
        if job_list:
            num_procs=[]
            for job in job_list:
                num_procs.append(job.procs)

        # otherwise, read the jobs from the queue file
        else:
            # read queue of submitted apps
            with open(self.queue_file) as f:
                lines = f.readlines()

            # get the number of processes requested
            num_procs=[]
            for line in lines:
                num_procs.append(line.split()[1])

        # generate the rankfiles
        for num_proc in num_procs:
            self.map2rankfile(int(num_proc))


    def find(self, policy, *args):
        """
        Return referenced nodes
        """
        if policy=='compact':
            nodes=filter(lambda node: node.is_empty(), self.nodes)
            node_num=int(args[0].procs)/(self.cores*self.sockets)

        elif policy=='spare':
            nodes=filter(lambda node: node.is_empty(), self.nodes)
            node_num=(int(args[0].procs)/(self.cores*self.sockets))*2
 
        elif policy=='strip':
            # firstly, choose the nodes that are completely empty
            nodes=filter(lambda node: node.is_empty(), self.nodes)
            # secondly, choose the nodes that are half empty
            nodes+=filter(lambda node: node.is_half_empty(), self.nodes)
            node_num=(int(args[0].procs)/(self.cores*self.sockets))*2

        # if resources are enough
        # return the min number of needed resources
        if node_num <= len(nodes):
            return nodes[:node_num]

        return []


    def submit(self, policy, *args):
        """
        Run the respective mpirun command
        """
        # find available nodes based on submitted policy
        nodes=self.find(policy, args[0])

        if policy=='compact' and nodes:
            for node in nodes:
                for i in range(len(node.jobs)):
                    node.jobs[i]=args[0]
                node.dedicated=True
            rankfile='rankfile'+str(len(nodes))+'x'+str(self.cores*self.sockets)+'_F'

        elif policy=='spare' and nodes:
            for node in nodes:
                node.jobs[node.free_socket()]=args[0]
                node.dedicated=True
            rankfile='rankfile'+str(len(nodes))+'x'+str(self.cores)+'_0'

        elif policy=='strip' and nodes:
            # how many nodes have been chosen for the submission where the socket=1
            len1=len(filter(lambda node: node.free_socket()==1, nodes))

            # prepape the host for the mpirun command
            # sort nodes by those who has the socket=1 free
            nodes.sort(key=lambda node: node.free_socket()==1, reverse=True)

            for node in nodes:
                node.jobs[node.free_socket()]=args[0]

            rankfile='rankfile'+str(len(nodes))+'x'+str(self.cores)+'_'+str(len1)

        else:
            return False

        names=[node.name for node in nodes]
        names=list(OrderedDict.fromkeys(names))
        hosts = "'"+','.join(names)+"'"
 
        self.mpirun(hosts, rankfile, args[0])

        return True
                

    def mpirun(self, hosts, rankfile, *args):

        job=args[0] # get the first job

        # create the output and error file of the job
        outfile=str(job.id)+'_'+job.app+'.o'
        errfile=str(job.id)+'_'+job.app+'.e'

        # bash parallel block
        # {
        # export needed env
        mpirun="{ export PATH=/home/users/ntriantafyl/openmpi-1.8.3/bin:$PATH; "

        # create pid file before starting mpirun
        mpirun+="echo '' > " + self.pid_dir + str(job.id) + " && "

        # run the job
        mpirun+="mpirun -np " + str(job.procs) + " -H " + hosts + " -v --report-bindings --timestamp-output --rankfile " + \
           self.rank_dir + rankfile + " --mca btl self,tcp " + self.app_dir + job.app + " >> " + self.log_dir + \
           outfile + " 2>> " + self.log_dir + errfile + " && "

        # delete pid file after finishing
        mpirun+="rm " + self.pid_dir + str(job.id) + "; } &"
        # }
        # end of bash parallel block

        #print hosts, rankfile, job
        print mpirun
        return subprocess.call(mpirun, shell=True)


    def free(self):
        """
        free processes
        """
        # get all running processes
        pids=[int(x) for x in os.listdir(self.pid_dir)]

        # check each node one by one
        for j, node in enumerate(self.nodes):
            # check each job one by one
            for i,job in enumerate(node.jobs):
                # if job is not found in pids
                # it means that it has been finished
                #if job:
                #    print node, job.id, pids
                #    if (not int(job.id) in pids):
                #        print "yes"
                if job and (not int(job.id) in pids):
                    # remove job
                    self.nodes[j].jobs[i]=None

            # if the node was dedicated and there are no jobs any more
            # then release dedication
            if node.is_empty() and node.dedicated:
                self.nodes[j].dedicated=False


    def is_empty(self):
        """
        Return True if no more jobs are running
        """
        pids=os.listdir(self.pid_dir)
        if pids:
            return False

        return True


    def run(self, policy):
        """
        Need to implement policies here
        """
        # classic RR policy
        while True:
            self.free()
            if self.jqueue:
                if self.submit(policy, self.jqueue[0]):
                    self.jqueue.pop(0)
                    print self

            if self.is_empty():
                break
