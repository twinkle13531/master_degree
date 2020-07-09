"""Python でファイルを開く（読み込みと書き込みを同時）: 初級テスト"""
"""
標準入力の１行目で示されたファイル名のファイルに対して、 
標準入力の２行目で示されたキーワードをサーチし、 
ヒットする行を標準入力の３行目で示されたファイル名のファイルに書き出せ。
ただし、行数と、何番目に現れたか、を各行の先頭に付加する。 
id を検索した場合には "voids" のように中間に含む単語も検索する。 
大文字小文字の同一視は行わなくて良い。"""

"""
line 7, hit #1: Cras aliquet sodales erat id posuere.
line 8, hit #2: Pellentesque finibus mi id ex euismod rhoncus.
line 10, hit #3: Etiam laoreet, leo in bibendum luctus, turpis massa eleifend lacus, id eleifend massa erat nec sem.
line 14, hit #4: Pellentesque aliquet id urna et congue."""


in_file, id, out_file=[input() for i in range(3)]
count=0
outcome=[]
with open(in_file) as in_f:
    in_f_list=in_f.readlines()
for i, in_f_list_each in enumerate(in_f_list, 1):
    in_f_list_each=in_f_list_each.replace("\n", "") #文字列ではreplaceが使える
    if id in in_f_list_each:
        count+=1
        outcome.append('line {}, hit #{}: {}'.format(i, count, in_f_list_each))
with open(out_file, mode='w') as out_f: 
     out_f.write("\n".join(outcome)+"\n")
"""
f1, id, f2=[input() for i in range(3)]
count=0
with open(f1) as f1o:
	l=f1o.readlines() #開いたファイル全体を行ごとに分割したリストとして取得する
	for i in range(len(l)):
		if id in l[i]: #lをidがあったら一行ずつ読んでいく
			count+=1 #idを見つけるたびにcountを1増やす
　　　　　　　mw=l[i].replace("\n", "")
            print("line {}, hit #{}: {}".format(i, count,m))
            """