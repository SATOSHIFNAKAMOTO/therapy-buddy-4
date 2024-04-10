from flask import Flask, render_template, session, redirect, url_for, g, request
import sqlite3
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'iRp8jpM7Hp2tZnOVKsokALou'  # Change this to a real secret key

@app.route('/')
def index():
    db = get_db()
    moods = db.execute('SELECT mood FROM moods').fetchall()
    return render_template('index.html', moods=moods)

@app.route('/login')
def login():
    # Redirect to Choreo's managed authentication login endpoint
    return redirect('https://3fdfee4d-6535-45b6-88cd-f21cd39cea2d.e1-us-cdp-2.choreoapps.dev/auth/login')

@app.route('/logout')
def logout():
    # Redirect to Choreo's managed authentication logout endpoint
    return redirect('https://3fdfee4d-6535-45b6-88cd-f21cd39cea2d.e1-us-cdp-2.choreoapps.dev/auth/logout')


@app.route('/submit_mood', methods=['POST'])
def submit_mood():
    data = request.get_json()  # Correctly call the method and assign the result to the 'data' variable
    mood = data['mood']
    db = get_db()
    db.execute('INSERT INTO moods (mood) VALUES (?)', (mood,))
    db.commit()
    return jsonify({'status': 'success', 'mood': mood})


@app.route('/show_login', methods=['GET'])
def show_login():
    return render_template('login.html')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            '/Users/satoshinakamoto/Documents/Therapy Buddy 4/moods.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        print("Initializing the database....")
        db.execute('CREATE TABLE IF NOT EXISTS moods (id INTEGER PRIMARY KEY, mood TEXT)')
        db.commit()
        print("Database initialized.")


if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)
