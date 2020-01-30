import uuid
from unittest import mock

import boto3

import request_unicorn


class TestLambda:
    def setup(self):
        self.request_event = {
            "path": "/ride",
            "httpMethod": "POST",
            "headers": {
                "Accept": "*/*",
                "Authorization": "eyJraWQiOiJLTzRVMWZs",
                "content-type": "application/json; charset=UTF-8",
            },
            "queryStringParameters": None,
            "pathParameters": None,
            "requestContext": {
                "authorizer": {"claims": {"cognito:username": "the_username"}}
            },
            "body": '{"PickupLocation":{"Latitude":47.6174755835663,'
            '"Longitude":-122.28837066650185}}',
        }
        self.request_result = {
            "statusCode": 201,
            "body": '{"RideId": "df192410-433f-11ea-a0c7-6c40089d22de", '
            '"Unicorn": {"Name": "Bucephalus", "Color": "Golden", '
            '"Gender": "Male"}, "UnicornName": "Bucephalus", '
            '"Eta": "30 seconds", "Rider": ""}',
        }

    def local_db_connection(self):
        dynamodb = boto3.resource(
            "dynamodb", region_name="us-west-2", endpoint_url="http://localhost:8000"
        )

        return dynamodb

    def random_ride_id(self):
        rideid = str(uuid.uuid1())

        return rideid

    @mock.patch("request_unicorn.set_db_connection")
    @mock.patch("request_unicorn.generate_ride_id")
    def test_lambda_handler(self, mock_generate_ride_id, mock_set_db_connection):
        mock_generate_ride_id.return_value = "df192410-433f-11ea-a0c7-6c40089d22de"
        mock_set_db_connection.get.side_effect = self.local_db_connection()
        result = request_unicorn.lambda_handler(event=self.request_event, context=None)

        assert result == self.request_result
