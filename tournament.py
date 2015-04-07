#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# import psycopg2 to connect to the db
# import bleach to sanitize inputs just cause we have no idea where they could be coming from
import psycopg2
import bleach

#Reduce redundancy of server calls for delete with utility functions

def commitConnect(arg):
    """ Connect to the PostgreSQL database.
        Runs the basic single arg commit functions.
        Looking at you delete.
    """
    #create db connection
    conn = psycopg2.connect("dbname=tournament")

    #create a cursor
    cur = conn.cursor()

    #execute query passed in
    cur.execute(arg)

    #commit changes
    conn.commit()

    #close cursor and connection
    cur.close()
    conn.close()

def selectConnect(arg):
    """ Connect to the PostgreSQL database.
        Executes select and returns all rows"""

    #create db connection
    conn = psycopg2.connect("dbname=tournament")

    #create a cursor
    cur = conn.cursor()

    #execute the passed in query
    cur.execute(arg)

    #fetch all rows, we can always pare this down later
    rows = cur.fetchall()

    #close cursor and connection
    cur.close()
    conn.close()

    #return the rows back to caller, they can decide what to do with it
    return rows

def sanitize(arg):
    """ Clean up params with bleach before they go into inserts"""

    # take param and strip out any unwanted html etc
    cleaned = bleach.clean(arg, strip=True)

    #return the freshly cleaned param
    return cleaned

def generateMatchId():
    """ Generates match ids.
        They needed to increment but not be unique since n players play a match"""

    #run the below select
    matchCount = selectConnect("Select max(match_id) from matches")

    #placeholder variable
    newCount = 0

    #check the first item of the first row
    if matchCount[0][0] == None:
        #if its empty, set it to 1
        newCount = 1

    #otherwise
    else:
        #take that number
        oldCount = matchCount[0][0]
        #and increment it by 1
        newCount = oldCount + 1

    #return the new match id to the caller
    return newCount

#Begin Basic delete and select functions

def deleteMatches():
    """Remove all the match records from the database."""

    #call commit utility with query
    commitConnect("Delete from matches")

def deletePlayers():
    """Remove all the player records from the database."""

    #call commit utility with query
    commitConnect("Delete from players")


def countPlayers():
    """Returns the number of players currently registered."""

    #call select utility with query
    row = selectConnect("Select count(id) as number from players")

    #return the item in row 0 position 0, this should just be a number not some weird L construct
    return row[0][0]

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

    #call select utility with query
    rows = selectConnect("select * from leader_board")

    #return everything
    return rows

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

    #call select utility with the following query (in plain english):
        # select player 1's user id and their name as well as player 2's user id and name
        # from the leader board view (2x)
        # where they have the same number of wins
        # and they aren't the same person (because we are matching the table against itself)

    rows = selectConnect("select a.id, a.name, b.id, b.name from leader_board a, leader_board b where a.wins = b.wins and a.id < b.id")

    #return everything
    return rows

#Begin insert functions
#No utility functions here because I couldn't account for the number of params going in

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    #new db connection
    conn = psycopg2.connect("dbname=tournament")

    #new cursor
    cur = conn.cursor()

    #sanitize input, who knows where it came from
    sparkly = sanitize(name)

    #build query string
    query = "Insert into Players (name) values (%s)"

    #execute query string with provided param
    cur.execute(query,(sparkly,))

    #commit
    conn.commit()

    #close cursor and connection
    cur.close()
    conn.close()

def reportMatch(p1_outcome, p2_outcome):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    #new db connection
    conn = psycopg2.connect("dbname=tournament")

    #new cursor
    cur = conn.cursor()

    #call to get a new match id
    newCount = generateMatchId()

    #two calls to sanitize inputs
    sparkly = sanitize(p1_outcome)
    sparkly2 = sanitize(p2_outcome)

    #build a query string
    query2 = "Insert into matches (match_id, player_id, win) values(%s, %s, %s)"

    #execute and commit string with winner params, providing true to the wins column to signify they won
    cur.execute(query2,(newCount, sparkly, True,))
    conn.commit()

    #execute and commit string with loser params, providing false to the wins column to signify they lost
    cur.execute(query2,(newCount, sparkly2, False,))
    conn.commit()

    #close connection and cursor
    cur.close()
    conn.close()
