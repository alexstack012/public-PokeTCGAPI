import re
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash



from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Collection:
    def __init__(self, data):
        self.id = data['id']
        self.poke_card_id = data['poke_card_id']
        self.qty = data['qty']
        self.setName = data['setName']
        self.user_id = data['user_id']

    @classmethod
    def add(cls, data):
        query = "INSERT INTO cards (poke_card_id,setName, user_id) VALUES (%(poke_card_id)s, %(setName)s, %(user_id)s);"
        return connectToMySQL("pokemontcg").query_db(query, data)
    @classmethod
    def remove(cls, data):
        query = "delete from cards where user_id = %(user_id)s and poke_card_id = %(poke_card_id)s;"
        return connectToMySQL("pokemontcg").query_db(query, data)
    @classmethod
    def update(cls, data):
        query = "update pokemontcg.cards set qty = %(qty)s where user_id = %(user_id)s and poke_card_id = %(poke_card_id)s;"
        return connectToMySQL("pokemontcg").query_db(query, data)