#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

"""Global var to hold the tournament name for testing purposes"""
testTournament = "The Thunderdome"
"""Global var to hold the serial ID of the tournament which is created"""
testTournamentID = -1

def testDeleteTournaments():
    deleteTournaments()
    print "0. Old tournaments can be deleted."


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches and results can be deleted."


def testDeletePlayers():
    deletePlayers()
    print "2. Players and their tournament assignment records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegisterTournament():
    global testTournamentID
    deleteTournaments()
    tournamentRegistered, testTournamentID = registerTournament(testTournament)
    if tournamentRegistered == 1:
        print "4. Tournament was successfully created."
    if tournamentRegistered == 0:
        raise ValueError("Tournament was not created successfully.")

def testRegisterPlayer():
    deleteMatches()
    deletePlayers()
    registerPlayer("Ross Gynn", testTournament)
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "5. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Homer Simpson", testTournament)
    registerPlayer("Marge Simpson", testTournament)
    registerPlayer("Bart Simpson", testTournament)
    registerPlayer("Lisa Simpson", testTournament)
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "6. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray", testTournament)
    registerPlayer("Randy Schwartz", testTournament)
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "7. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton", testTournament)
    registerPlayer("Boots O'Neal", testTournament)
    registerPlayer("Cathy Burton", testTournament)
    registerPlayer("Diane Grant", testTournament)
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(testTournamentID, id1, id2)
    reportMatch(testTournamentID, id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "8. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle", testTournament)
    registerPlayer("Fluttershy", testTournament)
    registerPlayer("Applejack", testTournament)
    registerPlayer("Pinkie Pie", testTournament)
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(testTournamentID, id1, id2)
    reportMatch(testTournamentID, id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "9. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteTournaments()
    testDeleteMatches()
    testDeletePlayers()
    testCount()
    testRegisterTournament()
    testRegisterPlayer()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"


