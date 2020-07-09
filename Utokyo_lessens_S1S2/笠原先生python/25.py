# coding: UTF-8
"""Python でファイルを開く（読み込みと書き込みを同時）"""
import sys
if len(sys.argv) <=1:
	print >> sys.stderr, "Usage: linenumber.py <input file>"
	sys.exit(1)
file_name = sys.argc[1]
line_count =0
with open(file_name, "rt") as f:
	while True:
		for l in f.readlines():
			line_count +=1
			print(line_count,":", l.strip(), f.readlines())
	else:
		print('ERROR')

#readlines()...各行を要素とするリストを取得
#readlines()で取得できるリストは行末の改行文字\nを含んでいる。
##除去したい場合はリスト内包表記で各要素（各行）にstrip()メソッドを適用する


