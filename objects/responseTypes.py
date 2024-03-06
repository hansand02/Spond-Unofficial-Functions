from enum import Enum

class ResponseTypes(Enum):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    UNANSWERED = "unanswered"
    UNCONFIRMED = "unconfirmed"
    WAITINGLIST = "waitinglist"
    