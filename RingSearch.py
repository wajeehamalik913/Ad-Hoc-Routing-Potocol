from mpi4py import MPI
import numpy as np
from random import randrange
import time
import random
import sys
import re
import networkx as nx
from networkx.generators.random_graphs import erdos_renyi_graph
import time
start_time = time.time()

path = [] ## maintains path from source to destination if found within TTL
ttl = 10   ## Time to live initial value
temp = ttl
destination = 41 #Destination node fixed temporarily

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()
c=0

if (rank == 0): ## Source Node

    a=0
    file3 = open('topology.txt', 'r')
    Line1 = file3.readlines()
    count = 0
    NewList = []
    rNewList = []
    List = []
    for line in Line1:
        count += 1
        x = line.split(',')
        for i in range(len(x)):
            x[i]=x[i].replace('(', '')
            x[i]=x[i].replace(')', '')
            NewList.append(int(x[i]))
            
    rNewList =  NewList[::-1]
    NewList.extend(rNewList)
    #print("NEW LIST", NewList)
    print("I am process (source):", rank)
    print("My neighbours are:")
    for i in range (int(len(NewList)/2)):
        if NewList[a] == rank:
            List.append(NewList[a+1])
            print(List[i])
        a=a+2
    a=0
    ran=random.randint(0,len(List)-1)
    print("RANDOM NEUGHBOUR LIST(INDEX)", List[ran])
    print("TTL:", ttl)
    comm.send(ttl, dest=List[ran])
    print(rank ,"sending message to :", List[ran])

##    ## Recieving signal that time to live expired without
##    ## reaching the destination. Incrementing TTL value by 2
##    
    data2 = comm.recv(source=MPI.ANY_SOURCE)
    ttl = temp+20
    print("TTL=temp+2:" , ttl)
##    
##    ## selects new neighbouring node and sends increased time to live.
##    
    ran=random.randint(0,len(List)-1)
    print(rank ,"sending message to :", List[ran])
    comm.send(ttl, dest=List[ran])
    
##
else:

    a=0
    file3 = open('topology.txt', 'r')
    Line1 = file3.readlines()
    count = 0
    NewList = []
    rNewList = []
    List = []
    for line in Line1:
        count += 1
        x = line.split(',')
        for i in range(len(x)):
            x[i]=x[i].replace('(', '')
            x[i]=x[i].replace(')', '')
            NewList.append(int(x[i]))
            
    rNewList =  NewList[::-1]
    NewList.extend(rNewList)
    #print("NEW LIST", NewList)
    print("I am process:", rank)
    print("My neighbours are:")
    for i in range (int(len(NewList)/2)):
        if NewList[a] == rank:
            List.append(NewList[a+1])
            #print(List[i])
        a=a+2
    a=0
    print("Neighbour List:", List)
    status = MPI.Status()
    data = comm.recv(source=MPI.ANY_SOURCE, status=status)
    if (rank == destination):
        print('**************DESTINATION REACHED**************')
        print("--- %s seconds ---" % (time.time() - start_time))
            #comm.Abort()
    print(rank , "got message from:", status.Get_source())
    ttl = data-1

    if (ttl == -1):
        print("sending to source")
        #comm.Abort()
        comm.send(9, dest=0)
##        data2 = comm.recv(source=MPI.ANY_SOURCE, status=status)
##        print("New TTL:", data2)
    if (ttl >= 0 ):
        print("TTL:" , ttl)
##    #print("Path:", path)
##    print(rank , "got message from:", status.Get_source())
##
    ## Randomly selects which neighbour
    ## to send data and takes a particular path
    
    ran=random.randint(0,len(List)-1)
    
    ## it checks that the randomly selected node is 
    ## not the parent node from which it received message
    
    while ( List[ran] == status.Get_source() ):
        ran=random.randint(0,len(List)-1)

    #sends message to a neighbour   
    comm.send(ttl, dest=List[ran])
    
    
##    
##    print(rank ,"sending message to :", int(list[ran]))
##    if (int(list[ran]) == destination):
##        print("Destination reached", int(list[ran]) )
##        print("ABORTING FROM :" , destination)
##
##
