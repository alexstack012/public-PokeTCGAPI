import re
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.card import Collection
from flask import flash


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.collection = []

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("must be more than 2 characters")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("must be more than 2 characters")
            is_valid = False
        if len(data['password']) < 8:
            flash("must be more than 8 characters")
            is_valid = False
        if data['password'] != data['conf_pass']:
            flash('passwords must match')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("email must be valid")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("pokemontcg").query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("pokemontcg").query_db(query, data)

    @classmethod
    def user_info(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("pokemontcg").query_db(query, data)
        return cls(results[0])

    @classmethod
    def collection_sets(cls, data):
        query = 'select * from users join cards on users.id = cards.user_id where users.id = %(id)s;'
        results = connectToMySQL('pokemontcg').query_db(query, data)
        print(results)
        user = cls(results[0])

        for card in results:
            card_data = {
                'id': card['cards.id'],
                'poke_card_id': card['poke_card_id'],
                'qty': card['qty'],
                'setName': card['setName'],
                'user_id': card['user_id'],
            }

            user.collection.append(Collection(card_data))
        return user

    @classmethod
    def collection_cards(cls, data):
        query = 'select * from users join cards on users.id = cards.user_id where users.id = %(id)s and cards.setName=%(setName)s;'
        results = connectToMySQL('pokemontcg').query_db(query, data)
        print(results)
        user = cls(results[0])

        for card in results:
            card_data = {
                'id': card['cards.id'],
                'poke_card_id': card['poke_card_id'],
                'qty': card['qty'],
                'setName': card['setName'],
                'user_id': card['user_id'],
            }

            user.collection.append(Collection(card_data))
        return user
