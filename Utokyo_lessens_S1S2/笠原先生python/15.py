"""正規表現を使った情報の抜き出しと文字列置換：初級テスト"""
#coding;UTF-8
"""
f=input() #file入力だと想定した
with open(f) as fo:
	l_list=fo.readlines() #開いたファイル全体を行ごとに分割したリストとして取得する
last_to_list=l_list[len(l_list)-1].split()
print(last_to_list[5])
#re.split('\d+', info
"""

info = [input() for i in range(8)]
last_list=info[len(info)-1].split()
print(last_list[5])
