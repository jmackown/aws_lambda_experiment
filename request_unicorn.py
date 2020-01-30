import json
import datetime
import logging
import logging.config

import boto3
import uuid


fleet = [
    {"Name": "Bucephalus", "Color": "Golden", "Gender": "Male",},
    {"Name": "Shadowfax", "Color": "White", "Gender": "Male",},
    {"Name": "Rocinante", "Color": "Yellow", "Gender": "Female",},
]

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.ERROR)
logger = logging.getLogger(__name__)


def lambda_handler(event, context):

    rideid = generate_ride_id()

    username = "the_username"

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
    logger.info(
        f'Finding unicorn for {pickuplocation["Latitude"]}, '
        f'{pickuplocation["Longitude"]}'
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


def set_db_connection():

    dynamodb = boto3.resource("dynamodb")

    return dynamodb


def generate_ride_id():

    rideid = str(uuid.uuid1())

    return rideid
