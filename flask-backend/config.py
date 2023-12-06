#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Flask application architecture tools.
from flask import Flask
# Cross-origin resource sharing tools.
from flask_cors import CORS
# Database migration and updating tools.
from flask_migrate import Migrate
# SQLAlchemy Flask-to-SQL communications tools.
from flask_sqlalchemy import SQLAlchemy
# SQL database schema metadata management tools.
from sqlalchemy import MetaData

# Environment variable loading and operational tools.
from dotenv import load_dotenv
import os

# Initialize Flask server application.
app = Flask(__name__)
# Set application to connect to new SQLite database.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hydrohomie.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# OPTIONAL: Configure naming conventions on SQLite database migration files.
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Instantiate SQLAlchemy connection to database instance.
db = SQLAlchemy(metadata=metadata)

# Tether database connection via migration from database instance to application server.
migrate = Migrate(app, db)
db.init_app(app)


#######################################################
########## ADDITIONAL SERVER CONFIGURATION(S) #########
#######################################################


# Enable cross-origin resource sharing between server and HTTP-based clients.
CORS(app)

# Load environment variables for additional application configuration.
load_dotenv()
# Configure application server with custom authentication token.
app.secret_key = "CompleteSecretKeySMILECHAMP"
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")