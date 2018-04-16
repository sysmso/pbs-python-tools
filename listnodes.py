#!/usr/bin/env python
#
# Author: Martin Souchal <souchal@apc.in2p3.fr>
# Date  : 20 oct 2016
# Desc. : CPU slot report for APC Cluster
#
#
#
#
import pbs
from PBSQuery import PBSQuery
from PBSQuery import PBSError
import sys

def main():

    p = PBSQuery()
    p.new_data_structure()
    nodes = p.getnodes()

    for id in nodes:
        try:
            #np = nodes[id].status.physmem[0]
            #queue = nodes[id].properties[0]
            #print np,queue
	    print nodes[id].status.loadave
            #print nodes[id].status.ncpus
            #if hasattr(nodes[id],"jobs"):
            #    for job in nodes[id].jobs :
            #        print job
        except PBSError, detail:
            print detail
        pass

main()
