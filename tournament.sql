-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- A bunch of drop statements to ensure there are no naming conflicts.
-- Order matters to prevent creation of orphans.
-- Wanted to make clean-up easier for you.

-- Drop View leader_board;
-- Drop Table matches;
-- Drop Table players;



-- Create a table of just the players, mapping their names to a unique id

Create Table players (
  id serial primary key,
  name text
);


-- Create a table to hold the individual matches, indicating who faced who and
-- whether player won or not

Create Table matches (
  match_id int not null,
  player_id int references players(id),
  win boolean,
  PRIMARY KEY (match_id, player_id)
);

--Create a view from the following query (in plain english):
  -- Select the player id, their name, their number of matches, and their win count
  -- from player and matches, using a left join to include everyone
  -- and join them on the player id
  -- then group everything by the player id, cause we have to,
  -- and order it by wins because we can satisfy one of the tests by default this way

Create View leader_board as
  select players.id, players.name, (select count (*) from matches where players.id = matches.player_id and win = True) as wins, count(matches.match_id) as matches
  from players left join matches
  on players.id = matches.player_id
  group by players.id order by wins desc;
