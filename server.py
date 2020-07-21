#!/usr/bin/env python3
#importing all the libraries
import os
import bcast
import socket
import random
import sqlite3
import multiprocessing


# database settings
database =os.path.join(os.path.dirname(os.path.abspath(__file__)),"vehicle_record.db")

# this is a simple socket connection function
def vehicle_connect(IP,data):
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as SOCKET:
        SOCKET.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        SOCKET.sendto(data,(IP,9091)) # the port for send the platoon is 9091
        #SOCKET.shutdown()
        SOCKET.close()

# this function will start to listen to the broadcast and put the vehicles in the database
def listner():
    try:
        connection = sqlite3.connect(database[0])
    except Exception as e:
        print(e)
    finally:
        if connection: 
            with bcast.BroadCastReceiver() as Receiver:
                for data,address in Receiver:
                    if "leader" in data.decode():
                        # this will add the vehicle ID as the platoon leader inside the db
                        print("The Leader is "+data.decode().split(":")[0])
                        cur=connection.cursor()
                        query="""INSERT INTO leader VALUES(?,?)"""
                        cur.execute(query,(data.decode().split(":")[0],data.decode().split('|')[-1]))
                        connection.commit()
                        cur.close()
                    else:
                        # this will register the Vehicle ID to form platoon
                        cur=connection.cursor()
                        query="""INSERT INTO Vehicle VALUES(?,?)"""
                        cur.execute(query,(data.decode(),address[0]))
                        connection.commit()
                        cur.close()

# this function will set the platoon and send the vehicles their peers...
def platooning():
    try:
        connection = sqlite3.connect(database[0])
    except Exception as e:
        print(e)
    finally:
        cur = connection.cursor()
        query="""SELECT * FROM Vehicle LIMIT 5"""
        cur.execute(query)
        rows=cur.fetchall()
        if len(rows)==5: # this is to ensure that the number of vehicles returned are exactly 5  
            random.shuffle(rows)
            temp=list()
            for row in rows:
                temp.append(":".join(row))
            platoon="|".join(temp).encode()
            for row in rows:
                vehicle_connect(row[1],platoon)
            # making space for new 5 vehicles 
            cur=connection.cursor()
            query="""DELETE * FROM Vehicle"""
            cur.execute(query)
            connection.commit()
            cur.close()
        
    

if __name__=="__main__":
    
    ListnerProcess = multiprocessing.Process(target=listner)
    ListnerProcess.start()
    
    while True:
        platooning()

    ListnerProcess.join()
