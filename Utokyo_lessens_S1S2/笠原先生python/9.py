#coding:UTF-8

def greeting(name):
	print "Hello, " + name + "!"

"""class Hogehoge を作れ。 
- コンストラクタは一つの引数（整数）を受け取り、それをインスタンス内に覚えておく。
覚えておいた値を今後 x と呼ぶこととする。 
- Hogehoge にはクラスメソッド plus(self, value) を持ち、
value に覚えておいた値 x を加算して返す。"""
class Hogehoge:
	def __init__(self, x):
		self.x = x

	def plus(self, value):
		self.value = self.value + 123


