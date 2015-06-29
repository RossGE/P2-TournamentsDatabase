#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from random import randint

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def connectOpen():
    """Connect to the database and open a cursor

    Returns:
        - connection object
        - cursor object
    """
    dbConnect = connect()
    dbCursor = dbConnect.cursor()

    return dbConnect, dbCursor

def deleteMatches():
    """Remove all the match and result records from the database."""
    db, cursor = connectOpen()
    cursor.execute("DELETE FROM match_results;")
    cursor.execute("DELETE FROM matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player definitions and registrations from the database."""
    db, cursor = connectOpen()
    cursor.execute("DELETE FROM tournament_registrations;")
    cursor.execute("DELETE FROM players;")
    db.commit()
    db.close()

def deleteTournaments():
    """Remove all the tournament definitions and registrations from the database."""
    db, cursor = connectOpen()
    cursor.execute("DELETE FROM tournament_registrations;")
    cursor.execute("DELETE FROM tournaments;")
    db.commit()
    db.close()


def countPlayers(argTournamentName=0):
    """Returns the number of players currently registered.

    Arguments:
        - Optionally pass the tournament ID to get players registered 
        in a specific tournament

    Returns:
        - Integer: number of players globally or in a specific tournament
    """
    db, cursor = connectOpen()

    """Restrict the where clause if a specific tournament was selected"""
    if argTournamentName != 0:
        cursor.execute("SELECT COUNT(*) FROM tournament_registrations WHERE tournament_id = %s;", (argTournamentName, ))
    else:
	cursor.execute("SELECT COUNT(*) FROM players;")

    playerCount = cursor.fetchone()[0]
    db.close()

    return int(playerCount)


def registerPlayer(argPlayerName, argTournamentName=0):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Arguments:
        - argPlayerName: the player's full name (need not be unique).
        - Optionally pass argTournamentName to register a player to a specific tournament 
    """
    db, cursor = connectOpen()
    cursor.execute("INSERT INTO players (player_name) VALUES (%s) RETURNING player_id;", 
        (argPlayerName, )
    )

    """Get serial ID of newly created player"""
    newPlayerID = cursor.fetchone()[0]

    """Also create a player tournament registration if requested"""
    if argTournamentName != 0:
	"""Get tournament ID from tournaments table for insert into registrations table"""
        cursor.execute("SELECT tournament_id FROM tournaments WHERE tournament_name = %s", (argTournamentName, ))
        tournamentID = cursor.fetchone()[0]        
        cursor.execute("INSERT INTO tournament_registrations VALUES (%s, %s);", 
	        (tournamentID, newPlayerID)
	    )

    db.commit()
    db.close()

def registerTournament(argTournamentName):
    """Adds a tournament to the tournament database.

    The database assigns a unique serial id number for the tournament

    Arguments:
        - argTournamentName: the name of the tournament

    Returns:
        - Count of 1 to indicate the tournament has been created successfully
        - ID of the tournament - this needs to be passed to the 
		match / pairing functions later
    """
    db, cursor = connectOpen()
    cursor.execute("INSERT INTO tournaments (tournament_name) VALUES (%s) RETURNING tournament_id;", 
        (argTournamentName, )
    )

    """Get serial ID of the new tournament"""
    newTournamentID = cursor.fetchone()[0]
    db.commit()

    """Verify the right tournament ID was obtained and the tournament was created"""
    cursor.execute("SELECT COUNT(*) FROM tournaments WHERE tournament_id = %s", 
        (newTournamentID, )
    )
    tournamentCreated = cursor.fetchone()[0]
    db.close()

    return tournamentCreated, newTournamentID


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (tournament, id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connectOpen()
    cursor.execute("SELECT * FROM player_standings;")
    standings = cursor.fetchall()

    return standings


def reportMatch(tournament, player1, player2):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the id of the tournament this match is for
      player1:  the id number of the first player 
	            (this will be the winner in the _test.py script)
      player2:  the id number of the second player
    """

    """First create the match in matches table, randomising which player is 
    the home player

    (NOTE - Udacity reviewers: I wanted to do it this way to allow for matches 
    to be paired up / scheduled randomly ahead of time in the database in future, 
    then results reported on after!)
    """

    db, cursor = connectOpen()
    if randint(1, 10) % 2 == 0:
        cursor.execute("INSERT INTO matches (tournament_id, home_player, away_player) VALUES (%s, %s, %s) RETURNING match_id;", 
            (tournament, player1, player2)
        )
    else:
        cursor.execute("INSERT INTO matches (tournament_id, home_player, away_player) VALUES (%s, %s, %s) RETURNING match_id;", 
            (tournament, player2, player1)
        )
    matchID = cursor.fetchone()[0]
    
    """Next set the winner and loser and insert into match_results table"""
    cursor.execute("INSERT INTO match_results VALUES (%s, %s, %s)",
        (matchID, player1, player2)
    )

    db.commit()
    db.close()       
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    """Get player standings from the function -> ordered view"""
    standingResults = playerStandings()

    """Loop over standing results two records at a time"""
    matchPairs = []    
    for p in range(0, len(standingResults), 2):
        """Set player1 to the first record in this pair, 
		player2 to second record
		"""
        player1 = standingResults[p]
        player2 = standingResults[p + 1]
        
        """Create paired list of tuples 
		(note: col 0 is id, col 1 is name - see playerStandings()
		"""
        matchPairs.append(
            [player1[0],
            player1[1],
            player2[0], 
            player2[1]]
        )

    return matchPairs
