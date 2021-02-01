import pymysql
import random

conn = pymysql.connect(host='localhost', user='root', password='a!4862753', db='mydb')
curs = conn.cursor()

def get_number():
    sql = 'select * from fund_group'
    curs.execute(sql)

    rows = list(curs.fetchall())
    rows = [list(_) for _ in rows]

    rows.sort(key=lambda x:x[1], reverse=True)
    tot = sum([_[1] for _ in rows])

    weight = [_[1]/tot for _ in rows]
    num = [int(_[0]) for _ in rows]

    group = random.choices(num, weights=weight, k=1)
    print(group)
    chocie_num = []
    i = 1
    while True:
        if len(chocie_num) == 6:
            break

        sql = 'select * from fund where grade = %s'
        curs.execute(sql, i)

        rows = list(curs.fetchall())
        rows = [list(_) for _ in rows]
        rows.sort(key=lambda x: x[2], reverse=True)
        tot = sum([_[2] for _ in rows])

        weight = [_[2] / tot for _ in rows]
        num = [int(_[1]) for _ in rows]
        random_num = random.choices(num, weights=weight, k=1)

        chocie_num.append(random_num)
        i += 1

    print(chocie_num)

get_number()

def fund_update_number(num_list):
    sql = 'update fund set count = count + 1 where grade = %s and num = %s' # grade는 숫자의 위치를 나타냄
    for i in range(len(num_list)):
        curs.execute(sql, (i+1, num_list[i]))
    conn.commit();

def fund_update_group(group):
    sql = 'update fund_group set count = count + 1 where num = %s'
    curs.execute(sql, group)
    conn.commit();