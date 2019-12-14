#!/usr/bin/python
import random

# format example:
# cg.A.16 16 2 8 60

apps=['bt', 'cg', 'ep', 'ft', 'is', 'lu', 'mg', 'sp']
apps=['bt', 'cg', 'ep', 'is', 'lu', 'mg', 'sp'] # ft not in class A
apps=['mg', 'ep', 'sp']

classes=['B', 'C']
classes=['C'] #BYPASS
procs=['16']


def rand(apps, classes, procs, apps_num):

    for i in range(apps_num):

        x=random.randint(0,len(apps)-1)
        y=random.randint(0,len(classes)-1)
        z=random.randint(0,len(procs)-1)

        print apps[x]+'.'+classes[y]+'.'+procs[z] + ' ' + procs[z] + ' 2 8 60'



if __name__ == "__main__":


    rand(apps, classes, procs, 50)
