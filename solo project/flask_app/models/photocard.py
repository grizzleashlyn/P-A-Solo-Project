from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from datetime import datetime

class Photocards:
    db = "pc_trading_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.member = data['member']
        self.group = data['group']
        self.album_version = data['album_version']
        self.details = data['details']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #staticmethod for validating pc

    #classmethod for adding new pc

    #classmethod for updating pc

    #classmethod for deleting pc

    #classmethod for displaying all pcs

    #classmethod for displaying one pc
