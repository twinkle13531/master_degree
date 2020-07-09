
import csv

def open_file(filename):
	# tsvFile = file("data.tsv")
	
	tsv = csv.reader(filename, delimiter = '\t')
	#for s in tsv:
	#    print(s) 
	return tsv

def scan_gene_lengths(read_lines_list):
	Chromosome_dic = {}
	for line_list in read_lines_list:
		line2 = line_list

		# skip the following block if the record attribute is not "gene"
		if line2[2] != 'gene':
			continue

		# skip if unmapped
		gene_name = line2[0]
		if gene_name.startswith('211') or gene_name.startswith('Unmapped'):
			continue

		# here we have the length; first check if we have already scanned the gene before
		if gene_name not in Chromosome_dic:
			Chromosome_dic[gene_name] = [0, 0]

		# update length and count
		gene_length = int(line2[4]) - int(line2[3]) + 1
		Chromosome_dic[gene_name][1] += gene_length
		Chromosome_dic[gene_name][0] += 1

	Chromosome_key_list = sorted(Chromosome_dic.keys())
	return Chromosome_key_list, Chromosome_dic #list

import sys
read_lines_list = open_file(sys.stdin)
Chromosome_key_list, t= scan_gene_lengths(read_lines_list)

print('Chromosome,Gene Count,Avg Size')
for i in Chromosome_key_list:
	print(i+'\t'+str(t[i][0])+'\t'+str(int(t[i][1]/t[i][0])))