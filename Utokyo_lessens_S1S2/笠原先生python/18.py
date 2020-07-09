"""CSV (Comma-Separated Value) ファイルとその扱い：中級テスト"""
"""標準入力から CSV ファイルが与えられる。
タブ区切りのTSVファイルに変換して出力せよ。 
値にカンマが含まれる場合は必ず "" で値が括られている。
値に '"' が含まれる例は入力に含まれない。 
また、値にタブ文字が元から入っていることもない。
値は全て ASCII で表すことのできる値である。"""

"""しらなかったこと
Name,ID
bob,123
alice,"456"
"S, carol",789
はリストだった"""

#coding:UTF-8
import sys
import csv

cin = csv.reader(sys.stdin)
for i in cin:
    print("\t".join(i))