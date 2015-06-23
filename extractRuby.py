# -*- coding: utf-8 -*-

import re
import codecs

class FuriganaExtractor:
  """"""
  title_regex = u''
  furigana_regex = u''
  title_prog = re.compile(title_regex, re.U)
  furigana_prog = re.compile(furigana_regex,re.U)
  def __init__(self, _filename):
    self.filename = _filename
    self.title_found = False
    self.body_found = False
    self.isComplete = False
    self.f = codecs.open(self.filename,'r','UTF-8')
  def nextPair(self):
    print 'nextPair'
  def isComplete(self):
    print 'isComplete'
  def isComplete(self):
    return self.isComplete

title_regex = u'^(\[)+(?P<title>[^|\[\]]*)(\])+$'
ruby_regex = u'^([「『《]*)(?P<noun>[^*(（」』》]+)([」』》]*)([（(](.*?))(?P<ruby>[^）):：;；,，、「『《]+)[,，、）『「《)]'
section_regex = u'^==(.*)==$'
ruby_prog = re.compile(ruby_regex, re.U)
title_prog = re.compile(title_regex, re.U)
section_prog = re.compile(section_regex, re.U)

f = codecs.open('text.txt','r','UTF-8')
f = codecs.open('jawiki-latest-pages-articles.xml-001.txt','r','UTF-8')
title_is_found = False
ruby_is_found = False
while True:
  line = f.readline()
  if not line:
    break
  # タイトルが見つかっていなければ
  if title_is_found is False:
    ruby_is_found = False
    title_match = title_prog.match(line)
    kana_regex = u'^[ 　ァ-ヾｦ-ﾟぁ-ゟ]+$' #日本語だよ
    kana_prog = re.compile(kana_regex, re.U)
    if title_match:
      title_is_found = True
      kana_match = kana_prog.match(title_match.group('title'))
      #print 'title'+title_match.group('title')
      if kana_match:
        print kana_match.group(0)+'\t'+kana_match.group(0)
        title_is_found = False
  # タイトルを発見している
  elif title_is_found is True:
    if title_prog.match(line):
      title_is_found = False
      ruby_is_found = False
    elif ruby_is_found is False:
      # 続いてルビを探す
      ruby_match = ruby_prog.match(line)
      # セクションを探す
      section_match = section_prog.match(line)
      redirect_match = re.match('^((#REDIRECT)|(#転送))',line)
      category_match = re.match('^(CATEGORIES:)',line)
      if redirect_match:
        title_is_found = False
        ruby_is_found = False
        pass
      elif category_match:
        pass
      else:
        if section_match:
          # セクションが見つかったらリセットする
          title_is_found = False
          ruby_is_found = False
        if ruby_match:
          title_is_found = False
          ruby_is_found = True
          #print 'noun: '+ruby_match.group('noun');
          #print 'ruby: '+ruby_match.group('ruby');
          print ruby_match.group('noun')+'\t'+ruby_match.group('ruby')

# セクションが見つかったらタイトルを見つけるまでスキップ

# FuriganaExtractor: 固有名詞とふりがなのペアを作る
# nextPair: 次の固有名詞とふりがなのペアを返す
# isEOF: ファイル終端かどうか確認する
# 元の文字を保存する
# ふりがなを保存する
## 挙動
# page titleを見つける
# カテゴリを見つける
# 本文を見つける
