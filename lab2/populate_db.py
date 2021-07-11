"""
1. Реализация в виде программы параметризуемого генератора, который позволит сформировать набор связанных данных в каждой таблице.
2. Частные требования к генератору, набору данных и результирующему набору данных:
    - количество записей в справочных таблицах должно соответствовать ограничениям предметной области
    - количество записей в таблицах, хранящих информацию об объектах или субъектах, должно
    быть параметром генерации; значения для внешних ключей необходимо брать из связанных таблиц

"""
import psycopg2
from mimesis import Generic
import timeit
from lib_insert import InsertFunctions

# GLOBALS
g = Generic()
cursor = None
parameter = 0

# tables (list of tuples)
table_countries = None
table_genres = None
table_albums = None
table_record_labels = None
table_singers = None
table_tracks = None

table_track_list = None
table_tracks_singers = None
table_label_singer = None


def get_countries():
    global table_countries
    cursor.execute("select name from countries")
    table_countries = list(cursor.fetchall())


def get_genres():
    global table_genres
    cursor.execute("select name from genres")
    table_genres = list(cursor.fetchall())


def get_albums():
    global table_albums
    cursor.execute("select name, release_date from albums")
    table_albums = list(cursor.fetchall())


def get_record_labels():
    global table_record_labels
    cursor.execute("select name from record_labels")
    table_record_labels = list(cursor.fetchall())


def get_singers():
    global table_singers
    cursor.execute("select name, countries_id from singers")
    table_singers = list(cursor.fetchall())


def get_tracks():
    global table_tracks
    cursor.execute("select name, duration from tracks")
    table_tracks = list(cursor.fetchall())


def get_track_list():
    global table_track_list
    cursor.execute("select * from track_list")
    table_track_list = list(cursor.fetchall())


def get_label_singer():
    global table_label_singer
    cursor.execute("select * from label_singer")
    table_label_singer = list(cursor.fetchall())


def get_tracks_singers():
    global table_tracks_singers
    cursor.execute("select * from tracks_singers")
    table_tracks_singers = list(cursor.fetchall())


if __name__ == '__main__':

    # get parameter
    print("Введите параметр генерации данных для задания количества записей в талицах")
    parameter = int(input())
    start = timeit.default_timer()
    # parameter = 50

    f = open('data/db_info.txt', 'r')

    conn_params = dict()

    for r in f:
        pair_dict = r.split('\n')[0]
        conn_params[pair_dict.split(':')[0]] = pair_dict.split(':')[1]

    # connect to the db

    schema = conn_params['schema']

    con = psycopg2.connect(
        host=conn_params['host'],
        database=conn_params['database'],
        user=conn_params['user'],
        password=conn_params['password'],
        options=f'-c search_path={schema}'
    )
    con.autocommit = True

    # cursor
    cursor = con.cursor()

    insert = InsertFunctions(parameter)

    # populate methods
    get_countries()
    table_countries = insert.insert_countries(cursor, table_countries)  # countries id

    get_genres()
    table_genres = insert.insert_genres(cursor, table_genres)

    get_record_labels()
    table_record_labels = insert.insert_record_labels(cursor, table_record_labels)

    get_singers()
    table_singers = insert.insert_singers(cursor, table_singers, table_countries)

    get_albums()
    table_albums = insert.insert_albums(cursor, table_albums)

    get_tracks()
    table_tracks = insert.insert_tracks(cursor, table_tracks, table_genres)

    get_track_list()
    insert.insert_track_list(cursor, table_tracks, table_albums, table_track_list)

    get_tracks_singers()
    insert.insert_tracks_singers(cursor, table_tracks, table_singers, table_tracks_singers)

    get_label_singer()
    insert.insert_label_singer(cursor, table_record_labels, table_singers, table_label_singer)

    # closing
    con.commit()
    cursor.close()
    con.close()

    end = timeit.default_timer() - start
    print(end)
