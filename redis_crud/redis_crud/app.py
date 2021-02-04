import json
import redis_proxy as r
import os

def lambda_handler(event, context):
    try:
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
                "message": "Redis update count-{0} CRUD count for {1}-{2}".format(r.Get("key_count"),redis_key, r.Get("crud_count_{0}".format(redis_key))),
            }),
        }
    except:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "missing post body",
            }),
        }        