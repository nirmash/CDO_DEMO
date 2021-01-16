import json
import requests
import datetime
import os
import urllib.parse
#import redis

# def connect_redis_direct(redis_direct_port, redis_direct_url):
#     global connection_mode
#     global r_direct_port
#     global r_direct_url

#     r_direct_port = redis_direct_port
#     r_direct_url = redis_direct_url

#     connection_mode = "redis_direct"

# def get_redis_connection():
#     return redis.Redis(host=r_direct_url, port=r_direct_port, db=0)

def start_timer():

    global start_time_value
    start_time_value = datetime.datetime.now()

def end_timer():
    delta = datetime.datetime.now() - start_time_value
    return (delta.microseconds / 1000)

def execute_command(cmd, returnType = 'string'):
    # if connection_mode == "redis_direct":
    #     rd = get_redis_connection()
    #     return rd.execute_command(cmd)
    # else:
    API_ENDPOINT = "http://localhost:2772/"
    start_timer()
    r = requests.post(url = API_ENDPOINT, data = cmd)
    print("Response {0}, time: {1}".format(r.text,end_timer()))
    return parse_response(r.text, returnType)

def GetToDoUsers():
    return SMembers("Todo_Users")

def AddNewTask (user, task, done):
    content = bytes(task,'utf-8')
    encoded = base64.b64encode(content)
    encoded_task = str(encoded,'utf-8')
    print(encoded_task)
    newTask = {
        "user":user,
        "task":encoded_task,
        "id":int(datetime.datetime.now().strftime("%Y%m%d%H%M%S%z")),
        "done":done
    }
    sTask = json.dumps(newTask).replace(" ","")
    execute_command("SADD Tasks_{0} {1}".format(user,sTask))

def Incr(key):
    return execute_command("incr {0}".format(key))
def Set (key, value):
    return execute_command("set {0} {1}".format(key,urllib.parse.quote_plus(value)))

def Exists (key):
    return execute_command("exists {0}".format(key))
def Get (key):
    return execute_command("get {0}".format(key))

def Del (key):
    return execute_command("del {0}".format(key))

def HSet (key, fld, value):
    return execute_command("hset {0} {1} {2}".format(key,fld,urllib.parse.quote_plus(value)))

def HGet (key, field):
    return execute_command("hget {0} {1}".format(key,field))

def HGetAll (key):
    return execute_command("hgetall {0}".format(key),'dict')

def HKeys (key):
    return execute_command("hkeys {0}".format(key),'array')

def HDell (key, field):
    return execute_command("hdell {0} {1}".format(key,field))

def RPush (key, value):
    return execute_command("rpush {0} {1}".format(key, urllib.parse.quote_plus(value)))

def LLen (key):
    return execute_command("llen {0}".format(key))

def LRange (key, min, max):
    return execute_command("lrange {0} {1} {2}".format(key, min, max),'array')

def SAdd (key, value):
    return execute_command("sadd {0} {1}".format(key, urllib.parse.quote_plus(value)))

def SMembers (key):
    return execute_command("smembers {0}".format(key),'array')

def SIsmember (key, value):
    return execute_command("sismember {0} {1}".format(key, value))

def SRem (key, value):
    return execute_command("srem {0} {1}".format(key, value))

def Keys(pattern):
    return execute_command("keys {0}".format(pattern),'array')

def parse_response(txt, responseType ,show_latency = False):
    retArr = json.loads(txt[8:])['data']['getRedis']
    arrLen=len(retArr)
    latency=retArr[arrLen-1]
    retVals = retArr[0:(arrLen-1)]
    if responseType == 'string':
        if retVals[0] == "":
            retVal = "empty"
        else:
            retVal = urllib.parse.unquote_plus(str(retVals[0]))
    if responseType == 'array':
        retVal = []
        for val in retVals:
            retVal.append(urllib.parse.unquote_plus(str(val)))
        retVal = retVals
    if responseType == 'dict':
        retVal = {}
        for ii in range(0,len(retVals)-1,2):
            retVal[retVals[ii]]=retVals[ii+1]
    
    if show_latency == True:
        return { 
            "latency" : latency,
            "data" : retVal
        }
    else:
        return retVal
