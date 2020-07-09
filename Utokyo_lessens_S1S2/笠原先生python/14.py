"""正規表現の特殊文字とその他の細かい話：上級テスト"""
"""
import re
pat = re.compile(r"^(\d+)$")
print("START")
for r in pat.finditer("123\n45\n678"):
  print(r.group(1))
print("END")
"""

import re
pat = re.compile(r"^(\d+)$", re.MULTILINE) 
print("START")
for r in pat.finditer("123\n45\n678"):
  print(r.group(1))
print("END")