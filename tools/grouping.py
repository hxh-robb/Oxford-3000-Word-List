#!/usr/bin/env python
from __future__ import print_function
import os

__pardir = os.path.dirname

TOOLS_DIR = __pardir(os.path.realpath(__file__))
ROOT_DIR = __pardir(TOOLS_DIR)
SOURCE_WORDLIST_FILENAME = 'Oxford 3000 Word List.txt'
DEST_WORDLIST_FILENAME = 'Oxford 3000 Word List Grouped.txt'

EXCEPTION = ['united','wing', 'use', 'used', 'armed', 'bed', 'camping', 'cell phone', 'early', 'evening', 'feed', 'nothing', 'only']
CUSTOM = ['businessman', 'fully', 'breathing', 'curly', 'dying','riding','skilful', 'skilfully', 'frighten away/off']

def grouping():
  os.chdir(ROOT_DIR)
  
  group = {}
  with open(SOURCE_WORDLIST_FILENAME) as src:
    for word in src:
      word = word.rstrip('\n')
      if word in CUSTOM  or word in group:
        continue
      if word in EXCEPTION:
        group[word] = [word]
        continue
      if ' ' in word:
        key = word.split(' ')[0]
        if key in group:
          group[key].append(word)
          continue
      elif 'ly' == word[-2:] or 'ed' == word[-2:]:
        key = word[:-2]
        if key in group:
          group[key].append(word)
          continue
        elif key + 'e' in group:
          group[key + 'e'].append(word)
          continue
        elif 'tional' == key[-6:] and key[:-2] in group:
          group[key[:-2]].append(word)
          continue
        elif 'ing' == key[-3:] and key[:-3] in group:
          group[key[:-3]].append(word)
          continue
      elif 'ing' == word[-3:]:
        key = word[:-3]
        if key in group:
          group[key].append(word)
          continue
        elif key + 'e' in group:
          group[key + 'e'].append(word)
          continue
        elif key[:-1] in group:
          group[key[:-1]].append(word)
          continue
      elif 'tional' == word[-6:]:
        key = word[:-2]
        if key in group:
          group[key].append(word)
          continue
      group[word] = [word]
  
  end_with_ied = [ x for x in group if (' ' not in x and 'ied' == x[-3:]) ]
  for word in end_with_ied:
    if (word[:-3] + 'y') in  group:
      del group[word]
      group[(word[:-3] + 'y')].append(word)

  group['business'].append('businessman')
  group['full'].append('fully')
  group['breathe'].append('breathing')
  group['curl'].append('curly')
  group['die'].append('dying')
  group['ride'].append('riding')
  group['skill'].append('skilful')
  group['skill'].append('skilfully')
  group['use'].append('used')
  group['frighten'].append('frighten away')
  group['frighten'].append('frighten off')

  with open(DEST_WORDLIST_FILENAME, 'w') as f:
    for key in sorted(group, key=lambda x:x.lower()):
      print(', '.join(group[key]),file=f)
      #print(', '.join(group[key]))

def main():
  grouping()

if __name__ == '__main__':
  main()
