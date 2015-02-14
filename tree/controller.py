import psycopg2
import tree_django.settings as settings
# from django.template import Node
import sys
import models

cursor = None
conn = None


def get_connection():
    global conn
    if conn is None:
        try:
            conn = psycopg2.connect('user={} host={} port={}'.format(
                settings.DB_USER,
                settings.DB_HOST,
                settings.DB_PORT
            ))
            conn.set_isolation_level(0)
        except Exception as e:
            print e
            raise e
    return conn


def get_cursor():
    global cursor
    if cursor is None:
        try:
            conn = get_connection()
            cursor = conn.cursor()
        except Exception as e:
            print e
            raise e
    return cursor


def get_max_level():
    cursor = get_cursor()
    cursor.execute('''
        SELECT array_length(tree, 1) FROM {}
        '''.format(settings.TABLE_NAME))
    lengths = map(lambda x: x[0], cursor.fetchall())
    return max(lengths)


def select_level(to_level, q=None, cols='*'):
    if to_level < 1:
        where = '''array_length(tree, 1) > 0'''
    else:
        where = '''array_length(tree, 1) <= {}'''.format(int(to_level))
    if q is not None:
        where_id = where + ''' and name = '{}' '''.format(q)
        records = select(cols, where=where_id)
        ids = set()
        for rec in records:
            ids.update(set(rec[2][1:]))
            ids.add(rec[0])
        if len(ids) < 1:
            ids.add(-1)
        where += ''' and id in ({}) '''.format(','.join(map(str, ids)))
        res = select(cols, where=where)
    else:
        res = select(cols, where=where)
    return res


def select(cols, where=None):
    cursor = get_cursor()
    qstring = '''SELECT {} FROM {} '''.format(cols, settings.TABLE_NAME)
    if where is not None:
        qstring = qstring + ''' WHERE {}'''.format(where)
    try:
        cursor.execute(qstring + ''' ORDER BY id ''')
    except Exception as e:
        print e
        raise e
    return cursor.fetchall()


def remove_subtree(element_id):
    print >>sys.stderr, 'Preparing to remove element {}'.format(element_id)
    if element_id is None:
        return 0
    if isinstance(element_id, str):
        try:
            element_id = int(element_id)
        except Exception as e:
            print >>sys.stderr, e
            return 0
    record = select('tree', where=''' id = {} '''.format(element_id))
    if len(record) == 1:
        record = record[0]
    else:
        return 01
    tree = ','.join(map(str, record[0]) + [str(element_id)])
    cursor = get_cursor()
    cursor.execute('''
        DELETE FROM {}
        WHERE tree @> '{{ {} }}'
        '''.format(settings.TABLE_NAME, tree))
    number = cursor.rowcount
    cursor.execute('''
        DELETE FROM {}
        WHERE id = {}
        '''.format(settings.TABLE_NAME, element_id))
    number += cursor.rowcount
    return number


def update_name_by_id(id, new_name):
    if id is None or new_name is None:
        return None
    if not isinstance(id, int):
        id = int(id)
    cursor = get_cursor()
    cursor.execute('''
        UPDATE {} SET name = '{}'
        WHERE id = {}
        '''.format(settings.TABLE_NAME, str(new_name), id))
    res = cursor.rowcount
    print 'asdfasdfasdf', res
    res = new_name if res > 0 else None
    print res
    return res


def select_all():
    return select('*')