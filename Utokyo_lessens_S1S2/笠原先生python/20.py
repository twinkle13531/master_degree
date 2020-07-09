"""Python のクラス（イントロ）: 初級テスト"""

class Mathconst:
    PI = 3.14159
    e = 2.71828

class Hogehoge:
    def __init__(self, x):
        self.x=x
    def plus(self, value):
        sum=value+self.x
        return "{0}".format(sum)

"""a = Hogehoge(123) #class名で引数１つ受け取った＝initコンストラクタのxですね
print(a.plus(654)) #plusメソッドでは引数１つ受け取った=valueに当たる
print(a.plus(0))
print(a.plus(1))

777
123
124

コンストラクタは一つの引数（整数）を受け取り、それをインスタンス内に覚えておく。
覚えておいた値を今後 x と呼ぶこととする。 
Hogehoge にはクラスメソッド plus(self, value) を持ち、
value に覚えておいた値 x を加算して返す。

class Spam:
    def __init__(self,ham,egg):
        self.ham = ham
        self.egg = egg
    def output(self):
        sum = self.ham + self.egg
        print("{0}".format(sum))

spam = Spam(5,10) #class名で引数２つ受け取った=ham, egg
spam.output() #outputメソッド関数では受け取らなかった=selfしか書いてないので
#15

"""