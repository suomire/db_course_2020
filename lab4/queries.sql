-- №1 альбомы за определенный период
explain analyse
select t.name,
       albums.name,
       albums.release_date
from albums
         join track_list tl on albums.id = tl.album_id
         join tracks t on t.id = tl.tracks_id
where release_date between '2018-01-01' and '2020-01-01'
order by albums.name, albums.release_date desc;

create index albums_release_date_idx on albums (release_date);
drop index if exists albums_release_date_idx;

-- №2 исполнители заданной страны
explain analyse
select singers.name as singer_name
from singers
         join countries c on singers.countries_id = c.id
where c.name = 'Russia';

create index singers_countries_id_idx on singers (countries_id);
drop index if exists singers_countries_id_idx;


-- №3 все сотрудничества артист-лейбл по настоящее время
explain analyse
--prepare query_2 as
select rl.name, s.name, date_from
from label_singer
         join record_labels rl on label_singer.record_label_id = rl.id
         join singers s on label_singer.singer_id = s.id
where date_to is null
order by rl.name, s.name;

explain analyse execute query_2;
deallocate query_2;

create index label_singers_idx on label_singer (record_label_id, singer_id) where date_to is null;

create index rlname_idx on record_labels (name);
create index singer_name_idx on singers (name);

drop index if exists label_singers_idx;
drop index rlname_idx;
drop index singer_name_idx;

-- №4 список исполнителей по жанрам
explain analyse
with t1 as (select s.id as sid, t.genres_id as gid, count(*) as nums
            from tracks_singers
                     join singers s on tracks_singers.singers_id = s.id
                     join tracks t on tracks_singers.tracks_id = t.id
            group by sid, gid),
     t2 as (select t1.sid, max(t1.nums) as maxnums from t1 group by t1.sid),
     t3 as (select t1.sid, t1.gid as gid
            from t1
                     join t2 on t1.sid = t2.sid
            where t1.nums = t2.maxnums)
select g.name, s2.name
from t3
         join genres g on t3.gid = g.id
         join singers s2 on t3.sid = s2.id
order by g.name, s2.name;

create index genres_name_idx on genres (name);

drop index genres_name_idx;

-- №5 список треков, входящих в альбом
explain analyse
select a.name, t.name
from track_list
         join albums a on track_list.album_id = a.id
         join tracks t on track_list.tracks_id = t.id
where a.name = 'Visions';

create index albums_name_idx on albums (name);
-- working album_release_idx because it has a name
