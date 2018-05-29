from __future__ import print_function
import os, random
import re, urllib, hashlib, subprocess
import itertools, time

debug = True

app_root = os.path.dirname(os.path.dirname(__file__))

oxford3k_filename = 'Oxford 3000 Word List.txt'
shuffled_filename = 'wordlist.txt'

mp3_dirname = 'mp3'
mp3_download_link = 'https://text-to-speech-demo.ng.bluemix.net/api/synthesize?text={0}&voice=en-GB_KateVoice&download=true&accept=audio%2Fmp3'

track_dirname = 'tracking'
track_day_dirname = 'day{}'

def file_path(filename,parent_dir=app_root):
  return '{}/{}'.format(parent_dir, filename)

def rmtree(name):
  path = file_path(name)
  if os.path.isdir(path):
    for entry in os.walk(path, topdown=False):
      for f in entry[2]:
        p = file_path(f,entry[0]) 
        if os.path.isfile(p):
          os.remove(p)
      for d in entry[1]:
        p = file_path(d,entry[0])
        if os.path.isdir(p):
          os.rmdir(p)
      os.rmdir(entry[0])
  elif os.path.isfile(path):
    os.remove(path)

def reset():
  rmtree(shuffled_filename)
  rmtree(mp3_dirname)
  rmtree(track_dirname)

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

def download(text, play_mp3=False):
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
  elif 0 != rt and os.path.exists(mp3):
    os.remove(mp3)

def play(mp3):
  subprocess.call(['ffplay', '-autoexit', '-nodisp', '-loglevel', '8', mp3])

def pick_words(num=10):
  shuffle()
  track_dir = file_path(track_dirname)
  if not os.path.exists(track_dir):
    os.mkdir(track_dir)

  day_dirnames = [ day_dirname for day_dirname in os.listdir(track_dir) if os.path.isdir(file_path(day_dirname,track_dir)) and re.match(r'day[\d]+', day_dirname) ]
  day_dirnames.sort()

  day = 0
  count = 0
  if day_dirnames:
    day = int(day_dirnames[-1].replace('day',''))
    for dirname in day_dirnames:
      try:
        day_dir = file_path(dirname, track_dir)
        count += int(subprocess.check_output(['wc', '-l', file_path('list.txt', day_dir)]).split(' ')[0])
      except:
        pass

  day_dirname = 'day%03d' % (day + 1)
  day_dir = file_path(day_dirname, track_dir)
  os.mkdir(day_dir)
  shu_list = file_path(shuffled_filename)
  day_list = file_path('list.txt', day_dir)
  with open(shu_list) as shu:
    with open(day_list,'w') as f:
      for x in itertools.islice([ word.rstrip('\n') for word in shu ], count, count + num ):
        print(x, file=f)
  play_list(day_dirname,0)

def play_list(day_dirname, interval=5):
  track_dir = file_path(track_dirname)
  if not os.path.exists(track_dir):
    pass
  day_dir = file_path(day_dirname, track_dir)
  day_list = file_path('list.txt', day_dir)
  if not os.path.isdir(day_dir) or not os.path.exists(day_list):
    pass
  with open(day_list) as f:
    wl = [ word.rstrip('\n') for word in f] 
    random.shuffle(wl)
    for word in wl:
      download(word.rstrip('\n'),True)
      time.sleep(interval)
