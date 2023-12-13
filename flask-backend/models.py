from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from config import db



# db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ("-friends.user", )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    amount_of_water_drank = db.Column(db.Integer)
    water_goal = db.Column(db.Integer, default=16, nullable=False)
    size_of_main_waterbottle = db.Column(db.Integer)

    friends = db.relationship("Friends", back_populates = "user")

# class UserCopy(db.Model, SerializerMixin):
#     __tablename__ = 'usersCopy'
#     serialize_rules = ("-friends.userCopy", )

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     size_of_main_waterbottle = db.Column(db.Integer)

#     friends = db.relationship("Friends", back_populates = "userCopy")



class Friends(db.Model, SerializerMixin):
    __tablename__ = 'friends'
    serialize_rules = ("-user.friends", )

    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey("users.id") ,nullable=False)
    # user2 = db.Column(db.Integer, db.ForeignKey("usersCopy.id") ,nullable=False)

    user = db.relationship("User", back_populates = "friends")
    # userCopy = db.relationship("UserCopy", back_populates = "friends")
