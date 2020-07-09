
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
   




