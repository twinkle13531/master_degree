""" """
#coding:UTF-8
import csv
name=[]
name_count=[]

file= input()
f=open(file, 'r')
tsv=csv.reader(f, delimiter='\t') #配列になっている
for row in tsv:
	row_list=row.spilt('\t')
	if row_list[0].startwith('211'):
		break
	elif row_list[0].startwith('Unmapped'):
		break
	elif row_list[0] not in name:
		name.append(row_list[0])
		name.sort()
		

"""
break文＝強制的に処理ブロックから抜け出す
continue文＝強制的に以降の処理を終了する
"""