import boto3
from boto3.dynamodb.conditions import Key

def fetch_by_position(position: str):
    """ fetch all players drafted at a given mock draft position """
    dynamodb_client = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb_client.Table('nfl-mock-drafts-2021')

    response = table.query(
        KeyConditionExpression=Key('position').eq(position)
    )

    print(response['Items'])
    return response['Items']