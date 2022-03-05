import json
import functools
import logging
import secrets

from datetime import date

from flask import Blueprint, flash, Flask, g, jsonify, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from v0.db import get_db

logging.basicConfig(filename=f'./v0/log/auth_{date.today().strftime("%Y_%m_%d")}.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Return all users
# Not currently consumed by from end, maybe be useful for admin features in the future
@bp.route('/getusers', methods=('GET',))
def getusers():
    log(request.remote_addr, request.url, request.origin, request.method)
    if request.method == 'GET':
        users = get_db().execute("SELECT * FROM user").fetchall()
        return json.dumps( [dict(ix) for ix in users] )

# Return single user based on request parameter
@bp.route('/getuser/<int:id>', methods=('GET',))
def getuser(id):
    log(request.remote_addr, request.url, request.origin, request.method)
    if request.method == 'GET':
        # Should probably be converted to .fetchone()
        users = get_db().execute("SELECT username, dob, street, zip FROM user WHERE id = :id", {"id": id}).fetchall()
        return json.dumps( [dict(ix) for ix in users] )

# Update user account info with incoming JSON dob, street, zip, id
@bp.route('/update', methods=('POST',))
def update():
    log(request.remote_addr, request.url, request.origin, request.method)
    if request.method == 'POST':
        data = request.get_json()
        db = get_db()
        # dob, street, zip are all nullable fields, so no length validation
        db.execute("UPDATE user SET dob = :dob, street = :street, zip = :zip WHERE id = :id", {
            "id": data['id'],
            "dob": data['dob'],
            "street": data['street'],
            "zip": data['zip']
        })
        db.commit()
        return 'Data saved'

# Update user password with incoming JSON current, confirm, new, id
@bp.route('/updatepassword', methods=('POST',))
def updatepassword():
    log(request.remote_addr, request.url, request.origin, request.method)
    if request.method == 'POST':
        data = request.get_json()
        db = get_db()
        # Should probably be converted to .fetchone()
        user = db.execute("SELECT password FROM user WHERE id = :id", {"id": data['id']}).fetchall()

        if data['current'] != data['confirm']:
            return 'Passwords do not match'

        if check_password_hash(user[0]['password'], data['current']) and check_password_hash(user[0]['password'], data['confirm']):
            newpassword = generate_password_hash(data['new'])
            db.execute("UPDATE user SET password = :newpassword WHERE id = :id", {
                "id": data['id'],
                "newpassword": newpassword
            })
            db.commit()
            return 'Password saved'
        else:
            return 'Incorrect password'

# Register new user with incoming JSON username, password
@bp.route('/register', methods=('POST',))
def register():
    log(request.remote_addr, request.url, request.origin, request.method)
    if request.method ==  'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        db = get_db()
        error = None

        # Make sure username and password are both not empty
        if not username:
            error = 'Username is required.'
            return {
                "error": error
            }
        elif not password:
            error = 'Password is required.'
            return {
                "error": error
            }

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, dob, street, zip) VALUES (?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), '', '',''),
                )
                db.commit()
                return {
                    "response": "You have been successfully registered!"
                }
            except db.IntegrityError:
                # Return error if usersame is already in database
                error = f"User {username} is already registered."
                return {
                    "error": error
                }

        flash(error)

# Log user in with incoming JSON
@bp.route('/login', methods=('GET', 'POST'))
def login():
    log(request.remote_addr, request.url, request.origin, request.method)
    if request.method == 'POST':
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # Check if usersame exists and, if so, if the suppled password is correct
        if user is None:
            error = 'Username not found'
            return {
                "response": error
            }
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
            return {
                "response": error
            }

        if error is None:
            # Create new cookies
            # Remove any previous cookie from sessions table
            # Add new cookie to sessions table
            # Return cookie for client to store
            cookie = secrets.token_hex(64)
            userid = user[0]
            session.clear()
            session['user_id'] = user['id']
            db.execute(
                'DELETE FROM sessions WHERE userid = ?', (userid,)
            )
            db.execute(
                "INSERT INTO sessions (userid, session) VALUES (?, ?)",
                (userid, cookie),
            )
            db.commit()
            return {
                "response": 'Successfully logged in!',
                "token": cookie,
                "id": userid
            }

        flash(error)

    return {
        "response": "Undefined error"
    }

# Return whether user has a current session
@bp.route('/loggedin', methods=('GET', 'POST'))
def loggedin():
    log(request.remote_addr, request.url, request.origin, request.method)
    token = request.cookies.get('Token')
    id = request.cookies.get('Id')
    # Use id cookie to select user session from sessions table
    userSession = get_db().execute(
        'SELECT session FROM sessions WHERE userid = ?', (id,)
    ).fetchone()

    # Check if user session doesn't exist or if sessions cookie doesn't match incoming cookie
    if (not userSession) or (userSession[0] != token):
        return {
            "loggedIn": False
        }
    else:
        return {
            "loggedIn": id
        }

# Log user out user based on request parameter
@bp.route('/logout/<int:id>')
def logout(id):
    if request.method == 'GET':
        log(request.remote_addr, request.url, request.origin, request.method)
        session.clear()
        # Remove user session from sessions table
        get_db().execute(
            'DELETE FROM sessions WHERE userid = ?', (id,)
        )
        get_db().commit()
        return {
            "response": "Logged out"
        }

# Log function called by all endpoints
# This could potentially be better positioned as middleware that fires on every incoming request
def log(ip, url, origin, method):
    app.logger.info(f'user at ip {ip} requested {method} {url} from {origin}')
