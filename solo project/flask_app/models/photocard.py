from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Photocards:
    db = "pc_trading_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.member = data['member']
        self.artist = data['artist']
        self.album_version = data['album_version']
        self.details = data['details']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #staticmethod for validating pc
    @staticmethod
    def validate_pc(data):
        is_valid = True
        if len(data["member"].strip()) == 0: 
            flash("*Must include the name of the member(s) on the card.")
            is_valid = False
        if len(data["artist"].strip()) == 0: 
            flash("*Must include the name of the artist or soloist the card is from.")
            is_valid = False
        if len(data["album_version"].strip()) == 0: 
            flash("*Must include the album title and version the card was pulled from.")
            is_valid = False
        if len(data["details"].strip()) == 0: 
            flash("*Must include relevant details about the photocard i.e. condition, things of interest, etc.")
            is_valid = False
        return is_valid

    #classmethod for adding new pc
    @classmethod
    def save_new_pc(cls, data):
        query = """INSERT INTO photocards (user_id, member, artist, album_version, details, created_at)
                VALUES (%(user_id)s, %(member)s, %(artist)s, %(album_version)s, %(details)s, NOW());"""
        return connectToMySQL(cls.db).query_db(query, data)

    #classmethod for updating pc
    @classmethod
    def update_pc(cls, data):
        query = """UPDATE photocards
                SET member=%(member)s, artist=%(artist)s, album_version=%(album_version)s,
                details=%(details)s, updated_at=NOW()
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,data)

    #classmethod for deleting pc
    @classmethod
    def delete_pc(cls, id):
        query  = "DELETE FROM photocards WHERE id = %(id)s;"
        data = {"id":id}
        return connectToMySQL(cls.db).query_db(query, data)

    #classmethod for displaying all pcs
    @classmethod
    def get_all_photocards_with_users(cls):
        query = """SELECT * FROM photocards
                JOIN users on photocards.user_id = users.id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_photocards = []
        for row in results:
            one_photocard = cls(row)
            one_photocards_author_info = {
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            author = user.Users(one_photocards_author_info)
            one_photocard.creator = author
            all_photocards.append(one_photocard)
        return all_photocards

    #classmethod for displaying one pc
    @classmethod
    def get_one_photocard_with_user(cls, id):
        query  = """SELECT * FROM photocards
                JOIN users on photocards.user_id = users.id
                WHERE photocards.id = %(id)s;"""
        data = {'id': id}
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) == 0:
            return None
        
        photocard = Photocards(results[0])
        user_data = {
            "id": results[0]['users.id'], 
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }
        photocard.user = user.Users(user_data)
        return photocard
