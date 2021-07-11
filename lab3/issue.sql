/*
    Для каждого запроса привести его план запроса (explain analyze) и пояснения.
*/

/*    Для каждого лейбла вывести исполнителей, которые стали наименее интересны лейблу для сотрудничества.
Интерес перестают представлять исполнители, которые в течение последнего года выпустили менее 5 новых треков.

Дату выпуска трека оценить по дате выпуска самого первого альбома среди тех, в которые этот трек входит.
*/

--получить дату релиза каждого трека
select album_id, tracks_id, release_date
from track_list
         join tracks t on track_list.tracks_id = t.id
         join albums a on track_list.album_id = a.id;

-- сопоставить трек с исполнителем и с минимальной датой релиза для комбинации "трек-исполнитель"
with t1 as (select album_id, tracks_id, release_date
            from track_list
                     join tracks t on track_list.tracks_id = t.id
                     join albums a on track_list.album_id = a.id)

select s.id                                   as sid,
       d.tracks_id                            as tid,
       min(extract(year from d.release_date)) as rdate
from tracks_singers
         join singers s on tracks_singers.singers_id = s.id
         join t1 d on tracks_singers.tracks_id = d.tracks_id
group by d.tracks_id, s.id
order by s.id, min(extract(year from d.release_date)) desc, d.tracks_id
;


-- сопоставить треки-исполнители-лейблы на основе даты выпуска трека:
-- должна быть больше чем date_from, a date_to = null;
--вывод непродуктивных артистов
explain analyze
with t1 as (select album_id, tracks_id, release_date
            from track_list
                     join tracks t on track_list.tracks_id = t.id
                     join albums a on track_list.album_id = a.id),
     t2 as (select s.id as sid, d.tracks_id as tid, min(d.release_date) as rdate
            from tracks_singers
                     join singers s on tracks_singers.singers_id = s.id
                     join t1 d on tracks_singers.tracks_id = d.tracks_id
            group by d.tracks_id, s.id)

select record_label_id as rid,
       sid,
       count(*)        as total_tracks
from label_singer
         join t2 iim on label_singer.singer_id = iim.sid
where date_to IS NULL       --значит что сотрудничество еще продолжается
  and iim.rdate > date_from -- выпуск трека произошел во время сотрудничества
  and extract(year from iim.rdate) = 2020
  --and extract(year from iim.rdate) = extract(year from current_date) -- в течение текущего года
group by rid, sid
having count(*) < 5
order by total_tracks desc, sid;



insert into albums
values (default, 'Test album 2021', null, '2020-12-30');

insert into tracks
values (default, 'Test track 2021', 'empty....', 1001, 2);

insert into tracks_singers
values (22291, 15);
insert into track_list
values (11147, 22291);



/*---------------------------------------------------------------------------------------------------------*/

--Вывести артистов, которые теряют продуктивность.
--Таковыми считать тех, кто за последние 3 года с каждым годом выпускает меньше треков, чем в предыдущем.
--Оценку даты выпуска трека производить аналогично п.1.

--выводим у каждого исполнителя список всех его треков по годам
with t1 as (select album_id,
                   tracks_id,
                   release_date
            from track_list
                     join tracks t on track_list.tracks_id = t.id
                     join albums a on track_list.album_id = a.id
)
select s.id                                   as sid,
       d.tracks_id                            as tid,
       extract(year from min(d.release_date)) as rdate
from tracks_singers
         join singers s on tracks_singers.singers_id = s.id
         join t1 d
              on tracks_singers.tracks_id = d.tracks_id
group by sid, tid
order by sid, rdate desc, tid
;

--теперь группируем по годам чтобы все посчитать
with t1 as (select album_id,
                   tracks_id,
                   release_date
            from track_list
                     join tracks t on track_list.tracks_id = t.id
                     join albums a on track_list.album_id = a.id
),
     t2 as (select s.id                                   as sid,
                   d.tracks_id                            as tid,
                   extract(year from min(d.release_date)) as rdate
            from tracks_singers
                     join singers s on tracks_singers.singers_id = s.id
                     join t1 d
                          on tracks_singers.tracks_id = d.tracks_id
            group by sid, tid)

select sid, count(*) as num_of_tracks
from t2
where rdate = extract(year from current_date) - 1 --2020
group by sid;

--получаю таблицу с показателями эффективности,
with t1 as (select album_id,
                   tracks_id,
                   release_date
            from track_list
                     join tracks t on track_list.tracks_id = t.id
                     join albums a on track_list.album_id = a.id
),
     t2 as (select t.id                                   as tid,
                   s.id                                   as sid,
                   extract(year from min(d.release_date)) as rdate
            from tracks_singers
                     join singers s on tracks_singers.singers_id = s.id
                     join tracks t on tracks_singers.tracks_id = t.id
                     join t1 d
                          on tracks_singers.tracks_id = d.tracks_id
            group by t.id, s.id),
     t3 as (select sid, count(*) as t17
            from t2
            where rdate = '2017'
            group by sid),
     t4 as (select sid, count(*) as t18
            from t2
            where rdate = '2018'
            group by sid),
     t5 as (select sid, count(*) as t19
            from t2
            where rdate = '2019'
            group by sid),
     t6 as (select sid, count(*) as t20
            from t2
            where rdate = '2020'
            group by sid)


select singers.id       as sid,
       coalesce(t17, 0) as t17,
       coalesce(t18, 0) as t18,
       coalesce(t19, 0) as t19,
       coalesce(t20, 0) as t20
from singers
         left join t3 on singers.id = t3.sid
         left join t4 on singers.id = t4.sid
         left join t5 on singers.id = t5.sid
         left join t6 on singers.id = t6.sid;

