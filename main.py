from requests import get
from dataclasses import dataclass
from pprint import pprint
base_url = "https://slc.ctld.ntust.edu.tw/rest/council/common/bookings/pager"

@dataclass
class User:
    uuid: str
    name: str
    user_id: str

@dataclass
class Book_Info:
    place: str
    creator: User
    create_date: str
    Participants: list[User]
    booking_end_date: str
    booking_start_date: str

def parse_user_data(data:dict) -> User:
    if 'participantName' in data:
        user_name:str = data['participantName']
        user_id:str = data['participantAccount']
        user_uuid:str = data['pid']
    else:
        user_name:str = data['creatorName']
        user_id:str = data['hostAccount']
        user_uuid:str = data['creatorId']
    return User(user_uuid, user_name, user_id)


def parse_book_data(data:dict):
    creator:User = parse_user_data(data)
    Participants:list[User] = []
    for Participant in data['bookingParticipants']:
        Participants.append(parse_user_data(Participant))
    create_date:str = data['createDate']
    booking_end_date:str = data['bookingEndDate']
    booking_start_date:str = data['bookingStartDate']
    resource = data['mainResourceName']
    return Book_Info(resource,creator, create_date, Participants, booking_end_date, booking_start_date)

response = get(base_url)
jdata = response.json()
results = jdata['resultList']
print(len(results))
print(jdata['totalCount'])
print(jdata['sortColumnName'])


for result in results:
    pprint(parse_book_data(result))
    print('----------------------------------')
