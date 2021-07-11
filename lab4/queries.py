from db_utils import connect

countries_singers = None
albums_release_dates = None
record_label_ids = None
albums_names = None

conn, cursor = connect()


def get_countries_from_singers():
    temp_sql = "select c.name " \
               "from singers join countries c on singers.countries_id = c.id"
    cursor.execute(temp_sql)
    countries_singers = set(cursor.fetchall())
    return countries_singers


def get_release_dates():
    temp_sql = "select albums.release_date from albums "
    cursor.execute(temp_sql)
    albums_release_dates = set(cursor.fetchall())
    return albums_release_dates


def get_rl_ids():
    temp_sql = "select id from record_labels "
    cursor.execute(temp_sql)
    rl_ids = cursor.fetchall()
    return rl_ids


def get_albums_names():
    temp_sql = "select name from albums "
    cursor.execute(temp_sql)
    albums_names = set(cursor.fetchall())
    return albums_names


# №1 альбомы за определенный период
sql1 = "select  t.name, albums.name, albums.release_date " \
       "from albums join track_list tl on albums.id = tl.album_id join tracks t on t.id = tl.tracks_id " \
       "where release_date > %(min_date)s and release_date < %(max_date)s;"

# №2 исполнители заданной страны
sql2 = "select singers.name as singer_name " \
       "from singers join countries c on singers.countries_id = c.id" \
       " where c.name = %s;"

# №3 все сотрудничества артист-лейбл по настоящее время
sql3 = "select rl.name, s.name, date_from " \
       "from label_singer join record_labels rl on label_singer.record_label_id = rl.id " \
       "join singers s on label_singer.singer_id = s.id " \
       "where date_to is null and label_singer.record_label_id = %s;"

# №4 список исполнителей по жанрам
sql4 = "with t1 as " \
       "(select s.id as sid, t.genres_id as gid, count(*) as nums " \
       "from tracks_singers join singers s on tracks_singers.singers_id = s.id " \
       "join tracks t on tracks_singers.tracks_id = t.id group by sid, gid), " \
       "t2 as (select t1.sid, max(t1.nums) as maxnums from t1 group by t1.sid), " \
       "t3 as (select t1.sid, t1.gid as gid from t1 join t2 on t1.sid = t2.sid " \
       "where t1.nums = t2.maxnums) " \
       "select g.name, s2.name from t3 join genres g on t3.gid = g.id " \
       "join singers s2 on t3.sid = s2.id order by g.name, s2.name;"

# №5 список треков, входящих в альбом
sql5 = "select a.name, t.name from track_list join albums a on track_list.album_id = a.id " \
       "join tracks t on track_list.tracks_id = t.id " \
       "where a.name = %s;"

l_of_queries = [sql1, sql2, sql3, sql4, sql5]

idx1 = "create index albums_release_date_idx on albums (release_date);"

idx2 = "create index singers_countries_id_idx on singers (countries_id);"

idx3 = "create index label_singers_idx " \
       "on label_singer (record_label_id, singer_id, date_to)" \
       " where date_to is null;"

idx4 = "create index genres_name_idx on genres (name);"

idx5 = "create index albums_name_idx on albums (name);"

create_idxs = [idx1, idx2, idx3, idx4, idx5]

prep_sql1 = "prepare query_1 as " + sql1.replace("%(min_date)s", "$1").replace("%(max_date)s", "$2")
prep_sql2 = "prepare query_2 as " + sql2.replace("%s", "$1")
prep_sql3 = "prepare query_3 as " + sql3.replace("%s", "$1")
prep_sql4 = "prepare query_4 as " + sql4
prep_sql5 = "prepare query_5 as " + sql5.replace("%s", "$1")

prep_sqls = [prep_sql1, prep_sql2, prep_sql3, prep_sql4, prep_sql5]

dealloc_sqls = ["deallocate query_1;", "deallocate query_2;", "deallocate query_3;", "deallocate query_4;",
                "deallocate query_5;"]


def get_global_list():
    global countries_singers, albums_release_dates, record_label_ids, albums_names
    countries_singers = list(get_countries_from_singers())
    albums_release_dates = list(get_release_dates())
    record_label_ids = list(get_rl_ids())
    albums_names = list(get_albums_names())
