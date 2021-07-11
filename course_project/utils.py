import psycopg2

tables = ['albums', 'countries', 'genres', 'label_singer', 'record_labels', 'singers', 'track_list', 'tracks',
          'tracks_singers', 'users']

editable_tables = {'albums': ['name', 'release_date', 'cover'],
                   'genres': ['name'],
                   'record_labels': ['name', 'bio'],
                   'singers': ['name', 'bio', 'countries_id', 'photo'],
                   'tracks': ['name', 'text', 'duration', 'genres_id']}

actions = ['select', 'update', 'delete', 'custom query']


class User:

    def __init__(self, username, admin=False):
        self.username = username
        self.admin = admin

    def __str__(self):
        return '{} (admin: {})'.format(self.username, self.admin)


def create_connection():
    f = open('data/db_info.txt', 'r')
    conn_params = dict()

    for r in f:
        pair_dict = r.split('\n')[0]
        conn_params[pair_dict.split(':')[0]] = pair_dict.split(':')[1]

    schema = conn_params['schema']

    con = psycopg2.connect(
        host=conn_params['host'],
        database=conn_params['database'],
        user=conn_params['user'],
        password=conn_params['password'],
        options=f'-c search_path={schema}'
    )
    con.autocommit = True

    cursor = con.cursor()
    return con, cursor


def registration(con, cursor, data):
    try:
        cursor.execute("insert into users (username, password, admin_privileges) values (%s, %s, %s)",
                       data)

    except psycopg2.IntegrityError as e:
        print('Error in db. Maybe user with entered username is already exists.', e.pgerror)
    con.commit()

    cursor.execute("select username from users where username = %s", (data[0],))

    respond = cursor.fetchall()
    if respond[0][0] == data[0]:
        return True
    else:
        raise EnvironmentError('Your account was not added. Try again later.')


def check_user(cursor, username, password):
    cursor.execute('select username, admin_privileges, password  from users where username = %s ', (username,))

    user = cursor.fetchall()

    if len(user) != 1:
        raise KeyError('You are not registered')
    if password != user[0][-1]:
        print('Wrong password, try again')
        raise ValueError('Your password was incorrect')
    else:
        user_obj = User(username, admin=user[0][1])
        print('Welcome, {}. '.format(user_obj))
        return user_obj


def adding_records_to_tables(cursor):
    print('Adding records')
    print('List of all tables: {}'.format(tables))
    print('List of editable tables: {}'.format(editable_tables.keys()))

    print('Table: ', end='')
    table = input()
    try:
        if table == list(editable_tables.keys())[0]:
            print('Album name: ', end='')
            album_name = input()

            print('Release date (YYYY-MM-DD): ', end='')
            release_date = input()

            cursor.execute("insert into albums (name, release_date) values (%s, %s)", (album_name, release_date))

        elif table == list(editable_tables.keys())[1]:
            print('Genre name: ', end='')
            genre_name = input()

            cursor.execute("insert into genres (name) values (%s)", (genre_name,))

        elif table == list(editable_tables.keys())[2]:
            print('Record label name: ', end='')
            record_label_name = input()

            print('Record label bio: ', end='')
            record_label_bio = input()

            cursor.execute("insert into record_labels (name, bio) values (%s, %s)",
                           (record_label_name, record_label_bio))

        elif table == list(editable_tables.keys())[3]:
            print('Singers name: ', end='')
            singer_name = input()

            print('Singer bio: ', end='')
            singer_bio = input()

            print('Singer country: ', end='')
            singer_country = input()

            cursor.execute("select id from countries where name = %s", (singer_country,))
            respond = cursor.fetchall()
            singer_country_id = respond[0][0]

            cursor.execute("insert into singers (name, bio, countries_id) values (%s, %s, %s)",
                           (singer_name, singer_bio, int(singer_country_id)))

        elif table == list(editable_tables.keys())[4]:
            print('Track name: ', end='')
            track_name = input()

            print('Track text: ', end='')
            track_text = input()

            print('Text duration: ', end='')
            track_duration = int(input())

            print('Text genre: ', end='')
            track_genre = input()

            cursor.execute("select id from genres where name = %s", (track_genre,))
            respond = cursor.fetchall()
            track_genre_id = respond[0][0]

            cursor.execute("insert into tracks (name, text, duration, genres_id) values (%s, %s, %s, %s)",
                           (track_name, track_text, track_duration, track_genre_id))
        else:
            raise ValueError('You entered wrong table')
    except psycopg2.DataError:
        raise ValueError('You entered wrong value!!!!!!')


def custom_query_mode(cursor):
    while True:
        try:
            print('Query (enter exit to return to the menu): ', end='')
            query = input()
            if query == 'exit':
                break
            cursor.execute(query)
            respond = cursor.fetchall()
            print(respond)
        except psycopg2.DataError:
            print('You entered wrong value! Try again ')
        except psycopg2.DatabaseError:
            print('There was database error. You have entered something wrong.')


