#!/usr/bin/env python
#
#  Copyright (c) 2011, Jesse Griffin <jesse@tummy.com>, tummy.com, ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#    Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.

help = '''  Load Opsview's status.dat into a python dictionary.

  Pass the file path of the log, default is /usr/local/nagios/var/status.dat.

  Returns a dictionary with this format:
    statusdict = {
        'host_name': {
            'host_attribute_desc1': 'attribute_value1',
             'host_attribute_desc2': 'attribute_value2',
             ...  etc.  ...
             }
        ( 'host_name', 'service_description' ): {
             'service_attribute_desc1': 'attribute_value1',
             'service_attribute_desc2': 'attribute_value2',
             ...  etc.  ...
             }
    }

  Use like this:
from read_opsview_log import *
statusdict = readlog()
'''

import os
import re
import sys
import string

def readlog(filepath = '/usr/local/nagios/var/status.dat'):
  '''Read Opsview status log.'''
  if not os.access(filepath, os.F_OK):
    print 'Could not access %s' % filepath
    sys.exit(1)

  # Load the file into a simple dictionary
  i = 0
  simpledict = {}
  logfh = open(filepath, 'r')
  for line in logfh.readlines():
    if '{' in line:
      i += 1
      simpledict[i] = {}
      continue
    if '=' in line:
      ( key, value ) = line.split('=', 1)
      if value:
        simpledict[i][key.strip()] = value.strip()
      else:
        print key
  logfh.close()

  # Turn simpledict into a smart dictionary
  statusdict = {}
  for k, v in simpledict.iteritems():
    properties = {}

    if not v.has_key('host_name'):
      continue

    if v.has_key('comment_id'):
      key = v['comment_id']
    elif v.has_key('service_description'):
      key = ( v['host_name'], v['service_description'] )
    else:
      key = v['host_name']

    for vk, vv in v.iteritems():
      properties[vk] = vv

    statusdict[key] = properties

  return statusdict


if __name__ == '__main__':
  print help
