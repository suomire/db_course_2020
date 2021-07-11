import psycopg2

idx1 = "create index albums_release_date_idx on albums (release_date);"

idx2 = "create index singers_countries_id_idx on singers (countries_id);"

idx3 = "create index label_singers_idx " \
       "on label_singer (record_label_id, singer_id, date_to)" \
       " where date_to is null;"

idx4 = "create index genres_name_idx on genres (name);"

idx5 = "create index albums_name_idx on albums (name);"

create_idxs = [idx1, idx2, idx3, idx4, idx5]

# dropping indexes
drop_idx1 = "drop index if exists singers_countries_id_idx"
drop_idx2 = "drop index if exists albums_release_date_idx"
drop_idx3 = "drop index if exists label_singers_idx"
drop_idx4 = "drop index if exists genres_name_idx"
drop_idx5 = "drop index if exists albums_name_idx"

drop_idxs = [drop_idx1, drop_idx2, drop_idx3, drop_idx4,
             drop_idx5]


def get_conn_params():
    f = open('data/db_info.txt', 'r')
    conn_params = dict()
    for r in f:
        pair_dict = r.split('\n')[0]
        conn_params[pair_dict.split(':')[0]] = pair_dict.split(':')[1]
    return conn_params


def connect():
    conn_params = get_conn_params()

    schema = conn_params['schema']

    conn = psycopg2.connect(
        host=conn_params['host'],
        database=conn_params['database'],
        user=conn_params['user'],
        password=conn_params['password'],
        options=f'-c search_path={schema}'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


def dropping_idxs():
    conn, cursor = connect()
    for di_q in drop_idxs:
        cursor.execute(di_q)
    close_connection(conn, cursor)
