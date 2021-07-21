from flask_app import app

from flask_app.controllers import users

if __name__=="__main__":
    app.run(debug=True)
    app.secret_key = "O-hi-Mark"
# idk if secret key goes here or __init__.py