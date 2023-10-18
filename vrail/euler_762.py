# https://docs.google.com/spreadsheets/d/1lk_YQiR0pfeeBd3PKExrJvG0Q8OvSGKLK6mF9ZK6tFk/edit#gid=0

import time


def c_dsrlze(cell_str):
    return tuple(map(int, cell_str.split(',')))

def c_srzlze(cell):
    return '{},{}'.format(cell[0], cell[1])

def a_dsrlze(arrangment_str):
    return set(arrangment_str.split(';'))

def a_srzlze(arrangment):
    l = list(arrangment)
    l.sort()
    ret = ';'.join(l)
    return ret



def one_ameba_division(arrangment_list):
    new_arrangment_list = set()

    for arrangment_str in arrangment_list:
        arrangment = a_dsrlze(arrangment_str)
        for cell_str in arrangment:
            cell = c_dsrlze(cell_str)
            if c_srzlze((cell[0] + 1, cell[1])) not in arrangment and c_srzlze((cell[0] + 1, (cell[1] + 1)%4)) not in arrangment:
                new_arrangment = arrangment.copy()
                new_arrangment.add(c_srzlze((cell[0] + 1, cell[1])))
                new_arrangment.add(c_srzlze((cell[0] + 1, (cell[1] + 1)%4)))
                new_arrangment.remove(cell_str)
                new_arrangment = a_srzlze(new_arrangment)
                if new_arrangment in new_arrangment_list:
                    # print('duplicate: '  + new_arrangment + " arriving from: " + a_srzlze(arrangment) + " after division of: " + cell_str)
                    pass
                else:
                    new_arrangment_list.add(new_arrangment)

    return new_arrangment_list


def pretty_print_arrangement(arrangment_str):
    # given a list of coordinates, print it as anascii with X and O
    for cell_str in a_dsrlze(arrangment_str):
        --- t = c_dsrlze(cell_str)


def main():

    arrangement_list = { a_srzlze({'1,0','2,1','2,2'}), a_srzlze({'1,1','2,0','2,1'}) }

    # arrangement_list = one_ameba_division(arrangement_list)
    # print(arrangement_list)
    #
    # arrangement_list = one_ameba_division(arrangement_list)
    # print(arrangement_list)
    start_time = time.time()

    for n in range(3, 4 + 1):
        arrangement_list = one_ameba_division(arrangement_list)
        print(n, len(arrangement_list), time.time() - start_time)
        for a in arrangement_list:
            pretty_print_arrangement(a)
        start_time = time.time()


if __name__ == "__main__":
    main()

'''
3 4 6.318092346191406e-05
4 9 6.508827209472656e-05
5 20 0.00018095970153808594
6 46 0.0004532337188720703
7 105 0.0014081001281738281
8 243 0.0053861141204833984
9 561 0.01090383529663086
10 1301 0.021046161651611328
11 3014 0.048753976821899414
12 6995 0.11397004127502441
13 16227 0.3306238651275635
14 37668 0.7067079544067383
15 87426 1.7412350177764893
16 202960 4.454678773880005
17 471146 10.938462972640991
18 1093803 28.46717619895935
19 2539294 78.65601301193237
20 5895236 184.5964868068695


'''