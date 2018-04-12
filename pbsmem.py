#!/usr/bin/env python
#
# Author: Martin Souchal <souchal@apc.in2p3.fr>
# Date  : 12 avril 2018
# Desc. : CPU memory report for APC Cluster
#
#
#
#
import pbs
from PBSQuery import PBSQuery
from PBSQuery import PBSError
import sys
import re

def countmem(queue):
    p = PBSQuery()
    p.new_data_structure()
    jobs = p.getjobs()
    nptot = 0
    for id in jobs:
        if jobs[id].queue == [queue]:
            try:
                np = jobs[id].Resource_List.mem
                np = np[0][:-2]
                np = int(np)
                nptot = nptot + np
            except PBSError, detail:
                print detail
            pass
    return nptot

def countppn(queue):
    p = PBSQuery()
    p.new_data_structure()
    nodes = p.getnodes()
    nptot = 0
    for id in nodes:
        try:
            if nodes[id].properties[0] == queue :
                np = nodes[id].status.physmem[0]
                np = np[:-2]
                np = int(np)
                np = np/1000000
                nptot = np + nptot
        except PBSError, detail:
            print detail
        pass
    return nptot

def main():
    print "CPU memory usage in Gb [ reserved / available ] : "
    p = PBSQuery()
    queues = p.getqueues()
    for queue in queues.keys():
        np = countmem(queue)
        npp = countppn(queue)
        print "%s : [ %s / %s ] " % (queue,np,npp)

main()