--получаю таблицу с решением об эффективности артистов за последние три года
explain (analyze)
with t1 as (select album_id, tracks_id, release_date
            from track_list
                     join tracks t on track_list.tracks_id = t.id
                     join albums a on track_list.album_id = a.id),
     t2 as (select t.id as tid, s.id as sid, extract(year from min(d.release_date)) as rdate
            from tracks_singers
                     join singers s on tracks_singers.singers_id = s.id
                     join tracks t on tracks_singers.tracks_id = t.id
                     join t1 d on tracks_singers.tracks_id = d.tracks_id
            group by t.id, s.id),
     t3 as (select sid, count(*) as t17 from t2 where rdate = extract(year from current_date) - 3 - 1 group by sid),
     t4 as (select sid, count(*) as t18 from t2 where rdate = extract(year from current_date) - 2 - 1 group by sid),
     t5 as (select sid, count(*) as t19 from t2 where rdate = extract(year from current_date) - 1 - 1 group by sid),
     t6 as (select sid, count(*) as t20 from t2 where rdate = extract(year from current_date) group by sid),
     t7 as (select singers.id       as sid,
                   coalesce(t17, 0) as t17,
                   coalesce(t18, 0) as t18,
                   coalesce(t19, 0) as t19,
                   coalesce(t20, 0) as t20
            from singers
                     left join t3 on singers.id = t3.sid
                     left join t4 on singers.id = t4.sid
                     left join t5 on singers.id = t5.sid
                     left join t6 on singers.id = t6.sid)

select sid, (t18 >= t17 and t19 >= t18 and t20 >= t19) as answ
from t7
where (t18 >= t17 and t19 >= t18 and t20 >= t19) is True;

-- выбираю только тех кто неэффективен и присоединяю таблицу с лейблами для конечного вывода результатов,
-- учитывая только те лейблы, с которыми сотрудничество еще продолжается

with t1 as (select album_id,
                   tracks_id,
                   release_date
            from track_list
                     join tracks t on track_list.tracks_id = t.id
                     join albums a on track_list.album_id = a.id
),
     t2 as (select t.id                                   as tid,
                   s.id                                   as sid,
                   extract(year from min(d.release_date)) as rdate
            from tracks_singers
                     join singers s on tracks_singers.singers_id = s.id
                     join tracks t on tracks_singers.tracks_id = t.id
                     join t1 d
                          on tracks_singers.tracks_id = d.tracks_id
            group by t.id, s.id),
     t3 as (select sid, count(*) as t17
            from t2
            where rdate = extract(year from current_date) - 3 - 1
            group by sid),
     t4 as (select sid, count(*) as t18
            from t2
            where rdate = extract(year from current_date) - 2 - 1
            group by sid),
     t5 as (select sid, count(*) as t19
            from t2
            where rdate = extract(year from current_date) - 1 - 1
            group by sid),
     t6 as (select sid, count(*) as t20
            from t2
            where rdate = extract(year from current_date)
            group by sid),
     t7 as (select singers.id       as sid,
                   coalesce(t17, 0) as t17,
                   coalesce(t18, 0) as t18,
                   coalesce(t19, 0) as t19,
                   coalesce(t20, 0) as t20
            from singers
                     left join t3 on singers.id = t3.sid
                     left join t4 on singers.id = t4.sid
                     left join t5 on singers.id = t5.sid
                     left join t6 on singers.id = t6.sid),
     t8 as (select sid, (t18 >= t17 and t19 >= t18 and t20 >= t19) as answ
            from t7
            where (t18 >= t17 and t19 >= t18 and t20 >= t19) is False)


select ls.record_label_id as rid, t8.sid
from t8
         join label_singer ls on t8.sid = ls.singer_id
where date_to is null
order by rid, t8.sid
;

/*---------------------------------------------------------------------------------------------------------*/

/*    Для каждого исполнителя вывести его жанр на основании наиболее часто встречающемся жанре его треков.*/

--сопоставим исполнителей и треки, добавим инфо о жанрах,
--сгруппируем по исполнитель-жанр, посчитаем кол-во таких записей
select s.id        as sid,
       t.genres_id as gid,
       count(*)    as nums
from tracks_singers
         join singers s on tracks_singers.singers_id = s.id
         join tracks t on tracks_singers.tracks_id = t.id
group by sid, gid
order by sid, gid;

--поиск максимального значения по жанрам
with t1 as (select s.id        as sid,
                   t.genres_id as gid,
                   count(*)    as nums
            from tracks_singers
                     join singers s on tracks_singers.singers_id = s.id
                     join tracks t on tracks_singers.tracks_id = t.id
            group by sid, gid)
select t1.sid, max(t1.nums) as maxnums
from t1
group by t1.sid;

--объединим t1 и их максимальное значение
explain (analyze)
with t1 as (select s.id as sid, t.genres_id as gid, count(*) as nums
            from tracks_singers
                     join singers s on tracks_singers.singers_id = s.id
                     join tracks t on tracks_singers.tracks_id = t.id
            group by sid, gid),
     t2 as (select t1.sid, max(t1.nums) as maxnums from t1 group by t1.sid)

select t1.sid, t1.gid as gid, t1.nums, t2.maxnums
from t1
         join t2 on t1.sid = t2.sid
where t1.nums = t2.maxnums

order by sid, nums desc, gid;


insert into tracks
values (default, 'TEST SONG FOR 2 SINGER new', NULL, 100, 164);

insert into tracks_singers
values ((select id from tracks where name = 'TEST SONG FOR 2 SINGER new'), 2);

select bio, coalesce(bio, 'str')
from singers