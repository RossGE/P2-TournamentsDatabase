# Tournaments Database FS0415
This project was created for Udacity Nanodegree FS0415

## What's Included?
The following files are included in this project:
- .vagrant
-- Vagrant VM config files
- tournament
-- tournament.py: Python code for the tournament database
-- tournament.sql: PostgreSQL database objects
-- tournament_test.py: Test suite for the Python functions
- README.md

## Requirements
- VirtualBox
- vagrant
- Python 2.7.6

## Installation
Install the tournament.sql file to postgre:

```bash
psql -f tournament.sql
```

## Execution
Run the test script to unit test the application:

```bash
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
1. Old matches and results can be deleted.
2. Players and their tournament assignment records can be deleted.
3. After deleting, countPlayers() returns zero.
4. Tournament was successfully created.
5. After registering a player, countPlayers() returns 1.
6. Players can be registered and deleted.
7. Newly registered players appear in the standings with no matches.
8. After a match, players have updated standings.
9. After one match, players with one win are paired.
Success!  All tests pass!
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$
```
