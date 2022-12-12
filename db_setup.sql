create database if not exists Playlist;
use Playlist;

drop table if exists Playlist.playlists;

create table Playlist.playlists (
    id varchar(39) primary key,
    name varchar(30)
);