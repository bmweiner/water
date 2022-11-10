import os
import sqlite3

# config
DB_PATH = os.path.expanduser("~/util.db")

SQL = """
    select
        strftime('{format}', pulse, 'localtime') as {label},
        count(*) * 10 as gallons
    from water
    group by {label}
    ;
"""

def query(sql):
    # init sqlite db
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        data = cur.execute(sql).fetchall()

    return data

def print_query(sql):
    data = query(sql)
    for row in data:
        print(row)
    print()

print_query(SQL.format(format='%Y-%m-%d %H', label='hour'))

print_query(SQL.format(format='%Y-%m-%d', label='day'))

print_query(SQL.format(format='%Y-%m', label='month'))
