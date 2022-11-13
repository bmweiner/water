import os
import sqlite3
import calendar
import datetime

# config
DB_PATH = os.path.expanduser("~/util.db")

def query(sql):
    # init sqlite db
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        data = cur.execute(sql).fetchall()
    return data

def is_dst(dt):
    cal = calendar.Calendar()
    dst_start = cal.monthdatescalendar(dt.year, 3)[1][6]
    dst_end = cal.monthdatescalendar(dt.year, 11)[0][6]
    return dt >= dst_start and dt <= dst_end

def et_offset_now():
    dt = datetime.datetime.utcnow().date()
    return 5 - is_dst(dt)

def today():
    limit = datetime.datetime.utcnow() - datetime.timedelta(hours=et_offset_now())
    limit = limit.date()
    sql = """
        select
            strftime('%Y-%m-%d %H:%M', pulse, '-{offset} hours') as time
        from water
        where strftime('%Y-%m-%d', time) == '{limit}'
        order by rowid desc
        ;
    """
    sql = sql.format(offset=et_offset_now(), limit=limit)
    return query(sql)

def daily():
    # last 30 Day totals
    limit = datetime.datetime.utcnow().date() - datetime.timedelta(days=30)
    sql = """
        select
            strftime('{form}', pulse, '-{offset} hours') as time,
            count(*) * 10 as gallons
        from water
        where pulse >= '{limit}'
        group by time
        order by time desc
        ;
    """
    sql = sql.format(form='%Y-%m-%d', offset=et_offset_now(), limit=limit)
    return query(sql)
