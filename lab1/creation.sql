drop
    schema public cascade;
create
    schema public;

create table track_list
(
    album_id  int not null,
    tracks_id int not null
);

create table albums
(
    id           serial primary key,
    name         varchar(100) not null,
    genres_id    int,
    cover        bytea,
    release_date date         not null

);

create table tracks
(
    id       serial primary key,
    name     varchar(100)               not null,
    text     text,
    duration int check ( duration > 0 ) not null

);

create table singers
(
    id           serial primary key,
    name         varchar(100) not null,
    bio          text,
    countries_id int,
    photo        bytea

);

create table record_labels
(
    id   serial primary key,
    name varchar(100) not null,
    bio  text
);

create table countries
(
    id   serial primary key,
    name varchar(100) not null
);

create table genres
(
    id   serial primary key,
    name varchar(100) not null
);

create table label_singer
(
    record_label_id int  not null
        references record_labels (id) on delete restrict,
    singer_id       int  not null
        references singers (id) on delete restrict,
    date_from       date not null,
    date_to         date

);

create table tracks_singers
(
    tracks_id  int not null,
    singers_id int not null

);

alter table track_list
    add constraint albums_id_fk foreign key (album_id) references albums (id) on delete restrict,
    add constraint tracks_id_fk foreign key (tracks_id) references tracks (id) on
        delete
        restrict;

alter table albums
    add constraint genre_id_fk foreign key (genres_id) references genres (id) on delete set null;

alter table singers
    add constraint country_id_fk foreign key (countries_id) references countries (id) on delete set null;

alter table tracks_singers
    add constraint singers_track_id_fk foreign key (tracks_id) references tracks (id) on delete restrict,
    add constraint singers_id_fk foreign key (singers_id) references singers (id) on
        delete
        restrict;

create table users
(
    id               serial primary key,
    username         varchar(100) not null unique ,
    admin_privileges boolean      not null,
    password         varchar(100) not null
);

drop table users;