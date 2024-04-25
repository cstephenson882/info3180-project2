from app import db
from .forms import RegisterForm, LoginForm, PostForm
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
from app import app
from flask import flash, redirect, render_template, request, jsonify, send_file, send_from_directory, session, url_for
import os
from app.models import Posts, Likes, Follows, Users
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf



def tokencheck(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            login = ""
            if not 'Authorization' in request.headers:
                return jsonify({"error": "Incorrent token!"}), 400
            token = request.headers["Authorization"].split(" ")[1]
            try:
                login = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            except:
                return jsonify({"error": "token missing!"}), 400
            return f(*args, **kws)    
    return decorated_function

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/')
def index(user):
    return jsonify({"message":"This is the beginning of our API"})

@app.route("/api/v1/register", methods=["POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form['username']
        biography = request.form['biography']
        file = form.profile.data
        filename = secure_filename(file.filename)    
        password = request.form['confirm_password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        location = request.form['location']
        filename = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filename)
        
    
        user = Users.query.filter_by(username=username).first()
        if user:
            return jsonify({"error": "Username already taken"}), 400
        user = Users.query.filter_by(email=email).first()
        if user:
            return jsonify({"error": "Email associated with another account"}), 400

        user = Users(username=username,password=generate_password_hash(password, method='pbkdf2:sha256'),firstname=firstname,lastname=lastname,email=email,location=location,biography=biography,profile=filename)

        db.session.add(user)
        try:
            db.session.commit()
            joined = user.joined_on

            response ={
                "message": "Successfully registered",
                "username": str(username),
                "password": str(user.password),
                "firstname": str(firstname),
                "lastname": str(lastname),
                "email": str(email),
                "location": str(location),
                "biography": str(biography),
                "profile_photo": f"/api/v1/photo/{str(filename)}",
                "joined_on": str(joined)
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({"error":"Failed to register"}), 400
    else: 
        errors = form_errors(form)
        response = {"errors": errors}
        return jsonify(response), 400
    


@app.route("/api/v1/users/<userId>", methods=["GET"])
def get_user(userId):
    following = False
    if (userId == "currentuser"):
        token = request.headers["Authorization"].split(" ")[1]
        user = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        userId = user['id']
    
    following = Users.query.filter_by(id=userId).first()
    current_user  = Users.query.filter_by(id=session['id']).first()
    checkfollows = Follows.query.filter_by(follower=following, currentuser=current_user).all()

    for follows in checkfollows:
        if follows.follower_id == int(userId):
            following = True
            break
    user = Users.query.filter_by(id=userId).first()
    if (not user):
        return jsonify({"error": "Not Possible"}), 400
  

    return jsonify({
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "location": user.location,
            "biography": user.biography,
            "profile_photo": "/api/v1/photo/" + user.profile,
            "joined_on": user.joined_on,
            "Following" : following
        }), 200



@app.route("/api/v1/users/<userId>/posts", methods=["POST"])
@tokencheck
def create_post(userId):
    form = PostForm()
    user = Users.query.get(userId)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if form.validate_on_submit():
        file = form.photo.data
        caption = form.caption.data
        filename = secure_filename(file.filename)
        img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(img_url)

        post = Posts(photo=filename, caption=caption, user=user)

        db.session.add(post)
        db.session.commit()

        return jsonify({"message": "Posted"})
    else:
        errors = form_errors(form)
        return jsonify({"errors": errors}), 400


@app.route("/api/v1/auth/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            data = {'id': user.id, 'username': user.username}
            session['id'] = user.id
            token = jwt.encode(data, app.config["SECRET_KEY"], algorithm="HS256")
            return jsonify({"message": "Logged in sucessful", "token": token})
        else:
            return jsonify({"errors": ["Incorrect Username or Password"]}), 401
    else:
        errors = form_errors(form)
        return jsonify({"errors": errors}), 400

      
        
@app.route("/api/v1/auth/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Succesfully logged out"})






@app.route("/api/v1/users/<userId>/posts", methods=["GET"])
@tokencheck
def get_posts(userId):
    user = Users.query.get(userId)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    posts_data = [{"photo": "/api/v1/photo/" + post.photo, "caption": post.caption} for post in user.posts]
    
    return jsonify({"posts": posts_data})




@app.route("/api/v1/posts", methods=["GET"])
def all_posts():
    posts = Posts.query.all()
    user_likes = Likes.query.filter_by(user_id=int(session.get('id', -1))).all()
    liked_post_ids = {like.post_id for like in user_likes}
    
    all_posts_data = []
    for post in posts:
        post_data = {
            "id": post.id,
            "user_id": post.user_id,
            "photo": "/api/v1/photo/" + post.photo,
            "caption": post.caption,
            "created_at": post.created_on,
            "likes": len(post.likes),
            "style": post.id in liked_post_ids,
            "style1": post.id not in liked_post_ids
        }
        all_posts_data.append(post_data)
    
    return jsonify({"posts": all_posts_data})



@app.route("/api/users/<userId>/follow", methods=["POST"])
@tokencheck
def follow(userId):
    login = Users.query.filter_by(id=userId).first()
    if(not login):
        return jsonify({"error": "user does not exist"})
    data = request.get_json()
    target_id = data['follow_id']

    targetuser = Users.query.filter_by(id=target_id).first()
    checkfollows = Follows.query.filter_by(follower=targetuser, currentuser=login).all()

    for follows in checkfollows:
        if int(follows.follower_id) == int(targetuser.id):
            return jsonify({"message": "You are now following " + targetuser.username})

    follow = Follows(follower=targetuser, currentuser=login)
    db.session.add(follow)
    db.session.commit()

    return jsonify({"message": "You are now following " + targetuser.username})


@app.route("/api/users/<userId>/follow", methods=["GET"])
@tokencheck
def get_followers(userId):
    try:
        auth_header = request.headers["Authorization"].split(" ")[1]
        decoded_token = jwt.decode(auth_header, app.config['SECRET_KEY'], algorithms="HS256")
    except:
        return jsonify({"error": "Invalid token!"}), 400
    
    user = Users.query.filter_by(id=userId).first()

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"followers_count": len(user.following)})


@app.route("/api/v1/posts/<postId>/like", methods=["POST"])
def like_post(postId):
    try:
        auth_header = request.headers["Authorization"].split(" ")[1]
        decoded_token = jwt.decode(auth_header, app.config['SECRET_KEY'], algorithms="HS256")
    except:
        return jsonify({"error": "Invalid token!"}), 400

    user_id = decoded_token['id']
    user = Users.query.filter_by(id=user_id).first()
    post = Posts.query.filter_by(id=postId).first()
    existing_likes = Likes.query.filter_by(user_id=user_id).all()

    for like in existing_likes:
        if int(like.post_id) == int(postId):
            return jsonify({"error": "Post already liked"}), 404

    new_like = Likes(post=post, user=user)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"likes": len(post.likes)})


@app.route("/api/v1/photo/<filename>", methods=['GET'])
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

def form_errors(form):
    error_messages = []
  
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
   
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
 
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404