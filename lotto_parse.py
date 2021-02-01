import pymysql
import random
import collections

conn = pymysql.connect(host='localhost', user='root', password='a!4862753', db='mydb')
curs = conn.cursor()

def get_number():
    sql = 'select * from lotto'
    curs.execute(sql)

    rows = list(curs.fetchall())
    rows = [list(_) for _ in rows]

    rows.sort(key=lambda x:x[1], reverse=True)
    tot = sum([_[1] for _ in rows])

    weight = [_[1]/tot for _ in rows]
    num = [int(_[0]) for _ in rows]

    chocie_num = []
    while True: # dup 제거
        dup = False
        if len(chocie_num) == 5: # 5000원 어치만
        # if len(chocie_num) == 1:  # 수작업 용도
                break
        num_list = random.choices(num, weights=weight,k=6) # 가중치 부여
        dup_check = dict(collections.Counter(num_list)) # dup count check
        for _ in dup_check.values():
            if _ != 1:
                dup = True
                break
        if dup == True:
            continue

        chocie_num.append(num_list) # dup 없을 때만 append

    conn.close()
    return chocie_num

def update_number(num_list):
    sql = 'update lotto set count = count + 1 where num = %s'
    for num in num_list:
        print(num)
        curs.execute(sql, num)
    conn.commit();