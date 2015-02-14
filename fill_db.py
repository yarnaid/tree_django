import psycopg2

from tree_django import settings

db_name = settings.DB_NAME
table_name = settings.TABLE_NAME
depth = settings.DB_DEPTH
entries_num = settings.ENTREIES_NUM

conn = psycopg2.connect("user={} host={} port={}".format(
    settings.DB_USER,
    settings.DB_HOST,
    settings.DB_PORT))
conn.set_isolation_level(0)

cur = conn.cursor()
try:
    cur.execute('''CREATE DATABASE {}'''.format(db_name))
except Exception as e:
    print e

try:
    cur.execute('''DROP TABLE "{}"'''.format(table_name))
    cur.execute('''
                CREATE TABLE "{}" (
                "id" serial primary key,
                "name" text not null,
                "tree" integer[] not null
                );
                '''.format(table_name))
    cur.execute('''
                CREATE INDEX idx1
                ON {}
                (tree)
        '''.format(table_name))
    cur.execute('''
                CREATE INDEX idx2
                ON {}
                (name)
        '''.format(table_name))
except Exception as e:
    print('Cannot create table!')
    raise e

last_id = 0
delim = ', '


def create_entries(max_depth, entries_num, d_suffix='-1'):
    global last_id
    res = list()
    cur_depth = d_suffix.count(delim)
    leaf = cur_depth + 1 < max_depth
    for e in xrange(entries_num):
        path = d_suffix
        rec = (last_id, e, '{' + path + '}')
        res.append(rec)
        last_id += 1
        if leaf:
            res.extend(create_entries(max_depth, entries_num, delim.join([path, str(last_id - 1)])))
    return res

records = create_entries(depth, entries_num)
print len(records)
cur.executemany('''INSERT INTO {} (id, name, tree) VALUES (%s, %s, %s)'''.format(
    table_name), records)

cur.close()
conn.close()

print 'DB entries created!'
