# -*- coding: utf-8 -*-

import subprocess
import glob
import sys

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  if argc == 3:
    dir_path = argvs[1]
    file_list = glob.glob(dir_path+'*')
    for fname in file_list:
      comm = u'PYTHONIOENCODING=utf-8 python extractRuby.py'
      comm = comm + ' ' + fname +' >> ' + argvs[2]
      print comm
      subprocess.call(comm, shell=True)
  else:
    print u'usage: [DIR contained wikipedia plane txt] [output FILE]'
