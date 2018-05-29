from __future__ import print_function
import os, random
import re, urllib, hashlib, subprocess
import itertools

debug = True

app_root = os.path.dirname(os.path.dirname(__file__))

oxford3k_filename = 'Oxford 3000 Word List.txt'
shuffled_filename = 'wordlist.txt'

mp3_dirname = 'mp3'
mp3_download_link = 'https://text-to-speech-demo.ng.bluemix.net/api/synthesize?text={0}&voice=en-GB_KateVoice&download=true&accept=audio%2Fmp3'

def file_path(filename,parent_dir=app_root):
  return '{}/{}'.format(parent_dir, filename)

def shuffle():
  o3k = file_path(oxford3k_filename)
  shu = file_path(shuffled_filename)
  if os.path.exists(o3k) and os.path.exists(shu):
    st_oxf3k = os.stat(o3k)
    st_words = os.stat(shu)
    if st_words.st_size != st_oxf3k.st_size:
      os.remove(shu)
  if not os.path.exists(shu):
    with open(o3k) as oxf3k:
      wordlist = [line.strip('\n') for line in oxf3k]
      random.shuffle(wordlist)
      with open(shu, 'w') as words:
        for line in wordlist:
          print(line, file=words)

def mp3(text, play_mp3=False):
  text = re.sub(r'[\.\,]', '\g<0> ', text).replace('  ', ' ')
  mp3_filename = hashlib.md5(text.encode()).hexdigest() + '.mp3'
  mp3_dir = file_path(mp3_dirname)
  if not os.path.exists(mp3_dir):
    os.mkdir(mp3_dir)
  mp3 = file_path(mp3_filename, mp3_dir)
  if os.path.exists(mp3):
    if play_mp3:
      play(mp3)
    return
  param = urllib.quote_plus(text)
  link = mp3_download_link.format(param)
  rt = subprocess.call(['wget', '-O' if debug else '-qO', mp3, link])
  if 0 == rt and play_mp3:
    play(mp3)
  elif os.path.exists(mp3):
    os.remove(mp3)

def play(mp3):
  subprocess.call(['ffplay', '-autoexit', '-nodisp', '-loglevel', '8', mp3])

#with open('{}/{}'.format(app_root,oxford3k_source_filename)) as f:
