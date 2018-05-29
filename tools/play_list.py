#!/usr/bin/env python

import sys,re
import oxford3k

if __name__ == '__main__':
  day = 'day001'
  try:
    param = sys.argv[1]
    if re.match(r'day\d+',param) : day = param
  except:
    pass
  oxford3k.play_list(day, 3)
