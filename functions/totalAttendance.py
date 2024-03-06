import asyncio
import argparse
import csv
import os
from datetime import date
from spond import spond
from config import username, password
from enum import Enum


class ResponseTypes(Enum):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    UNANSWERED = "unanswered"
    UNCONFIRMED = "unconfirmed"
    WAITINGLIST = "waitinglist"

parser = argparse.ArgumentParser(
    description="Creates an attendance.csv for organizers of events."
)
# ... rest of the code ...


parser = argparse.ArgumentParser(
    description="Creates an attendance.csv for organizers of events."
)

parser.add_argument(
    "-f",
    "--from",
    help="First date to query for. Date is included in results (format YYYY-MM-DD)",
    type=date.fromisoformat,
    dest="f",
)   

parser.add_argument(
    "-t",
    "--to",
    help="Last date to query for. Date is excluded from results (format YYYY-MM-DD)",
    type=date.fromisoformat,
    dest="t",
)

parser.add_argument(
    "-n",
    "--names",
    help="Only include these names.",
    type=lambda s: [name.strip().title() for name in s.split(",")],
    default=[None],
    dest="n",
)


async def totalAttendance():
    
    s = spond.Spond(username=username, password=password)
    events = await s.get_events( )

    foldername = "../exports/totalAttendance"

    if not os.path.exists(foldername):
        os.makedirs(foldername)


    # create a dict of all members, find members from events. 
    people = {}

    for e in events:
        filename = os.path.join(
            foldername, f"{e['startTimestamp']}-{e['heading']}.csv"
        )
        with open(filename, "w", newline="") as csvfile:
            
            spamwriter = csv.writer(
                csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            spamwriter.writerow(
                ["Start", "End", "Name", "Accepted", "Declined", "Unanswered", "Unconfirmed", "Waitinglist"]
            )

            




    await s.clientsession.close()




async def calculateAttendance(response_type):
    """ Process the respondent, can have different types: accepted, declined, unanswered, unconfirmed, waitinglist """

    acceptedResponses  = [response.value for response in ResponseTypes]

    if response_type.lower() not in acceptedResponses:
        raise ValueError("Invalid response_type: " + response_type + ", must be one of: " + ", ".join(acceptedResponses))


if __name__ == "__main__":
    asyncio.run(totalAttendance())
