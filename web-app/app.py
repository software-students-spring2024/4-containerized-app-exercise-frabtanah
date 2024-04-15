"""This module contains the web routes and logic for a Flask web application."""
import sys
import os

import datetime

import requests
from flask import Flask, render_template, request, redirect, flash, url_for, session
import pymongo

# from pymongo.server_api import ServerApi
import bcrypt
from dotenv import load_dotenv

# image imports
import base64
from bson import binary

# load credentials and configuration options from .env file
load_dotenv()  # take environment variables from .env.

# instantiate the app
app = Flask(__name__)

# connect to the database
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# @app.route('/predict-image', methods=['POST'])
# def predict_image():
#     # Assuming the image is sent as a file in the request
#     image_file = request.files['image']

#     # URL of the machine learning client API
#     api_url = 'http://machine-learning-client:5000/predict'  # Adjust based on your actual service name and port

#     # Preparing the files dict for requests to send as multipart/form-data
#     files = {'image': (image_file.filename, image_file, image_file.mimetype)}

#     # Making the POST request to the machine learning API
#     response = requests.post(api_url, files=files)

#     # Handle the response
#     if response.status_code == 200:
#         result = response.json()
#         return jsonify(result)
#     else:
#         return jsonify({'error': 'Failed to get prediction'}), response.status_code

@app.route('/save_picture', methods=['POST'])
def save_picture():
    """
    route to save the picture
    """
    if "email" not in session:
        flash("You must be logged in to save a picture.", "error")
        return redirect(url_for('show_signin'))

    image_data = request.form['image']
    if image_data:
        #strip the header from the image data
        header, encoded = image_data.split(",", 1)
        data = base64.b64decode(encoded)
        
        api_url = 'http://machine-learning-client:5000/predict'
        # emote = model.fetch_and_predict(data)

        # Making the POST request to the machine learning API
        response = requests.post(api_url, data=data)

        emote = response.json().get('predicted_class', 'Unknown')  # Adjust key as per your API's response
        
        #new assessment entry with the image
        current_date = datetime.datetime.now().strftime("%Y-%m-%d") 
        new_assessment = {
            "image_data": binary.Binary(data),
            "emotion_predict": emote,
            "currentDate": current_date  
        }
        #pusha new assessment into the assessments array
        db.users.update_one(
            {"email": session['email']},
            {"$push": {"assessments": new_assessment}}
        )

        flash('Picture saved successfully!', 'success')
        return redirect(url_for('assessments'))
    else:
        flash('No picture to save.', 'error')
        return redirect(url_for('picture'))

@app.route('/picture')
def picture():
    """
    display picture taking page
    """
    return render_template('picture.html')

@app.route("/")
def home():
    """
    Route for the home page
    """
    if "email" in session:
        return render_template("landing.html", logged_in=True)
    return render_template("landing.html", logged_in=False)


@app.route("/sign_up")
def show_signup():
    """
    Route for the sign up page
    """
    return render_template("sign_up.html")


@app.route("/sign_in")
def show_signin():
    """
    Route for the sign in page
    """
    return render_template("sign_in.html")


@app.route("/profile")
def profile():
    """
    profile
    """
    if "email" in session:
        user = db.users.find_one({"email": session["email"]})
        return render_template("profile.html", user=user)
    return redirect(url_for("show_signin"))


@app.route("/sign_in", methods=["POST"])
def sign_in():
    """
    sign in
    """
    email = request.form.get("email")
    password = request.form.get("password").encode("utf-8")

    if not all([email, password]):
        return redirect(url_for("show_signin"))

    user = db.users.find_one({"email": email})
    if user:
        hashed_password = user.get("password")

        if bcrypt.checkpw(password, hashed_password):
            session["email"] = user["email"]
            return redirect(url_for("assessment"))

        error_message = "Wrong Pass."
        return render_template("sign_in.html", error=error_message)

    error_message = "Credentials not found."
    return render_template("sign_in.html", error=error_message)


