"""正規表現の特殊文字とその他の細かい話: 上級テスト"""
#coding:UTF-8
import re
pat = re.compile(r"^(\d+)$", re.MULTILINE) 
print("START")
for r in pat.finditer("123\n45\n678"):
  print(r.group(1))
print("END")
"""
START
123
45
678
END
"""

import re
pat = re.compile(r"^(\d+)$")
print("START")
for r in pat.finditer("123\n45\n678"):
  print(r.group(1))
print("END")
"""
START
END
"""

"""re.MULTILINEを指定しない場合、^は文字列の先頭に、$は文字列の末尾しかマッチしない。
つまり1つの文字列変数につきそれぞれ1箇所しかマッチし得ない。
なので改行を含む文字列で各行の 先頭や末尾（改行）にマッチさせたい場合は
re.MULTILINEを指定する必要がある"""