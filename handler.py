import json
import app


def fetch_by_position(event, context):
    """ fetch all players drafted at a given mock draft position """
    players = app.fetch_by_position(str(event['pathParameters']['draft_position']))

    response = {
        "statusCode": 200   ,
        "body": json.dumps(players)
    }
    return response
