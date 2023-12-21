from flask import make_response, jsonify, request, session
from flask import Flask
from flask_migrate import Migrate
from models import Friends, User
from config import app, db
from middleware import authorization_required
import bcrypt
from datetime import date




# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hydrohomie.db"
# migrate = Migrate(app, db)
# db.init_app(app)


@app.get('/')
def hello():
    return "Hello, world"
    

@app.get('/api/date')
def get_date():
    today = date.today()
    formatted_date = date.isoformat(today)
    return {"Today" : formatted_date}

@app.get('/api/completed')
def get_completed():
    pass

# @app.get('/api/users/<int:user_id>/completed')
# def get_completed(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return make_response(jsonify({'ERROR': 'USER NOT FOUND'}), 404)
#     data = user.completed_days
#     return make_response(jsonify(data), 200)

@app.get('/api/users')
def get_users():
    users = User.query.all()
    data = [user.to_dict() for user in users]
    return make_response(data), 200

@app.get('/api/users/<int:user_id>')
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'ERROR': 'USER NOT FOUND'}), 404)
    data = user.to_dict()
    return make_response(jsonify(data), 200)

@app.get('/api/users/<int:user_id>/completed')
def get_completed_days(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'ERROR': 'USER NOT FOUND'}), 404)
    data = user.completed_days
    return make_response(jsonify(data), 200)

# PATCH Route to update mob's info in database
# @app.route("/mobs/<int:mob_id>", methods=["PATCH"])
# def update_mob_by_id(mob_id: int):
#     # GET my mob in database that matches the right id.
#     matching_mob = Mob.query.filter(Mob.mob_id == mob_id).first()
#     try:
#         payload = request.json
#         # Set each mathcing mob's attribute to the right value
#         for key in payload:
#         #   If a specific key-value chnage was requested, update that key
#         #   Otherwise leave it as the old value
#             setattr(matching_mob, key, payload[key])
#         # Add and Commit changes to database
#         db.session.add(matching_mob)
#         db.session.commit()
#         #Either return the changed mob or return an error
#         return make_response(jsonify(matching_mob.to_dict()), 200)
#     except:
#         return make_response(jsonify({"ERROR": "PATCH failed. Seek help."}))

@app.patch('/api/users/<int:user_id>')
def update_watercount(user_id: int):
    user = User.query.filter(User.id == user_id).first()
    try:
        payload = request.json
        print(payload)
        for key in payload:
            setattr(user, key, payload[key])

        db.session.add(user)
        db.session.commit()

        return make_response(jsonify(user.to_dict()), 200)
    except:
        return make_response(jsonify({"ERROR": "PATCH FAILED"}))

@app.get('/api/userData')
@authorization_required
def get_userData(current_user):
    userData = User.query.get(current_user["id"])
    return make_response(jsonify(userData.to_dict()), 200)


@app.get('/api/get_user_water')
@authorization_required
def get_water(current_user):
    user_water = current_user["amount_of_water_drank"]
    return make_response(jsonify(user_water), 200)


@app.route("/signup", methods=["POST"])
def add_user():
    if request.method == "POST":
        # Retrieve POST request as JSONified payload.
        payload = request.get_json()

        # Extract username and password from payload.
        username = payload["username"]
        password = payload["password"]
        amount_of_water_drank = payload["amount_of_water_drank"]
        size_of_main_waterbottle = payload["size_of_main_waterbottle"]

        # Generate salt for strenghening password encryption.
        # NOTE: Salts add additional random bits to passwords prior to encryption.
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)

        # Create new user instance using username and hashed password.
        new_user = User(
            username=username,
            password_hash=hashed_password.decode("utf-8"),
            amount_of_water_drank = amount_of_water_drank,
            size_of_main_waterbottle = size_of_main_waterbottle,
        )

        if new_user is not None:
            # Add and commit newly created user to database.
            db.session.add(new_user)
            db.session.commit()

            # Save created user ID to server-persistent session storage.
            # NOTE: Sessions are to servers what cookies are to clients.
            # NOTE: Server sessions are NOT THE SAME as database sessions! (`session != db.session`)
            session["user_id"] = new_user.id

            return make_response(new_user.to_dict(only=("id", "username", "email")), 201)
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)


# POST route to authenticate user in database using session-stored credentials.
@app.route("/login", methods=["POST"])
def user_login():
    if request.method == "POST":
        # Retrieve POST request as JSONified payload.
        payload = request.get_json()

        # Filter database by username to find matching user to potentially login.
        matching_user = User.query.filter(User.username.like(f"%{payload['username']}%")).first()

        # Check submitted password against hashed password in database for authentication.
        AUTHENTICATION_IS_SUCCESSFUL = bcrypt.checkpw(
            password=payload["password"].encode("utf-8"),
            hashed_password=matching_user.password.encode("utf-8")
        )

        if matching_user is not None and AUTHENTICATION_IS_SUCCESSFUL:
            # Save authenticated user ID to server-persistent session storage.
            # NOTE: Sessions are to servers what cookies are to clients.
            # NOTE: Server sessions are NOT THE SAME as database sessions! (`session != db.session`)
            session["user_id"] = matching_user.id
            print(session["user_id"])

            return make_response(matching_user.to_dict(only=("id", "username")), 200)
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    


@app.route("/logout", methods=["DELETE"])
def user_logout():
    if request.method == "DELETE":
        # Clear user ID from server-persistent session storage.
        # NOTE: Sessions are to servers what cookies are to clients.
        # NOTE: Server sessions are NOT THE SAME as database sessions! (`session != db.session`)
        session["user_id"] = None

        return make_response({"msg": "User successfully logged out."}, 204)
    else:
        return make_response({"error": f"Invalid request type. (Expected DELETE; received {request.method}.)"}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)