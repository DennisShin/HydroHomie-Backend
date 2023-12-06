from app import app
from models import db, User, Friends
from random import choice, randint
from faker import Faker
import bcrypt


faker = Faker()

def encypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)
    return hashed_password.decode('utf-8')

def make_users():
    users = []
    for _ in range(30):
        users.append(
            User(
                username=faker.name(),
                password= encypt_password("password"),
                amount_of_water_drank = randint(4, 12),
                size_of_main_waterbottle = 24
            )
        )
    return users

# def make_users_copy():
#     users = []
#     for _ in range(30):
#         users.append(
#             UserCopy(
#                 username=faker.name(),
#                 password=faker.word(),
#                 size_of_main_waterbottle = 24
#             )
#         )
#     return users

# def make_friends():
#     friends = []
#     for _ in range(10):
#         friends.append(
#             Friends(
#                 user1 = randint(1, 30),
#                 user2 = randint(1, 30)
#             ))
#     return friends
        
with app.app_context():
    print("Deleting old database data...")
    User.query.delete()
    Friends.query.delete()
    # UserCopy.query.delete()
    print("Complete....")

    print("Populating User database...")
    users = make_users()
    # usersCopy = make_users_copy()
    db.session.add_all(users)
    # db.session.add_all(usersCopy)
    db.session.commit()
    print("Complete....")

    print("Populating Friends database...")
    # friends = make_friends()
    # db.session.add_all(friends)
    # db.session.commit()
    print("Complete....")

    print("Database populated!")