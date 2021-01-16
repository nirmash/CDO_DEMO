import json
import redis_proxy as r
import os
# import requests


def lambda_handler(event, context):

    print("event is: {0}".format(json.dumps(event)))
    if type(event['body']) == str:
        body = json.loads(event['body'])
    else:
        body = event['body']

    redis_key = body['key']
    redis_value = body['value']

    r.Set(redis_key,redis_value)
    r.Incr("key_count")
    r.Incr("crud_count_{0}".format(redis_key))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "CRUD count - {0} CRUD count for {1} - {2}".format(r.Get("key_count"),redis_key, r.Get("crud_count_{0}".format(redis_key))),
        }),
    }
