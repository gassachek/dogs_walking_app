# from flask import Flask, request, redirect, render_template, session
# from app.db import get_db_connection
# from app import app
#
# app.secret_key = 'supersecretkey'
#
# @app.route('/profile/<int:user_id>')
# def profile(user_id):
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     if 'user_id' not in session:
#         return redirect('/authorization')
#
#     user_id = session['user_id']
#
#     # Получение данных пользователя
#     cursor.execute("SELECT FullName, Email FROM Users WHERE UserID = %s", (user_id,))
#     user = cursor.fetchone()
#
#     # Получение списка собак пользователя
#     cursor.execute("""
#             SELECT Dogs.DogName, Breeds.BreedName, Dogs.Size, Dogs.ActivityLevel
#             FROM Dogs
#             JOIN Breeds ON Dogs.BreedID = Breeds.BreedID
#             WHERE Dogs.OwnerID = %s
#         """, (user_id,))
#     dogs = cursor.fetchall()
#
#     cursor.close()
#     connection.close()
#
#     return render_template('profile.html', user=user, dogs=dogs, user_id=user_id)
#
# @app.route('/parks')
# def parks():
#     if 'user_id' not in session:
#         return redirect('/authorization')
#
#     user_id = session['user_id']
#
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     # Получение списка парков
#     cursor.execute("SELECT ParkID, ParkName, Location, Description FROM Parks")
#     parks = cursor.fetchall()
#
#     # Получение собак пользователя
#     cursor.execute("""
#         SELECT DogID, DogName FROM Dogs WHERE OwnerID = %s
#     """, (user_id,))
#     dogs = cursor.fetchall()
#
#     cursor.close()
#     connection.close()
#
#     return render_template('parks.html', parks=parks, dogs=dogs, user_id=user_id)
#
#
# @app.route('/meetings')
# def meetings():
#     if 'user_id' not in session:
#         return redirect('/authorization')
#
#     user_id = session['user_id']
#
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     # Получение данных о встречах
#     cursor.execute("""
#         SELECT Meetings.MeetingID, Meetings.StartDateTime, Meetings.Duration,
#                Parks.ParkName, Users.FullName
#         FROM Meetings
#         JOIN Parks ON Meetings.ParkID = Parks.ParkID
#         JOIN Users ON Meetings.OrganizerID = Users.UserID
#     """)
#     meetings = cursor.fetchall()
#
#     # Получение списка собак пользователя
#     cursor.execute("""
#         SELECT DogID, DogName FROM Dogs WHERE OwnerID = %s
#     """, (user_id,))
#     user_dogs = cursor.fetchall()
#
#     # Получение участников для каждой встречи
#     meeting_participants = {}
#     for meeting in meetings:
#         cursor.execute("""
#             SELECT Users.FullName, Dogs.DogName FROM MeetingDogs
#             JOIN Dogs ON MeetingDogs.DogID = Dogs.DogID
#             JOIN Users ON Dogs.OwnerID = Users.UserID
#             WHERE MeetingDogs.MeetingID = %s
#         """, (meeting[0],))
#         meeting_participants[meeting[0]] = cursor.fetchall()
#
#     cursor.close()
#     connection.close()
#
#     return render_template('meetings.html', meetings=meetings, user_id=user_id, user_dogs=user_dogs,
#                            meeting_participants=meeting_participants)
#
#
# @app.route('/join_meeting', methods=['POST'])
# def join_meeting():
#     if 'user_id' not in session:
#         return redirect('/authorization')
#
#     user_id = session['user_id']
#     meeting_id = request.form['meeting_id']
#     dog_id = request.form['dog_id']
#
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     # Проверяем, участвует ли уже собака в этой встрече
#     cursor.execute("SELECT * FROM MeetingDogs WHERE MeetingID = %s AND DogID = %s", (meeting_id, dog_id))
#     existing_entry = cursor.fetchone()
#
#     if existing_entry:
#         cursor.close()
#         connection.close()
#         return redirect('/meetings')
#
#     # Добавляем собаку во встречу
#     cursor.execute("INSERT INTO MeetingDogs (MeetingID, DogID) VALUES (%s, %s)", (meeting_id, dog_id))
#     connection.commit()
#
#     cursor.close()
#     connection.close()
#
#     return redirect('/meetings')
#
# @app.route('/create_meeting', methods=['POST'])
# def create_meeting():
#     if 'user_id' not in session:
#         return redirect('/authorization')
#
#     user_id = session['user_id']
#     park_id = request.form['park_id']
#     date = request.form['date']
#     time = request.form['time']
#     duration = request.form['duration']
#     dog_ids = request.form.getlist('dog_ids')  # Получаем список выбранных собак
#
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     # Добавляем встречу в базу данных
#     cursor.execute("""
#         INSERT INTO Meetings (OrganizerID, ParkID, StartDateTime, Duration, Status)
#         VALUES (%s, %s, %s, %s, 'scheduled')
#         RETURNING MeetingID
#     """, (user_id, park_id, f"{date} {time}", f"{duration} minutes"))
#
#     meeting_id = cursor.fetchone()[0]
#
#     # Добавляем собак в таблицу MeetingDogs
#     for dog_id in dog_ids:
#         cursor.execute("""
#             INSERT INTO MeetingDogs (MeetingID, DogID) VALUES (%s, %s)
#         """, (meeting_id, dog_id))
#
#     connection.commit()
#     cursor.close()
#     connection.close()
#
#     return redirect('/meetings')
#
# @app.route('/authorization')
# def authorization():
#     return render_template('authorization.html')
#
# @app.route('/login', methods=['POST'])
# def login():
#     email = request.form['email']
#     password = request.form['password']
#
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     # Проверка пользователя
#     cursor.execute("SELECT UserID, Password FROM Users WHERE Email = %s", (email,))
#     user = cursor.fetchone()
#
#     cursor.close()
#     connection.close()
#
#     if user and user[1] == password:  # Пока без хеширования (рекомендуется использовать bcrypt)
#         session['user_id'] = user[0]
#         return redirect(f'/profile/{user[0]}')  # Перенаправляем на страницу профиля
#     else:
#         return "Неверный email или пароль", 401  # Ошибка, если данные неверны
#
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect('/authorization')  # Перенаправление на страницу входа
#
# @app.route('/registration', methods=['GET'])
# def registration():
#     return render_template('registration.html')
#
# @app.route('/register', methods=['POST'])
# def register():
#     full_name = request.form['full_name']
#     email = request.form['email']
#     password = request.form['password']  # Пароль пока без хеширования (рекомендуется использовать bcrypt)
#
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     # Проверка, есть ли пользователь с таким email
#     cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
#     existing_user = cursor.fetchone()
#
#     if existing_user:
#         return "Email уже зарегистрирован!", 400  # Ошибка, если email уже используется
#
#     # Добавление нового пользователя
#     cursor.execute("""
#         INSERT INTO Users (FullName, Email, Password) VALUES (%s, %s, %s)
#         RETURNING UserID
#     """, (full_name, email, password))
#     user_id = cursor.fetchone()[0]
#
#     connection.commit()
#     cursor.close()
#     connection.close()
#
#     # Запоминаем пользователя в сессии
#     session['user_id'] = user_id
#     return redirect(f'/profile/{user_id}')
#
# # Обработчик формы для добавления собаки
# @app.route('/add_dog', methods=['POST'])
# def add_dog():
#     if 'user_id' not in session:
#         return redirect('/authorization')
#
#     owner_id = session['user_id']  # Теперь используется ID текущего пользователя
#     dog_name = request.form['dog_name']
#     breed_id = request.form['breed_id']
#     size = request.form['size']
#     activity_level = request.form['activity_level']
#
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     cursor.execute("""
#         INSERT INTO Dogs (OwnerID, BreedID, DogName, Size, ActivityLevel)
#         VALUES (%s, %s, %s, %s, %s)
#     """, (owner_id, breed_id, dog_name, size, activity_level))
#
#     connection.commit()
#     cursor.close()
#     connection.close()
#
#     return redirect(f'/profile/{owner_id}')


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
