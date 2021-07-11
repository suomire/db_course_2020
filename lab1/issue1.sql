/*Внесение изменений в структуру БД
Добавить жанры для треков и убрать их у альбомов. Жанр альбома будет собираться из комбинации жанров всех треков, входящих в него.

Также необходимо сохранить уже имеющиеся данные в БД после реорганизации структуры: для каждого трека проставить жанр альбома,
в котором он находится на тот момент. */

alter table tracks
    add column genres_id integer;

alter table tracks
    add constraint genre_id_fk foreign key (genres_id) references genres (id) on delete set null;


/*select tracks.id, albums.genres_id
from tracks
         join track_list on tracks.id = track_list.tracks_id
         join albums on track_list.album_id = albums.id;*/

update tracks
set genres_id = albums.genres_id
from albums
         join track_list on albums.id = track_list.album_id

where tracks.id = track_list.tracks_id;

alter table albums
    drop column genres_id;


/*
select *
from countries
         full outer join singers singer on countries.id = singer.countries_id;

insert into singers
values (default, 'Name', null, null, null);

select id
from singers
EXCEPT
select singers_id
from tracks_singers;

delete from singers where name ='Name';

select * from singers;


delete from countries;
delete from genres;
delete from label_singer;
delete from track_list;
delete from tracks_singers;
delete from albums;
delete from record_labels;
delete from singers;
delete from tracks;

select * from track_list where album_id=55 and tracks_id=102;*/
