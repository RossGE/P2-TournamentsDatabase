-- Table definitions for the tournament project.
--
-- Author: Ross Gynn
--
-- Design Notes:
--	= Assumption that players can enter more than one tournament, but only one used for this test
--	= Assumption that there are no ties, one winner and one loser per match
--	= Players are either the "home" or "away" player each match
--	= Strive for high normalization to reduce data redundancy
-- 
-- Resubmission Notes:
-- 	= Added DROP DATABASE IF EXISTS
--	= Added primary key to tournament_registrations
--	= Didn't change MATCHES to a view as suggested:
--	  - Need this to be a table as it actually defines the match pairings
--	  - I did this as I wanted the structure to be able to handle scheduled matches without results yet in future

-- Drop the database if it already exists
DROP DATABASE IF EXISTS tournament;

-- Create and connect to the tournament database
CREATE DATABASE tournament;
\c tournament

-- Tournament definitions
CREATE TABLE tournaments (
	tournament_id SERIAL PRIMARY KEY,
	tournament_name VARCHAR(100)
);

-- Player definitions
CREATE TABLE players (
	player_id SERIAL PRIMARY KEY,
	player_name VARCHAR(100) NOT NULL
);

-- Players registered to each tournament
CREATE TABLE tournament_registrations (
	registration_id SERIAL PRIMARY KEY,
        tournament_id INT REFERENCES tournaments(tournament_id),
        player_id INT REFERENCES players(player_id)
);

-- Tournament match pairing definitions
CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	tournament_id INT REFERENCES tournaments(tournament_id),
	home_player INT REFERENCES players(player_id),
	away_player INT REFERENCES players(player_id)
);

-- Results of each match
CREATE TABLE match_results (
	match_id INT REFERENCES matches(match_id),
	match_winner INT REFERENCES players(player_id),
	match_loser INT REFERENCES players(player_id)
);


CREATE OR REPLACE VIEW player_standings AS 
	SELECT 		p.player_id AS id,
			p.player_name AS name,
			(
				select count(*) from match_results r
				where r.match_winner = p.player_id
			) wins,
			(
			select count(*) from matches m
			where (m.home_player = p.player_id OR
				m.away_player = p.player_id)
			) matches
	FROM		players p, 
			tournament_registrations reg,
			tournaments t
	WHERE		p.player_id = reg.player_id
	AND		reg.tournament_id = t.tournament_id
	AND		t.tournament_name = 'The Thunderdome'
	ORDER BY	wins desc;
	

