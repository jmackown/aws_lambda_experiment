import json
import random
import datetime
import boto3
import uuid


fleet = [
    {"Name": "Bucephalus", "Color": "Golden", "Gender": "Male",},
    {"Name": "Shadowfax", "Color": "White", "Gender": "Male",},
    {"Name": "Rocinante", "Color": "Yellow", "Gender": "Female",},
]



def set_db_connection():
    dynamodb = boto3.resource("dynamodb")

    return dynamodb

def generate_ride_id():
    rideid = str(uuid.uuid1())

    return rideid


def lambda_handler(event, context):

    rideid = generate_ride_id()

    username = ""

    request_body = json.loads(event["body"])
    pickup_location = request_body["PickupLocation"]
    unicorn = find_unicorn(pickuplocation=pickup_location)

    record_ride(rideid=rideid, username=username, unicorn=unicorn)

    return {
        "statusCode": 201,
        "body": json.dumps(
            {
                "RideId": rideid,
                "Unicorn": unicorn,
                "UnicornName": unicorn["Name"],
                "Eta": "30 seconds",
                "Rider": username,
            }
        ),
    }


def find_unicorn(pickuplocation: dict):
    print(
        f'Finding unicorn for {pickuplocation["Latitude"]}, {pickuplocation["Longitude"]}'
    )

    return fleet[0]


def record_ride(rideid: str, username: str, unicorn: dict):
    dynamodb = set_db_connection()
    table = dynamodb.Table("Rides")
    table.put_item(
        Item={
            "RideId": rideid,
            "User": username,
            "Unicorn": unicorn,
            "UnicornName": unicorn["Name"],
            "RequestTime": datetime.datetime.now().isoformat(),
        }
    )
