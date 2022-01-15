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

message = 100 ## message that floods between nodes
destination = 45 ##Destination node fixed temporarily
a=0
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()
c=0


if (rank == 0): ## Source Node

        a=0
        List = []
        file3 = open('topology.txt', 'r')
        Line1 = file3.readlines()
        count = 0
        NewList = []
        rNewList = []
        for line in Line1:
                count += 1
                x = line.split(',')
                for i in range(len(x)):
                        x[i]=x[i].replace('(', '')
                        x[i]=x[i].replace(')', '')
                        NewList.append(int(x[i]))
                
        rNewList =  NewList[::-1]
        NewList.extend(rNewList)
        print("NEW LIST", NewList)
        print("I am process (source):", rank)
        print("My neighbours are:")
        for i in range (int(len(NewList)/2)):
                if NewList[a] == rank:
                        List.append(NewList[a+1])
                        print(List[i])
                a=a+2
        a=0
        for i in range(len(List)):
                comm.send(message, dest=List[i])
                print(rank ,"sending message to :", List[i])

else:
	List = []
	send = []
	a=0
	file3 = open('topology.txt', 'r')
	Line1 = file3.readlines()
	count = 0
	NewList = []
	for line in Line1:
                count += 1
                x = line.split(',')
                for i in range(len(x)):
                        x[i]=x[i].replace('(', '')
                        x[i]=x[i].replace(')', '')
                        NewList.append(int(x[i]))

	rNewList =  NewList[::-1]
	NewList.extend(rNewList)
	print("I am process:", rank)
	print("My neighbours are:")

	for i in range (int(len(NewList)/2)):
                if NewList[a] == rank:
                        List.append(NewList[a+1])
                        #print(List[i])
                a=a+2

	a=0
	status = MPI.Status()
	data = comm.recv(source=MPI.ANY_SOURCE, status=status)
	send.append(status.Get_source())
	
	if (rank == destination):
                print('**************DESTINATION REACHED**************')
                print("--- %s seconds ---" % (time.time() - start_time))
                #comm.Abort()
	print(rank , "got message from:", status.Get_source())

        ## if destination is not reached message will continue flooding and
	## node receiving message will send message to its neighbouring nodes.
	for i in range(len(List)):
                if (List[i] == '0'):
                        continue
                if (len(List) == 1 and List[i] == str(status.Get_source())):
                        print("EXITING")
                        comm.Abort()
                cc = 0
                if(List[i] in send):
                        cc=cc+1
                        if cc==len(List):
                                comm.Abort()
                        
                if (List[i] != str(status.Get_source())):
                        if (list[i] == destination):
                                print("Destination reached", int(list[ran]) )
                                print("ABORTING FROM :" , destination)
                        comm.send(message, dest=List[i])
                        send.append(rank)
                        print(rank ,"sending message to :", List[i])
                        
