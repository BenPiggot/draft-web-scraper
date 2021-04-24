import json
import app


def fetch_by_position(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    players = app.fetch_by_position('12')

    response = {
        "statusCode": 200,
        "body": json.dumps(players)
    }
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
