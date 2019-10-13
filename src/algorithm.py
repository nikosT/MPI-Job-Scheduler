#!/usr/bin/python

# sp - ep 1
# sp - (compact) 2
# sp - mg 3
# sp - sp 4

# mg - ep 1
# mg - sp 2
# mg - (compact) 3
# mg - mg 4

# ep - ! (anyway)

# if mg: then eg
#        then sp
#        then alone or mg

# if sp: then ep
#        then compact

# if any=1: then compact

queue_file='./queue'


def pop(list):
    try:
        return list.pop(0)
    except:
        return None





# read queue of submitted apps
with open(queue_file) as f:
    lines = f.readlines()
# create a list of lists
queue=[[i, line.split('.')[0]] for i, line in enumerate(lines)]

# classification of types
mgs=[[i,app] for i,app in queue if app=='mg']
sps=[[i,app] for i,app in queue if app=='sp']
eps=[[i,app] for i,app in queue if app=='ep']


mgs=mgs[:0]
sps=sps[:2]
eps=eps[:11]

print '*'*120
for elem in queue:
    print elem


magic=[]
while True:

    # if MG
    _mg=pop(mgs)
    if _mg:
        # co-schedule with EP
        _ep=pop(eps)
        if _ep:
            magic.append([_mg[0], _mg[1], _ep[0], _ep[1]])
            continue

        # co-schedule with SP
        _sp=pop(sps)
        if _sp:
            magic.append([_mg[0], _mg[1], _sp[0], _sp[1]])
            continue

        # compact (alone) [if only one left]
        magic.append([_mg[0], _mg[1]])
        continue


    # if SP
    _sp=pop(sps)
    if _sp:
        # co-schedule with EP
        _ep=pop(eps)
        if _ep:
            magic.append([_sp[0], _sp[1], _ep[0], _ep[1]])
            continue

        # compact (alone) [if only one left]
        magic.append([_sp[0], _sp[1]]) 
        continue

    # if EP
    _ep=pop(eps)
    if _ep:
        # co-schedule with EP
        _ep2=pop(eps)
        if _ep2:
            magic.append([_ep[0], _ep[1], _ep2[0], _ep2[1]])
            continue

        # compact (alone) [if only one left]
        magic.append([_ep[0], _ep[1]]) 
        continue

    # if no jobs found in any of the 3 lists
    if (not mgs) and (not sps) and (not eps):
        break


print '*'*120
for elem in magic:
    print elem




