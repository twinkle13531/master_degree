"""Python でファイルを開く（読み取り）: 初級テスト"""
"""test.txt というファイルを開き、行数を数えて出力するプログラムを作れ。"""
# coding: utf-8
with open('test.txt') as f:
      s = f.readlines()
print(len(s))