def check_selected(selected, editable_fields):
    if selected == '*':
        return True
    selected = selected.split(',')
    selected_field_list = list(map(str.strip, selected))
    bool_fields = [x in editable_fields for x in selected_field_list]
    return len(selected_field_list) == sum(bool_fields)


def action_with_records(cursor):
    print('Actions with records (select, delete, update)')
    print('List of all tables: {}'.format(tables))
    print('List of editable tables: {}'.format(list(editable_tables.keys())))
    print('Available actions: {}'.format(actions))
    print('Note: delete and update actions are available if you want to affect on unconnected records')

    print('Action: ', end='')
    action = input()
    if action not in actions:
        raise KeyError('You entered wrong action')
    elif action == actions[3]:
        custom_query_mode(cursor)
    else:
        print('Table: ', end='')
        table = input()
        while table not in tables:
            print('Please, try again')
            print('Table: ', end='')
            table = input()

        print('Fields: ', editable_tables[table])

        print('Filter field: ', end='')
        filter_field = input()
        while filter_field not in editable_tables[table]:
            print('Please, try again')
            print('Filter field: ', end='')
            filter_field = input()

        print('Filter value: ', end='')
        filter_value = input()
        try:
            if action == actions[1]:
                print('Update field: ', end='')
                update_field = input()
                while update_field not in editable_tables[table]:
                    print('Please, try again')
                    print('Update field: ', end='')
                    update_field = input()

                print('Update value: ', end='')
                update_value = input()

                request = 'update {} set {} = {} where {} = {}'.format(table, update_field, '%s', filter_field, '%s')
                cursor.execute(request, (update_value, filter_value))
                print('Records updated')

            elif action == actions[2]:
                request = 'delete from {} where {} = {}'.format(table, filter_field, '%s')
                cursor.execute(request, (filter_value,))
                print('Records deleted')

            elif action == actions[0]:
                print('Selected fields (using comma): ', end='')
                selected_field = input()

                while check_selected(selected_field, editable_tables[table]) is not True:
                    print('Please, try again')
                    print('Selected fields (using comma): ', end='')
                    selected_field = input()

                print('Limit (int number or all):', end='')
                limit = int(input())
                limit_str = ' limit ' + str(limit)
                if filter_value == '':
                    request = 'select {} from {}'.format(selected_field, table)
                    if limit:
                        request += limit_str

                    cursor.execute(request)

                else:
                    request = 'select {} from {} where {} = %s limit %s'.format(selected_field, table, filter_field,
                                                                                filter_value)
                    if limit:
                        request += limit_str

                    cursor.execute(request, (filter_value,))

                respond = cursor.fetchall()
                if selected_field != '*':
                    selected_fields = selected_field.split(', ')
                    for s in selected_fields:
                        print(s, end='\t')
                    print()
                for r in respond:
                    for field in r:
                        print(field, end='\t')
                    print()

        except psycopg2.DataError:
            print('You entered wrong value! Try again ')
        except psycopg2.DatabaseError:
            print('There was database error. You have entered something wrong.')


def print_respond(respond):
    for r in respond:
        if len(r) == 1:
            print(r[0])
        elif len(r) == 2:
            print(r[0], r[1], sep='\t\t')
        elif len(r) == 3:
            print(r[0], r[1], r[2], sep='\t\t')
        elif len(r) == 4:
            print(r[0], r[1], r[2], r[3], sep='\t\t')


def find_record_by_name_release_date(cursor, album_name, album_release_date):
    album_name = '%' + album_name + '%'
    sql_album = "select name, cover, release_date from albums where name ilike %s and release_date = %s"
    try:
        cursor.execute(sql_album, (album_name, album_release_date))
    except psycopg2.DataError:
        raise ValueError('You entered wrong data value')
    except psycopg2.DatabaseError:
        raise ValueError('There was database error. You have entered something wrong.')
    album_respond = cursor.fetchall()
    albums = []
    album = dict()
    print('Founded albums: ')
    for x in album_respond:
        album['name'] = x[0]
        print(album['name'], end='\t')

        if x[1] is None:
            album['cover'] = 'No cover'
        else:
            album['cover'] = x[1]
        print(album['cover'], end='\t')

        album['release_date'] = x[2]
        print(album['release_date'], end='\t')
        albums.append(album)

    sql_tracks = "select t.name, t.duration, s.name from track_list " \
                 "join albums a on track_list.album_id = a.id " \
                 "join tracks t on track_list.tracks_id = t.id " \
                 "join tracks_singers ts on t.id = ts.tracks_id " \
                 "join singers s on ts.singers_id = s.id " \
                 "where a.name ilike %s and a.release_date = %s " \
                 "order by a.release_date;"

    cursor.execute(sql_tracks, (album_name, album_release_date))
    track_list_respond = cursor.fetchall()
    artists = set()
    tracks = set()
    for x in track_list_respond:
        artists.add((x[2],))
        tracks.add((x[0], x[1]))

    print('\nArtists: ')
    print_respond(artists)
    print('Track list (name, duration in secs): ')
    print_respond(tracks)


