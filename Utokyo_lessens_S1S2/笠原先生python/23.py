i = int(input())
j = int(input())

for m in range(i, j+1):
    if m%3==0:
        if m%5==0:
            print("Fizz Buzz")
        else:
            print("Fizz")
    elif m%5==0:
        print("Buzz")
    else:
        print(m)

