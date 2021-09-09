import csv
from io import StringIO

FILE_BASE_ROMANTABLE = "./romantable_emoji.txt"
FILE_TAPGET_ROMANTABLE = "./romantable_IU_Swap_emoji.txt"

# 子音+k or x なら、kとxをスワップ


def make_array2d() -> list:
    with open(FILE_BASE_ROMANTABLE) as f:
        all_str = f.read()
    all_str = all_str.replace(' ', '\t')
    all_str = StringIO(all_str)
    reader = csv.reader(all_str, delimiter='\t')
    return [row for row in reader]


def get_unique_list(seq: list) -> list:
    '''２次元配列の重複を削除する。
    >>> get_unique_list([[1, 1], [0, 1], [0, 1], [0, 0], [1, 0], [1, 1], [1, 1]])
    [[1, 1], [0, 1], [0, 0], [1, 0]]
    '''

    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]


def main():
    lines = make_array2d()
    new_table = []
    tmp_table = []
    for index, line in enumerate(lines):
        if ((not line[0].startswith(':')) and (line[0].endswith('k') or line[0].endswith('x')) and line[1].endswith('ん') and index >= 1):
            tmp_table.append(line)
            # print(line)
        else:
            new_table.append(line)
    # print(len(new_table))

    tmp_table2 = []

    for index, tmp in enumerate(tmp_table):
        if (index >= 1):
            if (tmp_table[index][0][-2] == tmp_table[index-1][0][-2] and tmp_table[index][0][-1] == 'x' and tmp_table[index-1][0][-1] == 'k'):
                tmp_table2.append(tmp_table[index-1])
                tmp_table2.append(tmp_table[index])
            else:
                new_table.append(tmp)
        else:
            new_table.append(tmp)

    # pprint.pprint(tmp_table2)

    for i in range(len(tmp_table2)):
        if (i >= 1):
            if (tmp_table2[i][0][-1] == 'x' and tmp_table2[i-1][0][-1] == 'k'):
                tmp_table2[i][0], tmp_table2[i -
                                             1][0] = tmp_table2[i-1][0], tmp_table2[i][0]
                i += 1
    new_table.extend(tmp_table2)

    with open(FILE_TAPGET_ROMANTABLE, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(get_unique_list(new_table))


if __name__ == "__main__":
    main()
    # import doctest
    # doctest.testmod()
