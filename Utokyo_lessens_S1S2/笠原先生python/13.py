"""正規表現のマッチを Python で調べてみる: 初級テスト"""
#coding:UTF-8
header_line=[] #カウントはjで行う	
import sys
became_list=sys.stdin.readlines()
for r in became_list:
	if '>' in r:
		header_line.append(r)
#print(len(header_line))

for l in header_line:
	use_string=l.split('from')[0]
	m=use_string.rfind(",")
	latter=use_string[m+1:]
	former=use_string[:m]
	gene_name=former.split()[1]
	gene_location=latter.strip() # strip([chars])...文字列の先頭と末尾から指定した文字を除去する 
	if 'Chr' not in gene_location:
		plasmid=gene_location.split()[-1]
		print("{},{}".format(gene_name, plasmid))
	else:
		print("{},{}".format(gene_name, gene_location))
	"""
	print("{},{}".format(gene_name,
		gene_location if 'Chr' in gene_location else
		gene_location.split()[-1]))
	"""


"""splitlinesはデフォルトで改行文字があった場合は分割してリストとして返します。
文字列.splitlines()
re.split('[-+#]', s_marks)
"""


#try, except構文...何かエラーがあったら何がエラーかを示さずに終了する

"""
l, r=line.split(",")[:2] 配列の長さを２つに限定

for l in lines:


局所的に使う変数は簡単なものにする
"""