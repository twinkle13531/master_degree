"""CSV (Comma-Separated Value) ファイルとその扱い: 初級テスト"""
"""CSV ファイルの指定されたカラム２つを入れ替えるプログラムを作成せよ。
標準入力の１行目と２行目に入れ替えるカラムの番号（1-origin）、 ３行目以降に CSV ファイルの中身が渡される。 
出力は指定されたカラムを入れ替えた CSV ファイルとせよ。"""

"""pytohnの標準入力はinput()"""

#ok!
#coding:UTF-8
import sys
l_num1=int(input())
l_num2=int(input())
f_list=sys.stdin.readlines()
#print(f_list)
for each_info in f_list:
    each_info1=each_info.replace('\n', '').split(',')
    l_num1_content=each_info1[l_num1-1]
    l_num2_content=each_info1[l_num2-1]
    each_info1[l_num2-1]=l_num1_content
    each_info1[l_num1-1]=l_num2_content
    print(','.join(each_info1))


