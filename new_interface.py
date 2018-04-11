#!/usr/bin/env python
#
# Author: Bas van der Vlies <basv@sara.nl>
# Date  : 02 March 2005
# Desc. : Usage of the new PBSQuery module
#
# SVN info:
# $Id: new_interface.py 339 2015-03-10 16:55:29Z bas $
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

  #job = p.getjob('2983215')
  #print job['substate']
  #print job.substate
  #print job.queue
  #print job.Resource_List
  #print job.Resource_List.nodes 
  #print job.Resource_List.arch 
  #print job.Variable_List.PBS_O_HOME

  l = ['np', 'state' ]
  #node = p.getnode("r2n2", l)

  #print node.name
  #print node.name, node['np']

  #sys.exit(0)

  nodes = p.getnodes(l)
  for id in nodes:
	print id

	try:
		print nodes[id].np
		#print nodes[id].status.arch
		print nodes[id].status.uname
		print nodes[id].state
	except PBSError, detail:
		print detail
		pass
	
     #for attrib in nodes[id]:
     #	print attrib, nodes[id][attrib]

main()
