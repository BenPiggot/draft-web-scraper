import json
import app


def fetch_by_position(event, context):
    """ fetch all players drafted at a given mock draft position """
    print(event)
    players = app.fetch_by_position(str(event['path']['draft_position']))

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": players
    }
    return response
