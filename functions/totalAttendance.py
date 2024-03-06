import asyncio
import argparse
import csv
import os
from datetime import date
from spond import spond
from config.config import username, password
from enum import Enum
from responseTypes import ResponseTypes


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

    foldername = "./exports"

    if not os.path.exists(foldername):
        os.makedirs(foldername)


    # create a dict of all members, find members from events. 
    people = {}
    await calculateAttendance("accepted")



async def calculateAttendance(response_type):
    """ Process the respondent, can have different types: accepted, declined, unanswered, unconfirmed, waitinglist """

    print(list(ResponseTypes), " liste ja")

    if response_type.lower() not in list(ResponseTypes):
        raise ValueError("Invalid response_type: " + response_type + ", must be one of: " + ", ".join(response_type))


if __name__ == "__main__":
    asyncio.run(totalAttendance())
