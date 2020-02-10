import time
import curses
from curses import wrapper
import json



def output_progress(scr, log_num, log_total, users, factors):
    scr.addstr(5, 0, "Progress: " + str(log_num) + " / " + str(log_total))
    scr.addstr(6, 0, "Unique Users: " + str(len(users)))

    scr.addstr(8, 0, "Total AuthTypes:")
    base_coord = 9

    for z in factors:
        scr.addstr(base_coord, 0, "  " + z + ": ")                          # Factor Type Name
        scr.addstr(base_coord, 23, str(factors.get(z)) )                    # Number appearances
        scr.addstr(base_coord, 34, str( round((factors.get(z) / log_num)*100, 2) ) + " %   " )    # Percent of Total
        base_coord += 1

    scr.refresh()


def output_userdata(scr, users, log_total, userdata):
    scr.addstr(21, 0, "AuthTypes per User:")

    base_coord = 22

    for z in userdata:
        scr.addstr(base_coord, 0, "  " + z + ": ")                          # Factor Type Name
        scr.addstr(base_coord, 23, str(userdata.get(z)) )                    # Number appearances
        scr.addstr(base_coord, 34, str( round((userdata.get(z) / len(users))*100, 2) ) + " %   " )    # Percent of Total
        base_coord += 1

    scr.refresh()


def output_specific_userdata(scr, users, log_total, userdata, specific_user_num):
    scr.addstr(32, 0, "AuthTypes per User:")

    base_coord = 33

    for z in userdata:
        scr.addstr(base_coord, 0, "  " + z + ": ")                          # Factor Type Name
        scr.addstr(base_coord, 23, str(userdata.get(z)) )                    # Number appearances
        scr.addstr(base_coord, 34, str( round((userdata.get(z) / specific_user_num)*100, 2) ) + " %   " )    # Percent of Total
        base_coord += 1

    scr.refresh()


def write_results():
    pass



def main(scr):
    # Init curses output
    scr.clear()
    scr.addstr(0, 0, "DUO AuthType Parser v0.3")    # Version Info
    scr.addstr(3, 0, "")                            # Current Program Status
    scr.refresh()


    # Read the json file to be parsed
    scr.addstr(3, 0, "Reading JSON file...")
    scr.refresh()

    f = open("data.json", "r")
    raw_data = json.load(f)
    data = raw_data["data"]
    f.close()


    # Read the specific users file to be parsed
    scr.addstr(3, 0, "Reading Users file...")
    scr.refresh()

    f = open("users.txt", "r")
    raw_userlist = f.readlines()
    userlist = [x.strip() for x in raw_userlist]  # strip irrelevant characters
    f.close()


    # Parse the JSON logfile
    scr.addstr(3, 0, "Parsing logs...          ")
    scr.refresh()

    log_num = 0
    log_total = len(data)
    users = {}
    factors = {}    # assume 10 total factor types

    for x in data:
        log_num += 1
        auth_type = x['Factor']
        user = x['User']

        if user not in users:
            users[user] = 'n/a'

        if auth_type != 'Remembered Device':
            users[user] = auth_type
    
        # See if an auth_type is in factors and update the value, add it if not
        if auth_type in factors:
            factors[auth_type] += 1
        else:
            factors[auth_type] = 1

        output_progress(scr, log_num, log_total, users, factors)



    # Analyze User Data
    scr.addstr(3, 0, "Analyzing User Data...       ")
    scr.refresh()

    userdata = {}

    for y in users:
        auth = users[y]

        if auth not in userdata:
            userdata[auth] = 1
        else:
            userdata[auth] += 1

        output_userdata(scr, users, log_total, userdata)


    # Analyze data given a specific list of users
    scr.addstr(3, 0, "Analyzing Specific User Data...       ")
    scr.refresh()

    specific_userdata = {}
    specific_user_num = 0

    for y in users:

        if y in userlist:
            specific_user_num += 1
            auth = users[y]

            if auth not in specific_userdata:
                specific_userdata[auth] = 1
            else:
                specific_userdata[auth] += 1

            output_specific_userdata(scr, userlist, log_total, specific_userdata, specific_user_num)




    # Sleep forever!
    scr.addstr(3, 0, "Done!        Press ctrl + C to exit")
    scr.refresh()
    while True:
        pass



# Run the main program in a wrapper so curses plays nice with the terminal...
wrapper(main)

