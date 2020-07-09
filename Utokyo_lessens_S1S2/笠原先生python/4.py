"""Python でファイルを開く（読み取り）: 中級テスト"""
"""標準入力の１行目にファイル名を与えると、そのファイルを開いて行数情報を以下の様に付けて表示するプログラムをつくれ。 
ファイルがオープンできない場合には標準出力に "ERROR" （引用符は出力しない）と表示せよ。 
数字と : の間にはスペースを入れてはならない。
: とテキスト本体の間には半角スペースが１文字挿入されている。 これ以外の変更を行ってはならない。"""

#coding:UTF-8
#ok!
file_name=input()
try:
    with open(file_name) as f:
        file_list=f.readlines() #開いたファイル全体を行ごとに分割したリストとして取得
    for i, each_list in enumerate(file_list, 1): #番号を1スタートに
    	each_list=each_list.replace("\n", "")
    	print('{}: {}'.format(i, each_list))
except:
    print("ERROR")



"""
#ok!
import os.path

file= input()
if os.path.exists(file)==False: #ファイルパスが存在するかの確認 #pathがあってもファイルが開ける権限がないと開けないので不完全な条件である
	print("ERROR")
else:
	with open(file) as f:
		l = f.readlines()
	for i, l in enumerate(l, 1): #enumerate関数は0から始まる関数。1から始めるには指定する必要がある。
		l=l.replace("\n", "")
		print(str(i)+": "+l)
"""
"""os.path.exists()"""
#パスが存在しているかどうかを確認
#ファイルでもディレクトリでも、存在していればTrue、存在していなければFalseを返す。

#readlines()...開いたファイル全体を行ごとに分割したリストとして取得
#readline()...ファイルの先頭から一行ずつ文字列として取得

