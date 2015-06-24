# -*- coding: utf-8 -*-

import sys
import codecs
import re
import normalizer

class FormatGenerator:
  def __init__(self, _word, _ruby):
    self.word = _word
    self.ruby = _ruby
    self.cost = int(max(-36000, -400 * (len(self.word)**(1.5))))
  def getFormat(self):
    s = u'' + self.word + \
        u',,,' + str(self.cost) + \
        u',名詞,固有名詞,*,*,*,*,*,*,*,'+self.ruby+','+self.ruby
    return s

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  if argc == 3:
    f = codecs.open(argvs[1],'r','UTF-8')
    fw = codecs.open(argvs[2], 'w','UTF-8')
    while True:
      line = f.readline()
      if not line:
        break
      line = line.rstrip()
      if re.match(u'([ ]+)|(一覧)', line):
        pass
      else:
        pair = line.split('\t',1)
        word = normalizer.normalize_neologd(pair[0])
        ruby = normalizer.normalize_neologd(pair[1])
        fg = FormatGenerator(word,ruby)
        fmt = fg.getFormat()
        print fmt
        fw.write(fmt+'\n')
