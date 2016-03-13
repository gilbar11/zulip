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
import random 

# Connect to the database

zulip_client = zulip.Client(email="xjavelin-bot@zulip.com", 
                            api_key="hchm6HEGbqDi4y2v3bEJKeWgLdFbikCR", 
                            site="http://localhost:9991/",insecure=True
                            )
random.seed(1)


def error500(error):
    return error.body

    
@route('/get_user_results', method='GET')
def get_user_result():
    print request     
    #print request.body

    connection = pymysql.connect(host='attacksimulator-prod-us.csbgmyot2qon.us-east-1.rds.amazonaws.com',
                             user='hackaton_ro',
                             password='seculert1234',
                             db='hoverfly',
                             cursorclass=pymysql.cursors.DictCursor)
    
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
    
    connection.close()
    return {"crime_server":ret_res}

@route('/subscribe_to_javelin_agent', method='GET')
def start_javlin():
    user = request.query['user']
    email = request.query['email']

    print(email)

    message = 'You Sucessfully Subscribed to Javelin Agent!'
    message_data = {
        "type": 'private',
        "content": message,
        "subject": 'Javelin Agent Subscription',
        "to": email
    }
    print(zulip_client.send_message(message_data))



            # Read a single record
    
    connection = pymysql.connect(host='attacksimulator-prod-us.csbgmyot2qon.us-east-1.rds.amazonaws.com',
                             user='hackaton_ro',
                             password='seculert1234',
                             db='hoverfly',
                             cursorclass=pymysql.cursors.DictCursor)
    
    
    result =[]        
    time.sleep(20)
    with connection.cursor() as cursor:
                
        sql = "select s.requestStatus,count(*) as count from RequestDetails as r join SimulationRequestHistory as s on (r.id = s.requestId) where s.requestStatus = 'ALLOW' and s.userId = '" + user + "' group by s.requestStatus" 
        cursor.execute(sql)
            
        print(sql)
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
            "subject": 'Javelin Agent Results: get your updated black list!!!',
            "to": email
        }
        print(zulip_client.send_message(message_data))
        connection.close()
        return {"ok":"true","res":result}



@route('/start_javelin', method='GET')
def start_javlin():
    user = request.query['user']
    email = request.query['email']

    print(email)

            # Read a single record
    
    connection = pymysql.connect(host='attacksimulator-prod-us.csbgmyot2qon.us-east-1.rds.amazonaws.com',
                             user='hackaton_ro',
                             password='seculert1234',
                             db='hoverfly',
                             cursorclass=pymysql.cursors.DictCursor)
    
    
    result =[]        
    while (len(result) == 0) or (result[0]['count'] < 12 ):
        result =[]
        with connection.cursor() as cursor:
            time.sleep(10)        
            irand = random.randint(1,1000000000)
                    
            sql = "select count(distinct r.malwareId) as count from RequestDetails as r join SimulationRequestHistory as s on (r.id = s.requestId) where s.userId = '" + user + "' and " +   str(irand) + " = "  + str(irand)
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            cursor.close()
        connection.close()
        connection = pymysql.connect(host='attacksimulator-prod-us.csbgmyot2qon.us-east-1.rds.amazonaws.com',
                                     user='hackaton_ro',
                                     password='seculert1234',
                                     db='hoverfly',
                                     cursorclass=pymysql.cursors.DictCursor)
            
            

    time.sleep(20)
    with connection.cursor() as cursor:
                
        sql = "select s.requestStatus,count(*) as count from RequestDetails as r join SimulationRequestHistory as s on (r.id = s.requestId) where s.requestStatus = 'ALLOW' and s.userId = '" + user + "' group by s.requestStatus" 
        cursor.execute(sql)
            
        print(sql)
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
        connection.close()
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