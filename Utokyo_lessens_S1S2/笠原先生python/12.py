"""Python で遺伝子塩基配列の長さと GC 含有量を計算する：初級テスト"""
#coding:UTF-8
#append関数はリストを変更することができる
#m="" #try文の中だけでなくwhile文全体で効かせたいため、ここで定義
seq_count=0 #全要素数
lines_list=[] #読み取った内容をリスト形式で保存
label_lines_index=[] #>で始まる要素の番号を保存
read_lines_list=[] #>の後に続く塩基配列を保存
key_match_count=[] #>の後に続く塩基配列にkeywordがいくつ含まれているかリストで保存
ouput_label=[]
while True:
    try:
        tmp=input()
        if '>' in tmp:
            label_lines_index.append(seq_count)
        seq_count+=1
        lines_list.append(tmp)
    except EOFError: #入力が入らなくなったら
        break #whileから抜ける。
for i in range(len(label_lines_index)):
    if i==len(label_lines_index)-1:
    	if len(lines_list)-1-label_lines_index[i]==1: #ラストかつ一行だけ
    		base=lines_list[label_lines_index[i]+1]
    	else: #ラストで複数行
    		base="".join(lines_list[label_lines_index[i]+1:len(lines_list)])
    #elif label_lines_index[i+1]-label_lines_index[i]<=2: #一行
    #	base=lines_list[label_lines_index[i]+1]
    else: #複数行ｗ
    	base="".join(lines_list[label_lines_index[i]+1:label_lines_index[i+1]])
    read_lines_list.append(base)
    #print(base)
#for i in range(len(label_lines_index)):
    ee=lines_list[label_lines_index[i]].split()[0] #リストではなくて文字列になっている
    ouput_label.append(ee.strip(">")) #リストとして入った
def count_motif(key, target):
	moti=0
	key_list=list(key)
	target_list=list(target)
	#print(key)
	#print(target)
	for i in range(len(target_list)-len(key_list)+1):
		if key_list== target_list[i:i+len(key_list)]:
			moti+=1
	return moti
for i in range(len(read_lines_list)):
	key_match_count.append(count_motif(lines_list[0], read_lines_list[i]))
	print("{}: {}".format(ouput_label[i], key_match_count[i]))

"""
>>> test.split(",") # test というリストを 区切り文字” , ” で区切る
['orange', 'apple', 'banana', 'strawberry']
>>> test = "orange apple banana strawberry"
>>> test.split()　# 引数に何も指定しない場合、スペースやタブ等で自動的に区切る
['orange', 'apple', 'banana', 'strawberry']
"""