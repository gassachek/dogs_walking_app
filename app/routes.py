from flask import Flask, request, redirect, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connection
from app import app



@app.route('/')
def index():
    return redirect('/profile') if get_current_user() else redirect('/authorization')

def get_current_user():
    return session.get('user_id')


def require_login():
    if not get_current_user():
        return redirect('/authorization')


@app.route('/profile')
def profile():
    user_id = get_current_user()
    if not user_id:
        return redirect('/authorization')

    with get_db_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT FullName, Email FROM Users WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()

        cursor.execute("""
            SELECT Dogs.DogName, Breeds.BreedName, Dogs.Size, Dogs.ActivityLevel
            FROM Dogs
            JOIN Breeds ON Dogs.BreedID = Breeds.BreedID
            WHERE Dogs.OwnerID = %s
        """, (user_id,))
        dogs = cursor.fetchall()

    return render_template('profile.html', user=user, dogs=dogs, user_id=user_id)


@app.route('/parks')
def parks():
    user_id = get_current_user()
    if not user_id:
        return redirect('/authorization')

    with get_db_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT ParkID, ParkName, Location, Description FROM Parks")
        parks = cursor.fetchall()

        cursor.execute("SELECT DogID, DogName FROM Dogs WHERE OwnerID = %s", (user_id,))
        dogs = cursor.fetchall()

    return render_template('parks.html', parks=parks, dogs=dogs, user_id=user_id)


@app.route('/meetings')
def meetings():
    user_id = get_current_user()
    if not user_id:
        return redirect('/authorization')

    with get_db_connection() as conn, conn.cursor() as cursor:
        cursor.execute("""
            SELECT Meetings.MeetingID, Meetings.StartDateTime, Meetings.Duration,
                   Parks.ParkName, Users.FullName
            FROM Meetings
            JOIN Parks ON Meetings.ParkID = Parks.ParkID
            JOIN Users ON Meetings.OrganizerID = Users.UserID
        """)
        meetings = cursor.fetchall()

        cursor.execute("SELECT DogID, DogName FROM Dogs WHERE OwnerID = %s", (user_id,))
        user_dogs = cursor.fetchall()

        meeting_participants = {}
        for meeting in meetings:
            cursor.execute("""
                SELECT Users.FullName, Dogs.DogName FROM MeetingDogs
                JOIN Dogs ON MeetingDogs.DogID = Dogs.DogID
                JOIN Users ON Dogs.OwnerID = Users.UserID
                WHERE MeetingDogs.MeetingID = %s
            """, (meeting[0],))
            meeting_participants[meeting[0]] = cursor.fetchall()

    return render_template('meetings.html', meetings=meetings, user_id=user_id,
                           user_dogs=user_dogs, meeting_participants=meeting_participants)


@app.route('/join_meeting', methods=['POST'])
def join_meeting():
    user_id = get_current_user()
    if not user_id:
        return redirect('/authorization')

    meeting_id = request.form['meeting_id']
    dog_id = request.form['dog_id']

    with get_db_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM MeetingDogs WHERE MeetingID = %s AND DogID = %s", (meeting_id, dog_id))
        if cursor.fetchone():
            return redirect('/meetings')

        cursor.execute("INSERT INTO MeetingDogs (MeetingID, DogID) VALUES (%s, %s)", (meeting_id, dog_id))
        conn.commit()

    return redirect('/meetings')


@app.route('/register', methods=['POST'])
def register():
    full_name = request.form['full_name']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    with get_db_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM Users WHERE Email = %s", (email,))
        if cursor.fetchone():
            return "Email уже зарегистрирован!", 400

        cursor.execute("""
            INSERT INTO Users (FullName, Email, Password)
            VALUES (%s, %s, %s) RETURNING UserID
        """, (full_name, email, password))
        user_id = cursor.fetchone()[0]
        conn.commit()

    session['user_id'] = user_id
    return redirect('/profile')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    with get_db_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT UserID, Password FROM Users WHERE Email = %s", (email,))
        user = cursor.fetchone()

    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]
        return redirect('/profile')

    return "Неверный email или пароль", 401


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/authorization')

@app.route('/authorization')
def authorization():
    return render_template('authorization.html')  # Создайте этот шаблон
