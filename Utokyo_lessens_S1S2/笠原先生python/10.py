"""Python で遺伝子塩基配列の長さと GC 含有量を計算する（video)"""

#coding: UTF-8
import sys
 if len(sys.argv) <= 1:
 	print >> sys.stderr, "Usage: acgt_count.py <input multi-FASTA>"
 	sys.exit(1)

input_file_name = sys.argv[1]

def show_gene_composition(name, d): #key=name, value=d
	print name, ":"
	for k, v in d.items(): #items()関数によってkeyとvalueを抽出 
		print "\t" +k+ ": " + str(v)

d = {} #空のdictionaryを用意する
current_gene_name = None

try:
 	with open(input_file_name, "r") as f:
 	for l in f.readlines(): #f.readlines()から１つずつ変数lに格納していく	
 		l = l.strip() #\nをなくす
 		if len(l) == 0:
 			continue #振り出しへ戻る
 		if l[0] == '>':
 			show_gene_composition(current_gene_name, d)
 			current_gene_name = l[1:]
 			d = {} #空に戻す
 			continue #振り出しへ戻る
 	    for c in l: #l.strip()のlから１つずつ取り出して変数cに格納していく
 	    	if c in d: #dにc(=l.strip()の要素)があるとき
 	    		d[c] += 1 #
 		    else:
 		    	d[c] = 1
 	show_gene_composition(current_gene_name, d)
except IOError, e:
	print "I/O error: ", e
	print "Check the input file('%s')" % input_file_name

#
import sys
 if len(sys.argv) <= 1:
 	print >> sys.stderr, "Usage: acgt_count.py <input multi-FASTA>"
 	sys.exit(1)

input_file_name = sys.argv[1]

def show_gene_composition(name, d):
	if name == None: return
	num_a = d['A'] if 'A' in d else 0
	num_c = d['C'] if 'C' in d else 0
	num_g = d['G'] if 'G' in d else 0
	num_t = d['T'] if 'T' in d else 0
	num_cg = num_c + num_g
	num_at = num_a + num_t
	num_all = num_cg + num_at
	print name, ": GC %3.1f%%\t%d" % int((num_cg * 100.0 / num_all), num_all)

print "Gene name\tGC content\tLength" #ヘッダ
d = {}
current_gene_name = None
try:
 	with open(input_file_name, "r") as f:
 	for l in f.readlines():
 		l = l.strip()
 		if len(l) == 0:
 			continue
 		if l[0] == '>':
 			show_gene_composition(current_gene_name, d)
 			current_gene_name = l[1:]
 			d = {}
 			continue
 	    for c in l:
 	    	if c in d:
 	    		d[c] += 1
 		    else:
 		    	d[c] = 1
 	show_gene_composition(current_gene_name, d)
except IOError, e:
	print "I/O error: ", e
	print "Check the input file('%s')" % input_file_name

#csvlookを用いると整形した状態で見れる
