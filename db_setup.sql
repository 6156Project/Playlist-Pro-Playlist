create database if not exists PlaylistSong;
use PlaylistSong;

drop table if exists PlaylistSong.playlists;

create table PlaylistSong.playlists (
    playlist_id int primary key,
    playlist_name varchar(30)
);