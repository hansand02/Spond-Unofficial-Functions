import asyncio
import argparse
import csv
import os
from datetime import date
from spond import spond
from config import username, password
from enum import Enum
from collections import defaultdict
from person import Person
from dateutil.relativedelta import relativedelta

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

# Standard fra dato er 2 måneder tilbage
parser.add_argument(
    "-f",
    "--from",
    help="First date to query for. Date is included in results (format YYYY-MM-DD)",
    type=date.fromisoformat,
    dest="f",
    default= date.today() - relativedelta(months=2)
)   

# Standard til dato er i dag 
parser.add_argument(
    "-t",
    "--to",
    help="Last date to query for. Date is excluded from results (format YYYY-MM-DD)",
    type=date.fromisoformat,
    dest="t",
    default=date.today() + relativedelta(months=1)
)

parser.add_argument(
    "-n",
    "--names",
    help="Only include these names.",
    type=lambda s: [name.strip().title() for name in s.split(",")],
    default=[None],
    dest="n",
)

args = parser.parse_args()


async def totalAttendance():
    
    s = spond.Spond(username=username, password=password)
    events = await s.get_events(min_start=args.f, max_end=args.t)

    foldername = "./exports/totalAttendance"

    if not os.path.exists(foldername):
        os.makedirs(foldername)


    # create a dict of all members, find members from events. 
    
    
    people = defaultdict(list)

    for e in events:
            
            for r in e["responses"]["acceptedIds"]:
                await addAttendesToDict(spondObject=s, personID=r, theDict=people, response_type=ResponseTypes.ACCEPTED.value)

            for r in e["responses"]["declinedIds"]:
                await addAttendesToDict(spondObject=s, personID=r, theDict=people, response_type=ResponseTypes.DECLINED.value)

            for r in e["responses"]["unansweredIds"]:
                await addAttendesToDict(spondObject=s, personID=r, theDict=people, response_type=ResponseTypes.UNANSWERED.value)

            for r in e["responses"]["waitinglistIds"]:
                await addAttendesToDict(spondObject=s, personID=r, theDict=people, response_type=ResponseTypes.WAITINGLIST.value)

            for r in e["responses"]["unconfirmedIds"]:
                await addAttendesToDict(spondObject=s, personID=r, theDict=people, response_type=ResponseTypes.UNCONFIRMED.value)


    filename = os.path.join(
    foldername, f"{args.f} -> {args.t}.csv"
    )
    with open(filename, "w", newline="") as csvfile:
        
        spamwriter = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        spamwriter.writerow(
            ["Start", "End", "Name", "Accepted", "Declined", "Unanswered", "Unconfirmed", "Waitinglist"]
        ) 
        sorted_people = sorted(people.values(), key=lambda x: x[0].accepted, reverse=True)

        for person in sorted_people:   
            spamwriter.writerow(
                [
                    person[0].name,
                    f"{args.f} til {args.t}",
                    person[0].accepted,
                    person[0].declined,
                    person[0].unanswered,
                    person[0].unconfirmed,
                    person[0].waitinglist
                ]
            )
    await s.clientsession.close()

         
async def addAttendesToDict(spondObject, personID, theDict, response_type):
    person = await spondObject.get_person(personID)
    if personID not in theDict:
        pObjekt = Person(person["firstName"] + " " + person["lastName"])
        theDict[personID] = ([pObjekt])  # Fix: Pass the Person object as an iterable containing a single element
    
    if response_type == ResponseTypes.ACCEPTED.value:
        theDict[personID][0].accepted += 1
    elif response_type == ResponseTypes.DECLINED.value:
        theDict[personID][0].declined += 1
    elif response_type == ResponseTypes.UNANSWERED.value:
        theDict[personID][0].unanswered += 1
    elif response_type == ResponseTypes.UNCONFIRMED.value:
        theDict[personID][0].unconfirmed += 1
    elif response_type == ResponseTypes.WAITINGLIST.value:
        theDict[personID][0].waitinglist += 1
                    





async def calculateAttendance(response_type):
    """ Process the respondent, can have different types: accepted, declined, unanswered, unconfirmed, waitinglist """

    acceptedResponses  = [response.value for response in ResponseTypes]

    if response_type.lower() not in acceptedResponses:
        raise ValueError("Invalid response_type: " + response_type + ", must be one of: " + ", ".join(acceptedResponses))


if __name__ == "__main__":
    asyncio.run(totalAttendance())
