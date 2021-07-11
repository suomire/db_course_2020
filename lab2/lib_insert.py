import pandas as pd
from mimesis import Generic
import random
import psycopg2.extras

g = Generic()


class InsertFunctions:

    def __init__(self, param):
        self.parameter = param

    # get and insert countries from csv
    @staticmethod
    def insert_countries(cursor, table_countries):
        countries = pd.read_csv('data/world_2.csv', sep=',')
        add_set = set((x,) for x in countries.name)
        add_set = add_set - set(table_countries)

        sql = 'insert into countries (name) values (%s)'

        psycopg2.extras.execute_batch(cursor, sql, list(add_set))

        cursor.execute("select id from countries")
        table_countries = cursor.fetchall()

        return table_countries

    # get and insert genres as
    @staticmethod
    def insert_genres(cursor, table_genres):
        add_set = set()
        f = open('data/genres.txt', 'r')
        for x in f:
            add_set.add((x.split('\n')[0],))

        add_set = add_set - set(table_genres)

        sql = 'insert into genres (name) values (%s)'
        psycopg2.extras.execute_batch(cursor, sql, list(add_set))

        cursor.execute("select id from genres")
        table_genres = cursor.fetchall()
        return table_genres

    def insert_record_labels(self, cursor, table_record_labels):
        add_set = set()
        add_list = []
        sql = 'insert into record_labels (name, bio) values (%s, %s)'
        if self.parameter > 1000:  # 1143 - опытным путем
            param = 1000
        else:
            param = self.parameter

        for i in range(param):
            name = g.business.company()
            add_set.add((name,))

        add_set = list(add_set - set(table_record_labels))

        for x in add_set:
            if random.randint(0, 5) < 3:
                bio = g.text.text(random.randint(1, 5))
            else:
                bio = None
            elem_tuple = (x[0], bio)
            add_list.append(elem_tuple)

        psycopg2.extras.execute_batch(cursor, sql, add_list)

        cursor.execute("select id from record_labels")
        table_record_labels = cursor.fetchall()
        return table_record_labels

    def insert_singers(self, cursor, table_singers, table_countries):
        res = 1
        add_set = set()
        add_list = []
        for i in range(self.parameter):
            a = random.randint(0, 2)
            if a == 0:
                name = g._person().name() + " " + g._person().surname()
            elif a == 1:
                name = g.text.word().capitalize()
            else:
                name = g.text.word().capitalize() + " " + g.text.word().capitalize()
            country_id = table_countries[random.randint(0, len(table_countries) - 1)]
            add_set.add((name, country_id))

        add_set = add_set - set(table_singers)
        for x in add_set:
            a = random.randint(0, 2)
            if a > 1:
                bio = None
                photo = g.person.avatar()
            else:
                bio = g.text.text(random.randint(1, 3))
                photo = None
            add_list.append((x[0], bio, x[1], photo))

        sql = 'insert into singers (name, bio, countries_id, photo) values (%s, %s, %s, %s)'

        psycopg2.extras.execute_batch(cursor, sql, add_list)
        cursor.execute("select id from singers")
        table_singers = cursor.fetchall()
        return table_singers

    def insert_albums(self, cursor, table_albums):
        add_list = []
        add_set = set()
        for i in range(self.parameter):
            name = g.text.word().upper() + " " + g.text.word().upper()
            release_date = g.datetime.date(start=2020, end=2020)
            add_set.add((name, release_date))

        add_set = add_set - set(table_albums)
        for x in add_set:
            if random.randint(0, 5) < 3:
                cover = None
            else:
                cover = g.person.avatar()
            add_list.append((x[0], cover, x[1]))

        sql = 'insert into albums (name, cover, release_date) values (%s, %s, %s)'

        psycopg2.extras.execute_batch(cursor, sql, add_list)

        cursor.execute("select id from albums")
        table_albums = cursor.fetchall()
        return table_albums

    def insert_tracks(self, cursor, table_tracks, table_genres):
        add_list = []
        add_set = set()
        for i in range(self.parameter * 2):
            name = g.text.word().lower() + " " + g.text.word().lower()
            if random.randint(0, 5) < 3:
                duration = 1
            else:
                duration = random.randint(1, 6000)
            add_set.add((name, duration))

        add_set = add_set - set(table_tracks)
        for x in add_set:
            if random.randint(0, 5) < 3:
                text = g.text.text(random.randint(1, 10))
            else:
                text = None
            genre_id = table_genres[random.randint(1, len(table_genres) - 1)]
            add_list.append((x[0], genre_id, text, x[1]))

        sql = 'insert into tracks (name, genres_id, text, duration) values (%s, %s, %s, %s)'
        psycopg2.extras.execute_batch(cursor, sql, add_list)

        cursor.execute("select id from tracks")
        table_tracks = cursor.fetchall()
        return table_tracks

    def insert_track_list(self, cursor, table_tracks, table_albums, table_track_list):
        add_set = set()
        num_albums = len(table_albums) - self.parameter - 1
        for id in table_albums[num_albums:]:
            for i in range(random.randint(a=1, b=7)):
                num_tracks = len(table_albums) - self.parameter - 1
                t = table_tracks[random.randint(num_tracks, len(table_tracks) - 1)]
                add_set.add((id, t))

        add_set = add_set - set(table_track_list)
        sql = 'insert into track_list (album_id, tracks_id) values (%s, %s)'
        psycopg2.extras.execute_batch(cursor, sql, list(add_set))

    def insert_tracks_singers(self, cursor, table_tracks, table_singers, table_tracks_singers):
        add_set = set()
        for i in range(self.parameter * 2):
            num = len(table_singers) - self.parameter - 1
            s = table_singers[random.randint(0, len(table_singers) - 1)]
            # s = table_singers[random.randint(num, len(table_singers) - 1)]
            t = table_tracks[random.randint(num, len(table_tracks) - 1)]
            add_set.add((t, s))

        add_set = add_set - set(table_tracks_singers)
        sql = 'insert into tracks_singers (tracks_id, singers_id) values (%s, %s)'
        psycopg2.extras.execute_batch(cursor, sql, list(add_set))

    def insert_label_singer(self, cursor, table_record_labels, table_singers, table_label_singer):
        add_set = set()
        for i in range(self.parameter * 2):
            rl = table_record_labels[random.randint(0, len(table_record_labels) - 1)]
            s = table_singers[random.randint(0, len(table_singers) - 1)]

            date1 = g.datetime.date(start=2017, end=2020)
            date2 = g.datetime.date(start=2017, end=2020)
            min_date = min(date1, date2)
            max_date = max(date1, date2)

            if random.randint(0, 5) > 0:
                max_date = None
            add_set.add((rl, s, max_date, min_date))

        add_set = add_set - set(table_label_singer)
        sql = 'insert into label_singer (record_label_id, singer_id, date_to, date_from) values (%s, %s, %s, %s)'
        psycopg2.extras.execute_batch(cursor, sql, list(add_set))
