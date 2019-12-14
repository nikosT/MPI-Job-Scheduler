#!/bin/bash

# allocate workspace
#qsub -l walltime=10:00:00,nodes=clone1:ppn=8+clone2:ppn=8+clone3:ppn=8+clone4:ppn=8+clone5:ppn=8+clone6:ppn=8+clone9:ppn=8+clone8:ppn=8 /home/users/ntriantafyl/python_scheduler/scheduler.py


#sed -i 's/new_pol="compact"/new_pol="spare"/g' scheduler.py

#qsub -l nodes=clone10:ppn=8+clone1:ppn=8+clone2:ppn=8+clone3:ppn=8+clone4:ppn=8+clone5:ppn=8+clone6:ppn=8+clone7:ppn=8+clone9:ppn=8 /home/users/ntriantafyl/python_scheduler/scheduler.py
qsub -l nodes=clone10:ppn=8+clone1:ppn=8+clone2:ppn=8+clone3:ppn=8+clone4:ppn=8+clone13:ppn=8+clone14:ppn=8+clone15:ppn=8+clone16:ppn=8 /home/users/ntriantafyl/python_scheduler/scheduler.py

