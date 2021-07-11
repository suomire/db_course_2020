select t.name, t.duration, s.name
from track_list
         join tracks t on t.id = track_list.tracks_id
         join albums a on a.id = track_list.album_id
         join tracks_singers ts on t.id = ts.tracks_id
         join singers s on ts.singers_id = s.id
where a.name = 'Miss Anthropocene + test'
  and a.release_date = '2020-02-21';

select singers.name, c.name
from singers
         join countries c on c.id = singers.countries_id
where singers.name ilike '%gri%';

select name, singer_id, date_from, date_to
from record_labels
         join label_singer ls on record_labels.id = ls.record_label_id
where record_labels.name ilike '%Arbutus%';


select rl.name, s.name, date_from, date_to
from label_singer
         join record_labels rl on rl.id = label_singer.record_label_id
         join singers s on s.id = label_singer.singer_id
where rl.name ilike '%Arbutus%'
  and date_from > '2009-01-01'
  and date_to < '2020-01-01'
order by date_from, s.name;

select singers.name, singers.bio, singers.photo, c.name
from singers
         join countries c on c.id = singers.countries_id
where c.name ilike '%ussia%';

select s.name, a.name, t.name, a.release_date
from tracks_singers
         join singers s on s.id = tracks_singers.singers_id
         join tracks t on t.id = tracks_singers.tracks_id
         join track_list tl on t.id = tl.tracks_id
         join albums a on tl.album_id = a.id
where s.name ilike '%%'
order by s.name, a.name, t.name, a.release_date;
