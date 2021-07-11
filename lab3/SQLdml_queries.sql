/*
Список стандартных запросов

Создайте запрос, рассчитывающий совокупную характеристику с использованием группировки,
    наложите ограничение на результат группировки

*/

--Сделайте выборку всех данных из каждой таблицы
select *
from countries;
select *
from genres;
select *
from record_labels;
select *
from singers;
select *
from tracks;
select *
from albums;
select *
from label_singer;
select *
from tracks_singers;
select *
from track_list;

/*Сделайте выборку данных из одной таблицы при нескольких условиях,
    с использованием логических операций, LIKE, BETWEEN, IN (не менее 3-х разных примеров)*/
-- like
select name
from albums
where name like '%OO%';

select *
from tracks
where text not like '%pants%';

select *
from singers
where name like 'B__';

select tracks.name
from tracks
where tracks.name ilike 'b%';

-- between
select *
from tracks
where duration not between 30 and 300
order by duration;

select *
from albums
where release_date between '1999-01-01' and '2012-01-01';

select *
from label_singer
where date_from between '2001-01-01' and '2011-01-01'
  and date_to IS NULL
order by date_to;

-- in
select *
from label_singer
where singer_id not in (1, 5, 7);

select *
from track_list
where album_id in (4, 14)
order by track_list.album_id;

select *
from countries
where id in (select countries_id from singers);

-- Создайте в запросе вычисляемое поле
select *
from tracks
where duration > (select avg(duration) from tracks)
order by duration desc;


-- Сделайте выборку всех данных с сортировкой по нескольким полям
select *
from track_list
order by album_id desc, tracks_id desc;


-- Создайте запрос, вычисляющий несколько совокупных характеристик таблиц
select min(date_from), max(date_to)
from label_singer;


-- Сделайте выборку данных из связанных таблиц (не менее двух примеров)
select t.name, a.name, t.duration
from track_list
         inner join tracks t on track_list.tracks_id = t.id
         inner join albums a on track_list.album_id = a.id;

select singers.name, c.name, singers.bio
from singers
         inner join countries c on singers.countries_id = c.id; --пересечение множеств

select *
from genres,
     countries;

select *
from genres
         left join tracks t on genres.id = t.genres_id
order by genres.id;

-- Создайте запрос, рассчитывающий совокупную характеристику с использованием группировки, наложите ограничение на результат группировки
select tracks_id, count(tracks_id) as sum_singers
from tracks_singers
group by tracks_id
having count(tracks_id) > 4;

select count(*)
from tracks_singers;

-- Придумайте и реализуйте пример использования вложенного запроса

select singers.name, c.name
from singers
         join countries c on singers.countries_id = c.id
where countries_id in (select id from countries where name ilike 'c%');


select a.name, count(distinct genres_id)
from track_list
         inner join albums a on track_list.album_id = a.id
         inner join tracks t on track_list.tracks_id = t.id
group by a.name
order by count(distinct genres_id);

select count(genres_id)
from tracks;

-- С помощью оператора INSERT добавьте в каждую таблицу по одной записи
insert into genres
values (default, 'test genre');
insert into countries
values (default, 'Test country');

insert into albums
values (default, 'TEST ALBUM', null, '2010-01-01');
insert into record_labels
values (default, 'Test label', null);
insert into singers
values (default, 'Test Singer', null, (select id from countries where name = 'Test country'), null);
insert into tracks
values (default, 'test track', null, 1, (select id from genres where name = 'test genre'));

insert into label_singer
values ((select id from record_labels where name = 'Test label'),
        (select id from singers where name = 'Test Singer'), '2010-01-01');
insert into track_list
values ((select id from albums where name = 'TEST ALBUM'),
        (select id from tracks where name = 'test track'));
insert into tracks_singers
values ( (select id from tracks where name = 'test track')
       , (select id from singers where name = 'Test Singer'));


-- С помощью оператора UPDATE измените значения нескольких полей у всех записей, отвечающих заданному условию
update singers
set countries_id = (select id from countries where countries.name = 'Test country')
where countries_id = (select id from countries where countries.name = 'Canada');

-- С помощью оператора DELETE удалите запись, имеющую максимальное (минимальное) значение некоторой совокупной характеристики
delete
from track_list
where album_id in (select album_id
                   from (select album_id, count(album_id) as num_of_tracks
                         from track_list
                         group by album_id) as tt2
                   where num_of_tracks = (select min(num_of_tracks)
                                          from (select album_id, count(album_id) as num_of_tracks
                                                from track_list
                                                group by album_id) as tt1));
-- С помощью оператора DELETE удалите записи в главной таблице, на которые не ссылается подчиненная таблица (используя вложенный запрос)
delete
from albums
where id not in (select album_id from track_list group by album_id);

select count(id)
from albums;


