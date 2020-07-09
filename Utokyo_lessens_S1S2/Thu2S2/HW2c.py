def RPN(states):
    operator = {
        '+': (lambda x, y: x + y),
        '-': (lambda x, y: x - y),
        '*': (lambda x, y: x * y),
        '/': (lambda x, y: float(x) / y)
    }
    stack = []
    print('RPN: %s' % states)
    for index, z  in enumerate(states):
        if index > 0:
            print(stack)
        if z not in operator.keys():
            stack.append(int(z))
            continue
        y = stack.pop()
        x = stack.pop()
        stack.append(operator[z](x, y))
        print('%s %s %s =' % (x, z, y))
    print(stack[0])
    return stack[0]

def test():
    print("OK" if RPN("37+621-*+") == 16 else "NG")

if __name__ == '__main__':
    import sys
    RPN(sys.argv[1])
    test()