def find_records_by_name(cursor, name, find_action):
    name = '%' + name + '%'

    sql_albums = "select name, release_date from albums " \
                 "where name ilike %s "

    sql_singers_name = "select singers.name, singers.bio, singers.photo, c.name from singers " \
                       "join countries c on c.id = singers.countries_id " \
                       "where singers.name ilike %s "

    sql_genres = "select name from genres " \
                 "where name ilike %s "

    sql_record_labels = "select name from record_labels " \
                        "where name ilike %s "

    sql_tracks = "select name, duration from tracks " \
                 "where name ilike %s "

    action_table = {'album': sql_albums, 'singer': sql_singers_name,
                    'genre': sql_genres, 'record label': sql_record_labels,
                    'track': sql_tracks}

    try:
        cursor.execute(action_table[find_action], (name,))
    except psycopg2.DataError:
        raise ValueError('You entered wrong value! Try again')
    except psycopg2.DatabaseError:
        raise ValueError('There was database error. You have entered something wrong.')
    respond = cursor.fetchall()

    print('Founded items: ')
    print_respond(respond)


def find_albums_by_release_date(cursor, from_date, to_date):
    if len(to_date) == 0:
        sql_find = "select name, release_date from albums where release_date > %s order by release_date, name"
        data = (from_date,)

    else:
        sql_find = "select name, release_date from albums where release_date between %s and %s " \
                   "order by release_date, name"
        data = (from_date, to_date)
    try:
        cursor.execute(sql_find, data)

    except psycopg2.DataError:
        raise ValueError('You entered wrong value! Try again')
    except psycopg2.DatabaseError:
        raise ValueError('There was database error. You have entered something wrong.')
    respond = cursor.fetchall()
    print('Albums (name, release date): ')
    print_respond(respond)


def record_label_partnership(cursor, label_name, from_date, to_date):
    label_name = '%' + label_name + '%'
    if len(to_date) == 0:
        sql_record_label_collabs = "select rl.name, s.name, date_from from label_singer " \
                                   "join record_labels rl on rl.id = label_singer.record_label_id " \
                                   "join singers s on s.id = label_singer.singer_id " \
                                   "where rl.name ilike %s and date_from > %s and date_to is null " \
                                   "order by rl.name, date_from, s.name;"
        data = (label_name, from_date)
        print('Founded records (record label, artists names, date from):')
    else:
        sql_record_label_collabs = "select rl.name, s.name, date_from, date_to from label_singer " \
                                   "join record_labels rl on rl.id = label_singer.record_label_id " \
                                   "join singers s on s.id = label_singer.singer_id " \
                                   "where rl.name ilike %s and date_from > %s and  date_to < %s" \
                                   "order by rl.name, date_from, s.name;"
        data = (label_name, from_date, to_date)
        print('Founded records (record label, artists names, date from, date_to):')
    try:
        cursor.execute(sql_record_label_collabs, data)
    except psycopg2.DataError:
        raise ValueError('You entered wrong value! Try again')
    except psycopg2.DatabaseError:
        raise ValueError('There was database error. You have entered something wrong.')
    respond = cursor.fetchall()
    print_respond(respond)


def find_singers_by_country(cursor, country_name):
    country_name = '%' + country_name + '%'

    sql_country = "select singers.name, singers.bio, c.name from singers " \
                  "join countries c on c.id = singers.countries_id " \
                  "where c.name ilike %s "

    data = (country_name,)

    try:
        cursor.execute(sql_country, data)
    except psycopg2.DataError:
        raise ValueError('You entered wrong value! Try again')
    except psycopg2.DatabaseError:
        raise ValueError('There was database error. You have entered something wrong.')
    respond = cursor.fetchall()
    print('Founded artists (name, bio, country):')
    print_respond(respond)


def find_singer_album_track(cursor, name, option):
    name = '%' + name + '%'
    all_options = {'s': "Founded records (artist's name, album, track, release date): ",
                   'a': "Founded records (album's name, artist, track, release date): ",
                   't': "Founded records (track's name, artist, album, release date): "}
    print_str = all_options[option]
    all_options.__delitem__(option)
    sql_find = "select {}.name, {}.name, {}.name, a.release_date from tracks_singers " \
               "join singers s on s.id = tracks_singers.singers_id " \
               "join tracks t on t.id = tracks_singers.tracks_id " \
               "join track_list tl on t.id = tl.tracks_id " \
               "join albums a on tl.album_id = a.id " \
               "where {}.name ilike %s " \
               "order by {}.name, {}.name, {}.name, a.release_date;".format(option, list(all_options.keys())[0],
                                                                            list(all_options.keys())[1], option, option,
                                                                            list(all_options.keys())[0],
                                                                            list(all_options.keys())[1])
    try:
        cursor.execute(sql_find, (name,))
    except psycopg2.DataError:
        raise ValueError('You entered wrong value! Try again')
    except psycopg2.DatabaseError:
        raise ValueError('There was database error. You have entered something wrong.')
    respond = cursor.fetchall()
    print(print_str)
    print_respond(respond)
