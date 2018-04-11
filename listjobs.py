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
    jobs = p.getjobs()

    for id in jobs:
        try:
            np = jobs[id].Resource_List.nodes
            print np[0]
        except PBSError, detail:
            print detail
        pass

main()
