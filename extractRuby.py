# -*- coding: utf-8 -*-

import re
import codecs
import sys

# FuriganaExtractor: 固有名詞とふりがなのペアを作る
# nextPair: 次の固有名詞とふりがなのペアを返す
class FuriganaExtractor:
  """固有名詞とふりがなのペアを作る"""
  def __init__(self, _filename):
    self.filename = _filename
    self.title_found = False
    self.isComplete = False
    self.page_title = u''
   
    title_regex = u'^(\[){2}(?P<title>[^\[\]]+)(\]){2}$'
    ruby_regex = u'^([「『《]*)(?P<noun>[^、。*(（」』》]+)([」』》]*)([（(](.*?))(?P<ruby>[^、）):：;；,，、「『《]+)([,，、(（）『「《)。\-])'
    section_regex = u'^[=]+([^=]*)[=]+$'
    kana_regex = u'^[ 　ァ-ヾｦ-ﾟぁ-ゟ]+$' #日本語だよ
    redirect_regex = u'^((#REDIRECT)|(#転送))'
    category_regex = u'^(CATEGORIES:)'

    self.title_prog = re.compile(title_regex, re.U)
    self.ruby_prog = re.compile(ruby_regex,re.U)
    self.section_prog = re.compile(section_regex, re.U)
    self.kana_prog = re.compile(kana_regex, re.U)
    self.redirect_prog = re.compile(redirect_regex, re.U)
    self.category_prog = re.compile(category_regex, re.U)
    self.f = codecs.open(self.filename,'r','UTF-8')
  def nextPair(self):
    if self.isComplete is False:
      while True:
        line = self.f.readline()
        if not line:
          self.isComplete = True
          return

        title_match = self.title_prog.match(line)
        if title_match:
          self.title_found = True
          # かっこ削除
          kakko_regex = u'[ 　(（]+([^)）]*)[)）]+'
          kakko_match = re.search(kakko_regex, title_match.group('title'))
          #print '*** '+title_match.group('title')
          if kakko_match:
            self.page_title = re.sub(kakko_regex, '', title_match.group('title'), 2)
          else:
            self.page_title = title_match.group('title')
          kana_match = self.kana_prog.match(self.page_title)
          if kana_match:
            # タイトルが,かなだけなら
            self.title_found = False
            noun = kana_match.group(0)
            furigana = noun
            return (self.page_title, noun, furigana)
        else:
          if self.title_found:
            section_match = self.section_prog.match(line)
            redirect_match = self.redirect_prog.match(line)
            category_match = self.category_prog.match(line)
            ruby_match = self.ruby_prog.match(line)
            if section_match:
              self.title_found = False
            elif redirect_match:
              pass
            elif category_match:
              pass
            elif ruby_match:
              # ルビを見つけたら
              self.title_found = False
              noun = ruby_match.group('noun')
              furigana = ruby_match.group('ruby')
              noun = re.sub(u'\[[/]*(tpl)\]', '', noun, 2)
              furigana = re.sub(u'\[[/]*(tpl)\]', '', furigana, 2)
              furigana = re.sub(u'[0-9]+[年][0-9]+[月][0-9]+[日]', '', furigana)
              furigana = re.sub(u'[^ァ-ヾｦ-ﾟぁ-ゟ]*$', '', furigana, 2)
              ichiran = noun.rfind(u'一覧')
              mataha = furigana.find(u'または')
              # ゴミ除去
              if re.match('^[a-zA-Z|\- ]+$',furigana):
                pass
              elif re.match(u'^[0-9]+[月][0-9]+[日]$',noun):
                pass
              elif len(furigana) < 2 or len(noun) < 2:
                pass
              elif re.match(u'[^ァ-ヾｦ-ﾟぁ-ゟ－ 　]+',furigana):
                pass
              elif ichiran > -1:
                # 一覧を含む文字列
                pass
              elif mataha > -1:
                # または
                pass
              else:
                return (self.page_title, noun, furigana)
  def Complete(self):
    return self.isComplete

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  if argc == 2:
    ext = FuriganaExtractor(argvs[1])
    while ext.Complete() is False:
      pair = ext.nextPair()
      if pair:
        print pair[0]+'\t'+pair[2]
