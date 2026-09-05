from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson import ObjectId
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

client = OpenAI()
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'flexplan_secret_key_2024')

# MongoDB Configuration
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/flexplan')
mongo = PyMongo(app)

# ─── AUTH ROUTES ─────────────────────────────────────────────────────────────

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': 'All fields required'}), 400

    if mongo.db.users.find_one({'email': email}):
        return jsonify({'error': 'Email already registered'}), 409

    hashed = generate_password_hash(password)
    user_id = mongo.db.users.insert_one({
        'username': username,
        'email': email,
        'password': hashed,
        'created_at': datetime.utcnow()
    }).inserted_id

    session['user_id'] = str(user_id)
    session['username'] = username
    return jsonify({'message': 'Registered successfully', 'username': username}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    user = mongo.db.users.find_one({'email': email})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    session['user_id'] = str(user['_id'])
    session['username'] = user['username']
    return jsonify({'message': 'Login successful', 'username': user['username']}), 200


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200


@app.route('/api/me')
def me():
    if 'user_id' not in session:
        return jsonify({'logged_in': False}), 200
    return jsonify({'logged_in': True, 'username': session['username']}), 200


# ─── PROGRESS ROUTES ─────────────────────────────────────────────────────────

@app.route('/api/progress', methods=['GET'])
def get_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    logs = list(mongo.db.progress.find({'user_id': session['user_id']}).sort('date', -1).limit(50))
    for log in logs:
        log['_id'] = str(log['_id'])
    return jsonify(logs), 200


@app.route('/api/progress', methods=['POST'])
def log_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    weight = float(data.get('weight', 0))
    height = float(data.get('height', 0))
    bmi = round(weight / ((height / 100) ** 2), 1) if height > 0 else 0
    entry = {
        'user_id': session['user_id'],
        'username': session['username'],
        'workout': data.get('workout', ''),
        'calories': int(data.get('calories', 0)),
        'weight': weight,
        'height': height,
        'bmi': bmi,
        'date': datetime.utcnow().strftime('%m/%d/%Y'),
        'created_at': datetime.utcnow()
    }
    result = mongo.db.progress.insert_one(entry)
    entry['_id'] = str(result.inserted_id)
    return jsonify(entry), 201


@app.route('/api/progress/<entry_id>', methods=['DELETE'])
def delete_progress(entry_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    mongo.db.progress.delete_one({'_id': ObjectId(entry_id), 'user_id': session['user_id']})
    return jsonify({'message': 'Deleted'}), 200


# ─── PAGE ROUTES ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/workouts')
def workouts():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('workouts.html')

@app.route('/diet')
def diet():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('diet.html')

@app.route('/progress')
def progress():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('progress.html')

@app.route('/bmi')
def bmi():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('bmi.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/api/ai-workout', methods=['POST'])
def ai_workout():

    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()

        goal = data.get("goal")
        level = data.get("level")
        days = data.get("days")

        prompt = f"""
Create a {days}-day workout plan.

Goal: {goal}
Level: {level}

Give exercises with sets and reps.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        workout = response.choices[0].message.content

        return jsonify({"plan": workout})

    except Exception as e:
        print(e)
        return jsonify({"error": "AI generation failed"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
