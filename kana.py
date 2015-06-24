# -*- coding: utf-8 -*-

import subprocess
import glob

dir_path = u'../wikipedia_plane/'
file_list = glob.glob(dir_path+'*')
for fname in file_list:
  comm = u'PYTHONIOENCODING=utf-8 python extractRuby.py'
  comm = comm + ' ' + fname +' >> out.txt'
  print comm
  #os.system(comm)
  subprocess.call(comm, shell=True)
