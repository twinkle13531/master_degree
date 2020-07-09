"""CSV (Comma-Separated Value) ファイルとその扱い: 初級テスト"""
"""kashiwa問題"""
#ok!
#coding:UTF-8
import sys
col_num=input()
key=input()
f_list=sys.stdin.readlines()

output=[]
output.append(f_list[0])
for i in range(1,len(f_list)):
	f_list_list=f_list[i].split(",")
	if key == f_list_list[int(col_num)-1]:
		output.append(f_list[i])
		f_list_list=[]
for j in output:
	print(j, end="")
#print(end="\n")
"""
>>> test.split(",") # test というリストを 区切り文字” , ” で区切る
['orange', 'apple', 'banana', 'strawberry']

# ファイルをリストに出力
file = open('c:\\pg\\file.csv', 'r')
f_list = file.readlines()
file.close()
# リストから1行ずつ読み込む
for f_line in f_list:
    print(f_line)
"""

"""ファイルを一行ずつ処理
f=
"""