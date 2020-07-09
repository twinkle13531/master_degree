"""Python のリスト内包表記: 中級テスト"""
"""
Python には all という、真偽値のリスト（または後の章で解説するジェネレータ）を１つ受け取る関数がある。
受け取った要素が全て True の時のみ all は True を返す。 
すなわち all([True, False]) == False で all([True, True, True]) == True である。 
要素数が０のときには便宜的に成り立つとし、 all([]) == True である。
この all 関数を用いて、リスト x の中身が全て偶数であるかどうかを調べたい。
以下のプログラムの「ここを埋める」に 当てはまる式を答えよ。

if all(ここを埋める):

"""
if all([i for i in x if i%2==0]):
all(i % 2 == 0 for i in x):
all([i % 2 == 0 for i in x]):

"""
リスト内包表記にはフィルター操作もある。 for _ in _ のあとに if なになに を付け加えると、「なになに」が True のときのみ 値をリストに加える。 
詳しい説明は Data Structure の 5.1.4 List Comprehensions を見て欲しい。
今、リスト x に整数がたくさん入っているときにリスト内包表記を用いて偶数だけを取り出し、y に格納するにはどう書けば良いか？

y = ここに書く式を答えよ
"""
y=[i for i in x if i%2==0]

"""
Python には any という、真偽値のリスト（またはジェネレータ）を１つ受け取る関数がある。 
受け取った要素のうち一つでも True があれば any は True を返す。 
すなわち any([True, False]) == True で any([True, True, True]) == True、any([False, False]) == False である。 
要素数が０のときには False であると定義する。よって any([]) == False である。
この any 関数を用いて、リスト x の中身に偶数が一つ以上あるかどうかを調べたい。
以下のプログラムの「ここを埋める」に 当てはまる式を答えよ。 
i が偶数かどうかの判定は、２で割った余りが０かどうかを判定する式 i % 2 == 0 で行うのが一般的な手法の一つである。
"""
if any(for i in x if i%2==0):
if any(i % 2 == 0 for i in x):


s=[("Fizz" if x % 3 == 0 else str(x)) for x in range(1, 11)]
print(s)
"""
['1', '2', 'Fizz', '4', '5', 'Fizz', '7', '8', 'Fizz', '10']
"""

#新しいデータに対しては従来の手法を行うことでしかできない。
#従来のデータに対しては新しい手法を行うことができる。byつだせんせい


x = [[j for j in range(1, i + 1) if i % j == 0]   for i in range(1, 100)]
outer_list=[]
for i in range(1, 100):
	inner_list=[]
	for j in range(1, i+1):
		if i%j==0:
			inner_list.append(j)
	outer_list.append(inner_list)
outer_list
#リスト内包表記はネストすることもできる。 
#上記のプログラムを実行して得られる x についてx[i] は i の○○ を表す。
#○○に当てはまる言葉を漢字二文字で答えよ。


