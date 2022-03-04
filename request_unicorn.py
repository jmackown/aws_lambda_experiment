import json
import datetime
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


def lambda_handler(event: dict) -> dict:

    rideid: str = generate_ride_id()
    username: str = "the_username"
    request_body: dict = json.loads(event["body"])
    pickup_location: dict = request_body["PickupLocation"]
    unicorn: dict = find_unicorn(pickuplocation=pickup_location)

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


def find_unicorn(pickuplocation: dict) -> dict:
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

    return boto3.resource("dynamodb")


def generate_ride_id():

    return str(uuid.uuid1())
