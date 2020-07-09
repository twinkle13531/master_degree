"""Python でユーザー入力を標準入力やコマンドラインから受け取る: 中級テスト"""

"""２名の友達関係をユーザーがたくさん入力する。 
このとき、友達の人数が最も多かった人の名前とその人数を空白１つで区切って１行に出力せよ。
ただし、入力の終端にはENDENDが続いているものとし、END という名前の人間は居ない。 
友達の人数が最も多かった人が複数居る場合には誰を出力してもよい。 
友達関係は必ず１つ以上入力される。
人名には空白文字が含まれる場合もある（例：John Doe）ので注意せよ。
大文字小文字は区別するので John さんと JOHN さんは異なる人として扱う必要がある。
dict を使って "名前→友達の人数" の関係を記憶しておこう。
"""
#codind:UTF-8
#ok!
import sys
friends_dic={}
people_ends_list=sys.stdin.readlines()
for people_end_list in people_ends_list:
    people_end=people_end_list.strip()
    if people_end in friends_dic.keys():
        friends_dic[people_end] +=1
    elif people_end=="END":
        continue
    else:
        friends_dic[people_end]=1
friends_ranking_list=[(k, v) for k, v in sorted(friends_dic.items(), key=lambda x: -x[1])]
print(friends_ranking_list[0][0],friends_ranking_list[0][1])      


"""
class Person:
	def __init__(self, family_name, given_name, age):
		self.family_name=family_name
		self.given_name=given_name
		self.age=age
	def __lt__(self, other):
	    return self.family_name < other.family_name
	    return self.age < other.age
	    return self.given_name < other.given_name
	def sort(self):
		for i, l_lists in enumerate(l):
			print(l_lists)
			l_lists=l_lists.split( )
			print(l_lists)
			if l_lists[0]>self.family_name:
				l.insert(i, self.family_name, self.given_name, self.age)
			elif l_lists[0]<self.family_name:
				l.insert(i+1, self.family_name, self.given_name, self.age)
			else:
				if l_lists[2]>self.age:
					l.insert(i, self.family_name, self.given_name, self.age)
				elif l_lists[2]<self.age:
					l.insert(i+1, self.family_name, self.given_name, self.age)
				else:
					if l_lists[1]>self.given_name:
						l.insert(i, self.family_name, self.given_name, self.age)
					else:
						l.insert(i, self.family_name, self.given_name, self.age)
			' '.join(l_lists)
l = []
l.append(Person("Sato", "Taro", 18))
l.append(Person("Sato", "Hanako", 17))
l.append(Person("Sato", "Aiko", 20))
l.append(Person("Tanaka", "Hirofumi", 30))
l.append(Person("Tanaka", "Masako", 28))
l.append(Person("Aizawa", "Hanako", 9))
l.sort()
for i in l:
    print("%s %s (%d)" % (i.family_name, i.given_name, i.age))
    """