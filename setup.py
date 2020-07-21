#!/usr/bin/env python3
import sqlite3,os

database =os.path.join(os.path.dirname(os.path.abspath(__file__)),"vehicle_record.db")
connection = sqlite3.connect(database)
query="""CREATE TABLE IF NOT EXISTS Vehicle (ID TEXT PRIMARY KEY, address TEXT)"""
cur=connection.cursor()
cur.execute(query)
query="""CREATE TABLE IF NOT EXISTS leader (ID TEXT PRIMARY KEY, ExecutionTime TEXT, FOREIGN KEY (ID) REFERENCES vehicle(ID))"""
cur.execute(query)
connection.commit()
