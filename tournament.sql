-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE players (
    ID serial primary key,
    name varchar(50) NOT NULL,
    wins int default 0,
    matches int default 0
)
WITH (
  OIDS=FALSE
);
CREATE TABLE matches (
     winner int NOT NULL,
     loser int NOT NULL,
     PRIMARY KEY(winner,loser)
)
WITH (OIDS=FALSE);
