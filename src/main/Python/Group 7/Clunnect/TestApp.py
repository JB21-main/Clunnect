from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from Controllers.AuthController import AuthController
from Controllers.ClubController import ClubController
from Services.DBmgr import DBmgr
from Services.UserCreator import UserCreator

print("Loaded app module from:", __name__)

app = Flask(__name__)
app.secret_key = "supersecretkey"

print("before")
dbmgr = DBmgr()
auth_controller = AuthController(dbmgr)
club_controller = ClubController(dbmgr)
print("after")

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        result = auth_controller.authenticate(username, password)

        if result["success"]:
            session['user'] = result["data"]['user']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash(result.get('error', 'Login failed.'), 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        success, message = auth_controller.register(username,email,password)

        if success:
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash(message, "danger")
            return redirect(url_for('register'))
        
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/create_club', methods=['GET', 'POST'])
def create_club():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        owner_id = session['user']['id']

        success, message = club_controller.create_club(name, description, owner_id)
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('create_club'))
        
    return render_template('create-club.html')

@app.route('/join_club', methods=['GET', 'POST'])
def join_club():
    clubs = dbmgr.get_club_list()
    return render_template('join-club.html', clubs=clubs)

@app.route('/join_club/<int:club_id>', methods=['POST'])
def join_club_post(club_id):
    user_id = session['user']['id']
    try:
        dbmgr.add_user_to_clubs(user_id,club_id)
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error joining club: {str(e)}", 400

if __name__ == "__main__":
    app.run(debug=True)