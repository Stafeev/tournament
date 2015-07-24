#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()  # connect to DB
    c = DB.cursor()  # get cursor
    c.execute('delete from matches')  # execute query
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()  # connect to DB
    c = DB.cursor()  # get cursor
    c.execute('delete from players')  # execute query
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()  # connect to DB
    c = DB.cursor()  # get cursor
    c.execute('select count(*) from players')  # execute query
    result = c.fetchone()
    DB.commit()
    DB.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    bleach.clean(name)
    DB = connect()  # connect to DB
    c = DB.cursor()
    c.execute("Insert into players (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()  # connect to DB
    c = DB.cursor()
    c.execute("select id,name,wins,matches from players order by wins desc")
    standings = []
    for row in c.fetchall():
        standings.append((row[0], row[1], row[2], row[3]))
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    bleach.clean(winner)
    bleach.clean(loser)
    DB = connect()  # connect to DB
    c = DB.cursor()
    c.execute("Insert into matches (winner,loser) VALUES (%s,%s)", (winner, loser,))
    DB.commit()
    c.execute("Update players SET wins=wins+1, matches=matches+1 where id=(%s)", (winner,))
    DB.commit()
    c.execute("Update players SET matches=matches+1 where id=(%s)", (loser,))
    DB.commit()
    DB.close()


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
    listOfPlayers = playerStandings()
    if (len(listOfPlayers) < 2):
        return
    pairs = []
    i = 0  # index of first player
    j = 1  # index of the opponent
    while (j < len(listOfPlayers)):
        tuple = (listOfPlayers[i][0], listOfPlayers[i][1], listOfPlayers[j][0], listOfPlayers[j][1])
        pairs.append(tuple)
        i = j + 1
        j = i + 1
    return pairs
