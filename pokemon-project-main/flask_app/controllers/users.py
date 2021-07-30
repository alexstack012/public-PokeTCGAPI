from flask_app import app
from flask import render_template, redirect, request, session, flash,jsonify
from flask_app.models.user import User
from flask_app.models.card import Collection

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask import jsonify
from flask_app import app

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

from pokemontcgsdk import RestClient

RestClient.configure('a2723f7d-9159-4abc-8021-6ec2776ce9b0')

import random
from dataclasses import dataclass
from typing import Optional


# ======================================================= #
# ==== START OF LOGIN AND REGISTRATION =========#
# ======================================================= #


# ======================================================= #
# ==== BASE =========#
# ======================================================= #

@app.route("/")
def enter():
    return render_template('enter.html')

# ======================================================= #
# ==== LOGIN =========#
# ======================================================= #
@app.route("/loginPage")
def index():
    return render_template('loginReg.html')

@app.route("/register", methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    data1 = {
        "email": request.form['email']
    }
    if User.get_by_email(data1):
        flash("Email already exsists! please use different email to register")
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    new_user_id = User.save(data)
    session["user_id"] = new_user_id
    return redirect('/dashboard')


# ======================================================= #
# ==== LOGIN =========#
# ======================================================= #


@app.route('/login', methods=['POST'])
def login():
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

# ======================================================= #
# ==== LOGOUT =========#
# ======================================================= #


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ======================================================= #
# ==== END OF LOGIN AND REGISTRATION =========#
# ======================================================= #


# ======================================================= #
# ==== DASHBOARD =========#
# ======================================================= #

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id']
    }

    sets = Set.all()
    setList=[]
    for set in sets:
        setList.append(set.id)
    oneSet=random.choice(setList)
    rareCards = Card.where(q='set.id:'+oneSet, orderBy='prices',pageSize=7,page=1)
    oneSet=random.choice(setList)
    rareCards2 = Card.where(q='set.id:'+oneSet, orderBy='prices',pageSize=7,page=1)
    logged_user = User.user_info(data)
    return render_template("index.html", user=logged_user,rareCards=rareCards,rareCards2=rareCards2)


@app.route("/card/<string:id>")
def card(id):
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id']
    }
    logged_user = User.user_info(data)

    card = Card.find(id)
    print(card)
    return render_template("card.html", user=logged_user,card=card)

    # ======================================================= #
# ==== DASHBOARD =========#
# ======================================================= #

@app.route("/collection")
def collection():
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id']
    }
    cards = User.collection_sets(data)
    # for card in collection:
    setsNames = []
    setsList=[]
    for card in cards.collection:
        print(card)
        if card.setName in setsNames:
            pass
        else:
            setsNames.append(card.setName)
            set = Set.find(card.setName)
            setsList.append(set)

    logged_user = User.user_info(data)
    return render_template("collectionSets.html", user=logged_user, sets=setsList)


# ======================================================= #
# ==== DELETE card ROUTES =========#
# ======================================================= #


@app.route("/cards/delete/<id>")
def delete_card(id):
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id']
    }
    logged_user = User.user_info(data)
    card = Card.where(q='id:' + str(id))
    data = {
        "poke_card_id" : card[0].id,
        "user_id" : session['user_id'],
    }
    Collection.remove(data)
    
    return redirect("/collection/"+card[0].set.id+"/all_cards")

@app.route("/sets")
def all_sets():
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    sets = Set.all()
    data = {
        "id": session['user_id']
    }

    logged_user = User.user_info(data)
    return render_template("sets.html", user=logged_user,sets=sets)

@app.route("/set/<string:id>/all_cards")
def allCardsInSet(id):
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#

    cards = Card.where(q='set.id:'+id)
    data = {
        "id": session['user_id']
    }
    logged_user = User.user_info(data)
    return render_template("cardsInSet.html", user=logged_user,cards=cards)

@app.route("/search", methods=["POST"])
def all_search():
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id']
    }
    cards = Card.where(q='name:' + request.form['search'])
    logged_user = User.user_info(data)
    return render_template("cardsInSet.html", user=logged_user, cards=cards)

@app.route("/addToCollection/<id>")
def add(id):
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id']
    }
    logged_user = User.user_info(data)
    card = Card.where(q='id:' + str(id))
    data = {
        "poke_card_id" : id,
        "setName" : card[0].set.id,
        "user_id" : session['user_id'],
    }
    Collection.add(data)
    
    return redirect("/collection/"+str(card[0].set.id)+"/all_cards")

@app.route("/YourCards/<id>")
def YourCardsInSet(id):
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id'],
    }
    logged_user = User.user_info(data)
    data = {
        "id": session['user_id'],
        "setName": id,
    }
    user = User.collection_cards(data)

    cardList=[]
    for cards in user.collection:
        card = Card.find(cards.poke_card_id)
        cardList.append(card)
    return render_template("collectionCards.html", user=logged_user,cards=cardList,userCards=user)

@app.route("/collection/<string:id>/all_cards")
def CollectionTable(id):
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id'],
        "setName": id,
    }
    user = User.collection_cards(data)
    for card in user.collection:
        print(card.poke_card_id)
    cards = Card.where(q='set.id:'+id)
    for card in cards:
        for collection in user.collection:
            if card.id == collection.poke_card_id:
                card.qty=collection.qty
                break
            else:
                card.qty=0
    data = {
        "id": session['user_id']
    }
    logged_user = User.user_info(data)
    return render_template("collectionTable.html", user=logged_user,cards=cards,userCards=user)

@app.route("/update/<id>", methods = {'POST'})
def update(id):
    if "user_id" not in session:
        flash("Please register / login before you can proced to the website")
        return redirect("/")
    # the if condition above can ONLY go in render routes. NOT REDIRECT ROUTES.#
    data = {
        "id": session['user_id']
    }
    logged_user = User.user_info(data)
    data = {
        "poke_card_id" : id,
        'qty':request.form[id],
        "user_id" : session['user_id'],
    }
    card = Card.find(id)
    Collection.update(data)
    print(card)
    
    return redirect("/collection/"+str(card.set.id)+"/all_cards")