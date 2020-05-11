
# DUOAuthParser

A JSON parser for analyzing the auth methods of users in DUO


To use this program, place your authentication log file (renamed to data.json) in the same directory as the python script.

You will also need to provide a users.txt file containing a subset list of users (one per line all lowercase) that you would like to optionally find the authentication types for. This file must be left blank if not using the feature.

Once both a data.json and user.txt file are present the script can be run.

Requires Python 3.5 or above.
