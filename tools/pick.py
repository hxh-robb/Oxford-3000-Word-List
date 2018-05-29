#!/usr/bin/env python

import sys
import oxford3k

if __name__ == '__main__':
  num = 10
  try:
    num = int(sys.argv[1])
  except:
    pass
  if num > 50:
    num = 50
  oxford3k.pick_words(num)
