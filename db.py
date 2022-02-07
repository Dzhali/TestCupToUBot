# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 13:34:24 2022

@author: Liana
"""

import sqlite3

class ClientDatabase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchall()
            return bool(len(result))
    
    def add_user(self, user_id, state):
        with self.connection:
            self.cursor.execute("INSERT INTO 'users' (user_id, state) VALUES (?)", (user_id, state))
        
    def set_state(self, user_id, state):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'state' = ? WHERE 'user_id' = ?", (state, user_id))