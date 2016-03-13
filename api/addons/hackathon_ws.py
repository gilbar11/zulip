from bottle import route, run, request, abort ,error
#import bottle_redis
#import bottle.ext.redis
#from bottle import get, post, request , response # or route
import os,sys, traceback

#import cjson #sudo pip install python-cjson
#import re
#import gzip
import glob
#import ujson
import traceback
import time

#app = bottle.Bottle()
#plugin = bottle.ext.redis.RedisPlugin(host='localhost')
#app.install(plugin)
import pymysql

import zulip


# Connect to the database
connection = pymysql.connect(host='attacksimulator-prod-us.csbgmyot2qon.us-east-1.rds.amazonaws.com',
                             user='hackaton_ro',
                             password='seculert1234',
                             db='hoverfly',
                             cursorclass=pymysql.cursors.DictCursor)

zulip_client = zulip.Client(email="xjavelin-bot@zulip.com", 
                            api_key="hchm6HEGbqDi4y2v3bEJKeWgLdFbikCR", 
                            site="http://localhost:9991/",insecure=True
                            )



def error500(error):
    return error.body

    
@route('/get_user_results', method='GET')
def get_user_result():
    print request     
    #print request.body
    
    user = request.query['user']
    
    ret_res = []
    with connection.cursor() as cursor:
            # Read a single record
            sql = "select r.host,r.successPath  from RequestDetails as r join SimulationRequestHistory as s on (r.id = s.requestId) where s.requestStatus = 'ALLOW' and s.userId = '" + user + "'" 
            cursor.execute(sql)
            
            print(sql)
            print(cursor.description)

            print()

#            for row in cursor:
#                print(row)
            
            result = cursor.fetchall()
            
            print(result)
            
            for line in result:
                ret_res.append(line['host'] + line['successPath'])
    

    return {"ok":"true","res":ret_res}



@route('/start_javelin', method='GET')
def start_javlin():
    user = request.query['user']
    email = request.query['email']

    print(email)

    with connection.cursor() as cursor:
            # Read a single record
            result =[]
            
            while (len(result) == 0) or (result[0]['count'] < 12 ):
                time.sleep(20)                
                sql = "select count(distinct r.malwareId) as count from RequestDetails as r join SimulationRequestHistory as s on (r.id = s.requestId) where s.userId = '" + user + "'" 
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                
            sql = "select s.requestStatus,count(*) as count from RequestDetails as r join SimulationRequestHistory as s on (r.id = s.requestId) where s.requestStatus = 'ALLOW' and s.userId = '" + user + "' group by s.requestStatus" 
            cursor.execute(sql)
            
            print(sql)
                #print(cursor.description)

            print()

            result = cursor.fetchall()
            
            allowed = 0 
            blocked = 0 
            
            for line in result:
                if line['requestStatus'] == 'ALLOW':
                    allowed = line['count']
                if line['requestStatus'] == 'BLOCK':
                    blocked = line['count']
            # second query number of threat types

            sql = "select count(distinct r.malwareId) as count from RequestDetails as r join SimulationRequestHistory as s on (r.id = s.requestId) where s.requestStatus = 'ALLOW' and s.userId = '" + user + "'" 
            cursor.execute(sql)
            results = cursor.fetchall()
            
            maleware = results[0]['count']
            
            message = 'We got your Javelin Results: Out of 12 Maleware we check ' + str(maleware) + ' were NOT Blocked!! , you had: ' + str(allowed) + ' server allowed and ' + str(blocked) +' server blocked, list of allowed server are in '
            message += 'http://localhost:8080/get_user_results?user=' + user
            message_data = {
                "type": 'private',
                "content": message,
                "subject": 'Javelin Results: get your black list!!!',
                "to": email
            }
            print(zulip_client.send_message(message_data))
            
            return {"ok":"true","res":result}
            
@route('/update_proxy', method='GET')
def update_server():
    user = request.query['user']
    email = request.query['email']
    
    time.sleep(10)                

    message = 'Your Proxy Block list was updated!'
    message_data = {
                "type": 'private',
                "content": message,
                "subject": 'Javelin Results:Proxy Block list - Server update!',
                "to": email
            }
    print(zulip_client.send_message(message_data))
    return {"ok":"true"}




run(host='0.0.0.0', port=8080, debug=True)