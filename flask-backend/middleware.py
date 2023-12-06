#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Flask server request-response and session storage utilities.
from flask import make_response, session
# Configured application/server instance.
from config import app, db
# Relative access to user model.
from models import User

# Additional tools for extending decorator function logic.
from functools import partial, wraps


#######################################################
###### EXPORTABLE MIDDLEWARE UTILITY FUNCTION(S) ######
#######################################################


def authorization_required(func=None, methods=["GET"]):
    # Applied operations to handle optional `methods` argument for decorator.
    if func is None:
        return partial(authorization_required, methods=methods)
    
    # Factory function to tether wrapper to decorator.
    @wraps(func)

    # Inner authorization function.
    def decorated_authorizer(*args, **kwargs):
        # Retrieve existing and matching user ID from server-persistent session storage.
        # NOTE: Sessions are to servers what cookies are to clients.
        # NOTE: Server sessions are NOT THE SAME as database sessions! (`session != db.session`)
        user_id = session.get("user_id")

        if not user_id:
            return make_response({"error": "User account not authenticated. Please log in or sign up to continue using the application."}, 401)
        try:
            # Query users from database where authorized user exists (has matching ID).
            authorized_user = User.query.filter(User.id == user_id).first()
            if authorized_user is None:
                return make_response({"error": "Invalid username or password. Try again."}, 401)
            
            # Define methods authorized only for administrative access.
            UNAUTHORIZED_METHODS = ["POST", "PATCH", "DELETE"]
            # Check if any decorator-submitted methods are unauthorized to non-administrative users.
            if any(method in methods for method in UNAUTHORIZED_METHODS):
                # If so, check if currently authorized user is an administrator.
                if not authorized_user.is_administrator():
                    # If not, return an error response due to unauthorized access.
                    return make_response({"error": "Administrative permissions are required to access this part of the application."}, 401)
        except Exception as error:
            return make_response({"error": f"Something went wrong.", "details": str(error)}, 500)

        # Invoke wrapped view function with administrative access as output.
        return func(authorized_user.to_dict(), *args, **kwargs)
    return decorated_authorizer