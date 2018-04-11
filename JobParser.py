#!/usr/bin/env python
#
# Author:       Dennis Stam
# Date:         30 September 2014
# Description:  This is a very simple jobscript parser to fetch all #PBS arguments
#               and convert them to a attropl list which can be used for submission
#

import re
import sys
import argparse
import time
import pbs

class JobParser(object):
    '''A simple simple jobscript parser to fetch all #PBS arguments from the header'''

    job_script = None
    matcher = re.compile(r'\#PBS\s(?P<args>.+)')

    ## These are the arguments that exist in Torque
    pbs_attrs = {
        'a' : {
            'func': 'pbs_datetime',
            'args_opts': {
                'type': str,
            },
        },
        'A' : {
            'args_opts': {
                'type': str,
            },
        },
        # Checkpoint is not yet implemented
        #'c' : {
        #    'args_opts': {
        #        'type': str,
        #        'action': 'append',
        #    },
        #},
        'e' : {
            'args_opts': {
                'type': str,
            },
        },
        'F' : {
            'args_opts': {
                'type': str,
            },
        },
        'f' : {
            'args_opts': {
                'action' : 'store_true',
            },
        },
        'h' : {
            'args_opts': {
                'action' : 'store_true',
            },
        },
        'I' : {
            'args_opts': {
                'action' : 'store_true',
            },
        },
        'j' : {
            'args_opts': {
                'type': str,
                'choices': ['eo','oe','n'],
            },
        },
        'k' : {
            'args_opts': {
                'type': str,
                'choices' : ['e','o','eo','oe','n'],
            },
        },
        'l' : {
            'args_opts': {
                'type': str,
                'action': 'append',
            },
        },
        'm' : {
            'args_opts': {
                'type': str,
                'choices': ['a','b','e','n'],
            },
        },
        'M' : {
            'args_opts': {
                'type': str,
                'action': 'append',
            },
        },
        'N' : {
            'args_opts': {
                'type': str,
            },
        },
        'o' : {
            'args_opts': {
                'type': str,
            },
        },
        'p' : {
            'args_opts': {
                'type': int,
            },
        },
        'P' : {
            'args_opts': {
                'type': str,
            },
        },
        'q' : {
            'args_opts': {
                'type': str,
            },
        },
        'r' : {
            'args_opts': {
                'action' : 'store_true',
            },
        },
        'S' : {
            'args_opts': {
                'type': str,
                'action' : 'append',
            },
        },
        't' : {
            'args_opts': {
                'type': str,
            },
        },
        'u' : {
            'args_opts': {
                'type': str,
                'action' : 'append',
            },
        },
        'W' : {
            'args_opts': {
                'type': str,
                'action' : 'append',
            },
        },
    }

    def __init__(self, job_script=None):
        if hasattr(job_script, 'readlines'):
            self.job_script = job_script.readlines()

    def read(self, filename):
        try:
            with open(filename, 'r') as fi:
                self.job_script = fi.readlines()
        except IOError:
            error_str = "Jobscript filename does not exists: %s" %(filename)
            raise Exception(error_str)

    def __get_pbs_args(self):
        if not self.job_script:
            raise Exception("User function read to read from file")

        args = list()
        for line in self.job_script:
            if self.matcher.search(line.strip()):
                args.append(self.matcher.findall(line.strip())[0])
        return args

    def pbs_datetime(self, input):

        current_time, current_seconds = tuple(time.strftime('%Y%m%d%H%M.%S').split('.'))

        if len(input.strip()) == 12:
            return input.strip()
        elif len(input.strip()) == 10:
            return current_time[0:2] + input.strip()
        elif len(input.strip()) == 8:
            return current_time[0:4] + input.strip()
        elif len(input.strip()) == 6:
            return current_time[0:6] + input.strip()
        elif len(input.strip()) == 4:
            return current_time[0:8] + input.strip()

        return current_time

    def parse_pbs(self):
        '''Parse the arguments and check if they are using the correct format'''

        ## First create an arguments parser
        parser = argparse.ArgumentParser(add_help=False)
        for arg, options in self.pbs_attrs.items():
            parser.add_argument('-'+arg, **options['args_opts'])

        ## Parse the arguments that have been found in the jobscript
        args = parser.parse_args(self.__get_pbs_args())

        ## Create an dict with items we wan't to set, skip evrything which is None, empty of False
        process_args = dict()
        for k,v in args.__dict__.items():
            if v:
                if self.pbs_attrs.has_key(k) and self.pbs_attrs[k].has_key('func'):
                    try:
                        process_args[k] = getattr(self, self.pbs_attrs[k]['func'])(v)
                    except AttributeError as err:
                        raise Exception('Could not locate function')
                else:
                    if type(v) is type(list()):
                        value = list()
                        for x in v:
                            value.extend(x.strip().split(','))
                        process_args[k] = ",".join(value)
                    else:
                        process_args[k] = v.strip()
        return process_args

    def get_attropl(self):
        data = self.parse_pbs()

        ### First al the keys, except for --resource-list/-l
        ##  and perhaps more later
        length = len([ x for x in data.keys() if x not in ['l']])
        if data.has_key('l'):
            length += len(data['l'].split(','))

        attropl = pbs.new_attropl(length)
        index = 0

        for attr, value in data.items():
            if attr in ['l']:
                for v in value.split(','):
                    parts = v.split('=')
                    resource, value = parts[0], "=".join(parts[1:])
                    attropl[index].name = getattr(pbs, 'ATTR_'+attr)
                    attropl[index].resource = resource
                    attropl[index].value = value
                    index += 1
            else:
                attropl[index].name = getattr(pbs, 'ATTR_'+attr)
                attropl[index].value = value
                index += 1
        return attropl

if __name__ == '__main__':
    jp = JobParser()

    try:
        jp.read(sys.argv[1])
    except IndexError:
        print("Usage: %s <jobscript>" %(sys.argv[0]))
        sys.exit(1)
        

    server_name = pbs.pbs_default()
    con = pbs.pbs_connect(server_name)
    job_id = pbs.pbs_submit(con, jp.get_attropl(), sys.argv[1], 'batch', 'NULL')

    e, e_txt = pbs.error()
    if e:
        print(e, e_txt)
    else:
        print(job_id)
