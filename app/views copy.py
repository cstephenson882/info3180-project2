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
        pic = form.profile.data
        filename = secure_filename(pic.filename)    
        password = request.form['confirm_password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        location = request.form['location']
        img_url = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        pic.save(img_url)

    
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
                "profile_photo": "/api/v1/photo/" + str(filename),
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
    
    targetuser = Users.query.filter_by(id=userId).first()
    me  = Users.query.filter_by(id=session['id']).first()
    checkfollows = Follows.query.filter_by(follower=targetuser, currentuser=me).all()

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
    id = userId
    user = Users.query.filter_by(id=id).first()
    if(not user):
        return jsonify({"message": "Not Possible"})
    
    if  form.validate_on_submit():
        file = form.photo.data
        caption = request.form['caption']
        filename = secure_filename(file.filename)
        img_url = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(img_url)

        post = Posts(photo=filename,caption=caption,user=user)

        db.session.add(post)
        db.session.commit()

        return jsonify({"message": "Posted"})
    else:
        errors = form_errors(form)
        response = {'errors': errors}
        return jsonify(response), 400

@app.route("/api/v1/auth/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect login information')
            return jsonify({'errors': ["Incorrect Username or Password"]})
            
        data = {}
        data['id'] = user.id
        data['username'] = user.username
        session['id'] = user.id
        
        token = jwt.encode(data, app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"message": "User successfully logged in","token": token})
    else:
        errors = form_errors(form)
        response = {'errors': errors}
        return jsonify(response), 400
      
        
@app.route("/api/v1/auth/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Succesfully logged out"})






@app.route("/api/v1/users/<userId>/posts", methods=["GET"])
@tokencheck
def get_posts(userId):

    user = Users.query.filter_by(id=userId).first()
    posts = user.posts
    allPosts = []
    for post in posts:
        allPosts.append({"photo": "/api/v1/photo/" + post.photo,"caption": post.caption})

    return jsonify({"posts": allPosts})



@app.route("/api/v1/posts", methods=["GET"])
def all_posts():
    posts = Posts.query.all()
    likeornot = []
    checkid = Likes.query.filter_by(user_id=int(session['id'])).all()
    for i, likes in enumerate(checkid):
        if int(likes.post_id) == posts[i].id:
            likeornot.append(False)
        else:
            likeornot.append(True)


    for i in range(len(posts)):
        try:
            likeornot[i]
        except Exception:
            likeornot.append(True)
   
    allPosts = []
    for i, post in enumerate(posts):
        postt = {
            "id": post.id,
            "user_id": post.user_id,
            "photo": "/api/v1/photo/" + post.photo,
            "caption": post.caption,
            "created_at": post.created_on,
            "likes": len(post.likes),
            "style": likeornot[i],
            "style1": not likeornot[i]
         
        }
        allPosts.append(postt)
    return jsonify({"posts": allPosts})


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
def followers(userId):
    login = Users.query.filter_by(id=userId).first()

    if(not login):
        return jsonify({"error": "NOT POSSIBLE"}), 400
    
    return jsonify({"followers": len(login.following)})


@app.route("/api/v1/posts/<postId>/like", methods=["POST"])
def like(postId):
    try:
        token = request.headers["Authorization"].split(" ")[1]
        decoded_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    except:
        return jsonify({"error": "Incorrect token!"}), 400
    userId = decoded_data['id']
    login = Users.query.filter_by(id=userId).first()
    post = Posts.query.filter_by(id=postId).first()
    checkid = Likes.query.filter_by(user_id=userId).all()
    for likes in checkid:
        if int(likes.post_id) ==int(postId):
            return jsonify({
                "error": "Post already liked"
            }), 404
    like = Likes(posts=post, user=login)
    db.session.add(like)
    db.session.commit()

    return jsonify({
        "likes": len(post.likes)
    })

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