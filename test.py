import asyncio
import argparse
import asyncio
import csv
import os
from datetime import date
from spond import spond
from config import username, password
from datetime import datetime
from person import Person

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
    help="Only include these names. Cap sensitive",
    type=lambda s: [name.strip().title() for name in s.split(",")],
    default=[None],
    dest="n",
)

parser.add_argument(
    "-a", help="Also include all members", default=True, action="store_true"
)

args = parser.parse_args()


async def main():
    
    s = spond.Spond(username=username, password=password)
    events = await s.get_events( )

    foldername = "./exports"

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
                ["Start", "End", "Description", "Name", "Answer", "Organizer"]
            )



            for o in e["owners"]:
                person = await s.get_person(o["id"])
                full_name = person["firstName"] + " " + person["lastName"]
                spamwriter.writerow(
                    [
                        e["startTimestamp"],
                        e["endTimestamp"],
                        e["heading"],
                        full_name,
                        o["response"],
                        "X",
                    ]
                )

            if args.a is True:
                    for r in e["responses"]["acceptedIds"]:
                        await processRespondent(s, spamwriter, respondent=r, event=e, response_type="accepted")

                    for r in e["responses"]["declinedIds"]:
                        await processRespondent(s, spamwriter, respondent=r, event=e, response_type="declined")

                    for r in e["responses"]["unansweredIds"]:
                        await processRespondent(s, spamwriter, respondent=r, event=e, response_type="unanswered")

                    for r in e["responses"]["waitinglistIds"]:
                        await processRespondent(s, spamwriter, respondent=r, event=e, response_type="waitinglist")

                    for r in e["responses"]["unconfirmedIds"]:
                        await processRespondent(s, spamwriter, respondent=r, event=e, response_type="unconfirmed")

                        
            await s.clientsession.close()


async def processRespondent(s: spond.Spond, spamwriter, respondent, event, response_type:str):
    """ Process the respondent, can have different types: accepted, declined, unanswered, unconfirmed, waitinglist """
    
    response_types = ["accepted", "declined", "unanswered", "unconfirmed", "waitinglist"]

    if response_type.lower() not in response_types:
        raise ValueError("Invalid response_type: " + response_type + ", must be one of: " + ", ".join(response_types))


    person = await s.get_person(respondent)
    full_name = person["firstName"] + " " + person["lastName"]

    spamwriter.writerow(
        [
            event["startTimestamp"],
            event["endTimestamp"],
            event["heading"],
            full_name,
            response_type,
        ]
    )

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
asyncio.run(main())

