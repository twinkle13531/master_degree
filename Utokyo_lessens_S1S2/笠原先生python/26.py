"""Python でファイルを開く（読み込みと書き込みを同時）"""
# coding: UTF-8
"""
標準入力の１行目で示されたファイル名のファイルに対して、 
標準入力の２行目で示されたキーワードをサーチし、 
ヒットする行を標準入力の３行目で示されたファイル名のファイルに書き出せ。
行数と、何番目に現れたか、を各行の先頭に付加する。 
id を検索した場合には "voids" のように中間に含む単語も検索する。 
大文字小文字の同一視は行わなくて良い。"""

import sys
if len(sys.argv) <=4:
	print("入力内容が不十分です")
	sys.exit(1)

in_file_name = sys.argc[1]
key = sys.argc[2]
out_file_name = sys.argc[3]

with open(in_file_name, "rt") as f:
    lines = f.readlines() #すべての行をリスト化

#組み込み関数enumerate()...条件を満たす行の行番号を抽出
l_key = [(i, len(i), line) for i, line in enumerate(lines) if key in line]
l_i, l_leni, l_cont = list(zip(*l_key))

print("Line ", l_i, " hit #", l_leni, ": " l_cont)