@app.route("/sign_up", methods=["POST"])
def sign_up():
    """
    Post route for user creation of their user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    full_name = request.form.get("full_name")

    if password is not None:
        password_bytes = password.encode("utf-8")
    else:
        error_message = "Missing password"
        return render_template("sign_up.html", error=error_message)

    if not all([email, password, full_name]):
        error_message = "Missing Fields"
        return render_template("sign_up.html", error=error_message)

    if db.users.find_one({"email": email}):
        error_message = "Email already in use"
        return render_template("sign_up.html", error=error_message)

    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    db.users.insert_one({"email": email, "password": hashed, "full_name": full_name})
    session["email"] = email

    return redirect(url_for("assessment"))


@app.route("/logout")
def logout():
    """
    User logout route
    """
    session.pop("email", None)
    return redirect(url_for("home"))


@app.route("/delete_profile", methods=["POST"])
def delete_profile():
    """
    Route to delete the current user's profile
    """
    if "email" in session:
        email = session["email"]
        db.users.delete_one({"email": email})
        session.pop("email", None)
        return redirect(url_for("home"))
    return redirect(url_for("home"))


@app.route("/change_password")
def show_change_password():
    """
    Route for the change password page.
    """
    return render_template("change_password.html")


@app.route("/change_pass", methods=["POST"])
def change_pass():
    """
    Update the user password
    """
    new_password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if not new_password or not confirm_password:
        error_message = "Missing password or confirmation password."
        return render_template("change_password.html", error=error_message)

    if new_password != confirm_password:
        error_message = "Passwords do not match."
        return render_template("change_password.html", error=error_message)

    if "email" in session:
        email = session["email"]
        user = db.users.find_one({"email": email})

        if not user:
            error_message = "User not found."
            return render_template("change_password.html", error=error_message)

        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        db.users.update_one({"email": email}, {"$set": {"password": hashed_password}})
        return redirect(url_for("profile"))

    error_message = "User is not logged in."
    return render_template("login.html", error=error_message)


@app.route('/assessments')
def assessments():
    """
    route to show assessments
    """
    if "email" not in session:
        flash("You must be logged in to view assessments.", "error")
        return redirect(url_for('show_signin'))

    email = session['email']
    user = db.users.find_one({"email": email})

    assessments_list = []
    if user and "assessments" in user:
        for assessment in user['assessments']:
            #check if the assessment is an image or text
            if 'image_data' in assessment:
                image_b64 = base64.b64encode(assessment['image_data']).decode('utf-8')
                assessments_list.append({
                    'type': 'image',
                    'image_b64': image_b64,
                    'emotion_predict': assessment['emotion_predict'],
                    'currentDate': assessment['currentDate']
                })
            else:
                assessments_list.append({
                    'type': 'text',
                    'mainEmotion': assessment['mainEmotion'],
                    'subEmotion': assessment['subEmotion'],
                    'postActivity': assessment['postActivity'],
                    'currentDate': assessment['currentDate']
                })

    return render_template('assessments.html', assessments=assessments_list)


@app.route("/assessment")
def show_assessment():
    """
    shows assessment
    """
    if "email" in session:
        return render_template("assessment.html")
    return redirect(url_for("show_signin"))


@app.route("/assessment", methods=["POST"])
def assessment():
    """
    Route to input mood assessment
    """
    if "email" in session:
        email = session["email"]
        user = db.users.find_one({"email": email})

        if user:
            main_emotion = request.form["main-emotion"]
            sub_emotion = request.form["sub-emotion"]
            post_activity = request.form["post-activity"]
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            if not main_emotion or not sub_emotion or not post_activity:
                return render_template(
                    "assessment.html", error="Please enter all fields"
                )

            assessment_data = {
                "mainEmotion": main_emotion,
                "subEmotion": sub_emotion,
                "postActivity": post_activity,
                "currentDate": current_date,
            }

            db.users.update_one(
                {"email": email}, {"$push": {"assessments": assessment_data}}
            )

            return redirect(url_for("profile"))

    error_message = "User not found."
    return render_template("assessment.html", error=error_message)


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "8000")
    app.run(port=FLASK_PORT)
