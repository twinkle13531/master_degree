#coding:UTF8
def hanoi(num, start, end, work):
    if n ==1:
        print("{}→{}".format(start, end))
    else:
        hanoi(n-1, start, work, end)
        hanoi(1, start, end, work)
        hanoi(n-1, end, start, work)
hanoi(4, 'A', 'B', 'C')

def hanoi(tower_list, pile_list, disk_number):
    cnt = 0
    passed_list = [tower_list[:]]
    while True:
        for disk in range(1, disk_number+1):
            if tower_list.index(tower_list[disk-1]) != disk-1:
                idx = pile_list.index(tower_list[disk-1])
            if (disk_number % 2 == 0 and disk % 2 == 1) or (disk_number % 2 == 1 and disk % 2 == 0) :
                if idx+1 >= len(pile_list):
                    idx = -1
                if pile_list[idx+1] not in tower_list or tower_list.index(pile_list[idx+1]) > disk-1:
                    tower_list[disk-1] = pile_list[idx+1]
                    passed_list.append(tower_list[:])
                    cnt += 1
            else:
                if 0 >= idx:
                    idx = len(pile_list)
                if pile_list[idx-1] not in tower_list or tower_list.index(pile_list[idx-1]) > disk-1:
                    tower_list[disk-1] = pile_list[idx-1]
                    passed_list.append(tower_list[:])
                    cnt += 1

            if tower_list == ['r'] * disk_number:
                return cnt, passed_list