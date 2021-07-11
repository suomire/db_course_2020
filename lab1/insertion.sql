insert into countries
values (default, 'Canada'),
       (default, 'UK'),
       (default, 'Russia'),
       (default, 'Germany'),
       (default, 'France'),
       (default, 'Spain'),
       (default, 'Italy'),
       (default, 'USA');


insert into genres
values (default, 'Synth-pop'),
       (default, 'Indie-rock'),
       (default, 'Postpunk'),
       (default, 'Ambient'),
       (default, 'Trip hop'),
       (default, 'Hip-hop');

insert into albums
values (default, 'Visions', (select id from genres where name = 'Synth-pop'), null, '2012-01-31'),
       (default, 'A New Place 2 Drown', (select id from genres where name = 'Trip hop'), null, '2015-12-10'),
       (default, '6 Feet Beneath the Moon', (select id from genres where name = 'Indie-rock'), null, '2013-08-24'),
       (default, 'Art Angels', (select id from genres where name = 'Synth-pop'), null, '2015-11-06'),
       (default, 'Miss Anthropocene ', null, null, '2020-02-21');

insert into record_labels
values (default, 'Arbutus', null),
       (default, '4AD Records', null),
       (default, 'True Panther', null),
       (default, 'XL', null);

insert into singers
values (default, 'Grimes', null, (select id from countries where name = 'Canada'), null),
       (default, 'King Krule', null, (select id from countries where name = 'UK'), null);

insert into tracks
values (default, 'Infinite ♡ Without Fulfillment', null, 96),
       (default, 'So Heavy I Fell Through The Earth', null, 6 * 60 + 8),
       (default, 'Darkseid', null, 3 * 60 + 44),
       (default, 'Delete Forever', null, 3 * 60 + 57),
       (default, 'Violence', null, 3 * 60 + 40),
       (default, '4ÆM', null, 3 * 60 + 15),
       (default, 'New Gods', null, 3 * 60 + 15),
       (default, 'My Name Is Dark', null, 5 * 60 + 56),
       (default, 'You''ll miss me when I''m not around', null, 2 * 60 + 41),
       (default, 'Before the fever', null, 3 * 60 + 37),
       (default, 'IDORU', null, 7 * 60 + 12);

insert into label_singer
values ((select id from record_labels where name = 'Arbutus'), (select id from singers where name = 'Grimes'),
        '2010-01-10', '2015-11-06'),
       ((select id from record_labels where name = '4AD Records'), (select id from singers where name = 'Grimes'),
        (select release_date from albums where name = 'Art Angels'), null),
       ((select id from record_labels where name = 'True Panther'), (select id from singers where name = 'King Krule'),
        (select release_date from albums where name = '6 Feet Beneath the Moon'), null);

insert into track_list
values ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'So Heavy I Fell Through The Earth')),
       ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'Darkseid'));

insert into tracks_singers
values ((select id from tracks where name = 'So Heavy I Fell Through The Earth'),
        (select id from singers where name = 'Grimes')),
       ((select id from tracks where name = 'Darkseid'), (select id from singers where name = 'Grimes')),
       (1, 1),
       (4, 1),
       (5, 1),
       (6, 1),
       (7, 1),
       (8, 1),
       (9, 1),
       (10, 1),
       (11, 1);

update tracks
set text = '[Verse]
I will wait for you if you want me to
(It’s all upon my own way, it’s all upon my own, babe
It’s all upon, it’s all I can do)
I will wait for you if you want me to
I will wait for you if you want me to
(It’s all upon my own way, it’s all upon my own, babe
It’s all upon, it’s all I can do)
I will wait for you if you want me to
I will wait for you if you want me to
(When you want to)
(It’s all upon my own way, it’s all upon my own, babe
It’s all upon, it’s all i can do)
I will wait for you if you want me to
(I will wait for you if you want me to)
I will wait for you if you want me to
(When you want to)
(It’s all upon my own way, it’s all upon my own, babe
It’s all upon, it’s all I can do)

I will wait for you if you want me to
(I will wait for you if you want me to)
I will wait for you if you want me to
(When you want to)
I will wait for you if you want me to
(I will wait for you if you want me to)
I will wait for you if you want me to
(When you want to)
(I will wait wait wait, and I’ll go go go, go at night oh)
I will wait for you if you want me to
(I will wait for you if you want me to
I will wait for you if you want me to
(If you want me to)
(I will leave leave leave, and I’ll go go go, go at night oh)
I will wait for you if you want me to
(I will wait for you if you want me to
I will wait for you if you want me to
(When you want to)
(I will leave leave leave, and I’ll go go go, go at night oh)
I will wait for you if you want me to
(I will wait for you if you want me to
I will wait for you if you want me to
(When you want to)
(I will leave leave leave, and I’ll go go go, go at night oh)
I will wait for you if you want me to
(I will wait for you if you want me to)

I will wait wait wait wait wait wait wait wait wait wait wait wait, oh
(I will wait, I will wait, I will wait, I will wait, I will wait, I will wait)'
where name = 'Infinite ♡ Without Fulfillment';

insert into genres
values (default, 'Ethereal');

update albums
set genres_id = (select id from genres where name = 'Ethereal')
where name = 'Miss Anthropocene ';

insert into track_list
values ((select id from albums where name = 'Visions'),
        (select id from tracks where name = 'Infinite ♡ Without Fulfillment'));


insert into track_list
values ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'Delete Forever')),
       ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'Violence')),
       ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = '4ÆM')),
       ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'New Gods')),
       ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'My Name Is Dark')),
       ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'You''ll miss me when I''m not around')),
       ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'Before the fever')),
       ((select id from albums where name = 'Miss Anthropocene '),
        (select id from tracks where name = 'IDORU'));


insert into label_singer
values (1, 1, '2010-01-01', null)

insert into users values (default, 'db_admin', True, 'coolPassword');


delete
from singers
where name = 'delete test';

insert into singers values (default, 'delete test', null, 3, null);

select name from singers limit all ;