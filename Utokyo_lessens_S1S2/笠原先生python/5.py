"""Python で遺伝子塩基配列の長さと GC 含有量を計算する: 初級テスト"""
"""標準入力の１行目に塩基のモチーフ（１０文字以内）をとり、 ２行目以降は Multi-FASTA 形式の塩基配列となっている。
入力に含まれる各塩基配列に含まれているモチーフの出現回数を表示せよ。"""
#coding:UTF-8
#ok!
import sys
seq_row_num=[]
lines=sys.stdin.readlines()
print(lines)
for i, each_line in enumerate(lines):
    if '>' in each_line:
        seq_row_num.append(i)
print(seq_row_num)