from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from Controllers.AuthController import AuthController
from Controllers.ClubController import ClubController
from Controllers.EventController import EventController
from Controllers.JoinClubController import JoinClubController
from Controllers.SearchController import SearchController       
from Controllers.AccountController import AccountController
from Services.DBmgr import DBmgr
from Services.UserCreator import UserCreator

print("Loaded app module from:", __name__)

app = Flask(__name__)
app.secret_key = "supersecretkey"

print("before")
dbmgr = DBmgr()
auth_controller = AuthController(dbmgr)
club_controller = ClubController(dbmgr)
event_controller = EventController(dbmgr)
join_club_controller = JoinClubController(dbmgr)
search_controller = SearchController(dbmgr=dbmgr)    
account_controller = AccountController(dbmgr=dbmgr) 
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
            return redirect(url_for('homepage'))
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
        category = request.form.get('category')
        meeting_day = request.form.get("meeting_day")
        meeting_time = request.form.get("meeting_time")
        owner_id = session['user']['id']

        success, message = club_controller.create_club(name, description, category, meeting_day, meeting_time,owner_id)
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('create_club'))
        
    return render_template('create-club.html')

@app.route('/edit_club', methods=['GET', 'POST'])
def edit_club():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    owner_id = session['user']['id']
    clubs = dbmgr.find_club_by_owner(owner_id)

    if request.method == 'POST':
        delete_flag = request.form.get('delete_club') == '1'
        club_id = int(request.form.get('club_id'))
        if delete_flag:
            club_controller.delete_club(club_id, owner_id)
            flash("Club deleted successfully", "success")
            return redirect(url_for('dashboard'))

        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        date = request.form.get('meeting_day')
        time =  request.form.get('meeting_time')
        
        club_id = int(request.form.get('club_id'))

        if not club_id:
            flash("Please select a event", "danger")
            return redirect(url_for(edit_event))

        club_dict = {
            "name": name,
            "description": description,
            "category": category,
            "date": date,
            "time": time
        }

        success, result = club_controller.edit_club(club_id, name, description, category, date, time, owner_id)
        
        if success:
            flash("Event created successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash(result, "danger")
            return redirect(url_for('edit_club'))

    return render_template('edit-club.html', user=session['user'], clubs=clubs)

@app.route('/join_club', methods=['GET', 'POST'])
def join_club():
    clubs = dbmgr.get_club_list()
    return render_template('join-club.html', clubs=clubs)

@app.route('/join_club/<int:club_id>', methods=['POST'])
def join_club_post(club_id):
    user_id = session['user']['id']
    try:
        result = join_club_controller.join_club(user_id,club_id)
        
    
        if result != "Joined successfully":
            flash(result, "warning")
            return redirect(url_for('join_club'))
        else:
            flash("You joined the club!", "success")
            return redirect(url_for('join_club'))
    except Exception as e:
        return f"Error joining club: {str(e)}", 400
    
@app.route('/api/search', methods=['GET'])
def handle_search():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    search_query = request.args.get('query')
    
    results = search_controller.search(search_query)
    return jsonify(results)

@app.route('/api/update-account', methods=['POST'])
def handle_account_update():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    username = data.get('username')
    new_pass = data.get('password')
    user_id = session['user']['id'] 
    
    success, message = account_controller.change_account_info(
        username=username,
        new_pass=new_pass,
        user_id=user_id
    )
    return jsonify({"success": success, "message": message})

@app.route('/create_event', methods=['GET','POST'])
def create_event():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    owner_id = session['user']['id']
    clubs = dbmgr.find_club_by_owner(owner_id)

    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('time')
        category = request.form.get('category')
        description = request.form.get('description')
        date = request.form.get('date')
        time =  request.form.get('time')
        
        club_id = int(request.form.get('club_id'))

        if not club_id:
            flash("Please select a club", "danger")
            return redirect(url_for(create_event))

        event_dict = {
            "name": name,
            "description": description,
            "category": category,
            "date": date,
            "time": time
        }

        success, result = event_controller.create_event(event_dict, club_id, owner_id)
        
        if success:
            flash("Event created successfully!", "success")
            return redirect(url_for('event_dashboard_user'))
        else:
            flash(result, "danger")
            return redirect(url_for('create_event'))
        
    return render_template('create-event.html', user=session['user'], clubs = clubs)

@app.route('/homepage')
def homepage():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    return render_template('homepage.html', user=session['user'])

@app.route('/event_dashboard_user')
def event_dashboard_user():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    return render_template('event-dashboard-officer.html', user=session['user'])

@app.route('/edit_event', methods=['GET','POST'])
def edit_event():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    owner_id = session['user']['id']
    clubs = dbmgr.find_event_by_owner(owner_id)

    if request.method == 'POST':
        delete_flag = request.form.get('delete_event') == '1'
        event_id = int(request.form.get('club_id'))
        if delete_flag:
            event_controller.delete_event(event_id, owner_id)
            flash("Event deleted successfully", "success")
            return redirect(url_for('event_dashboard_user'))

        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        date = request.form.get('date')
        time =  request.form.get('time')
        
        event_id = int(request.form.get('club_id'))

        if not event_id:
            flash("Please select a event", "danger")
            return redirect(url_for(edit_event))

        event_dict = {
            "name": name,
            "description": description,
            "category": category,
            "date": date,
            "time": time
        }

        success, result = event_controller.edit_event(event_id, event_dict, owner_id)
        
        if success:
            flash("Event created successfully!", "success")
            return redirect(url_for('event_dashboard_user'))
        else:
            flash(result, "danger")
            return redirect(url_for('edit_event'))

    return render_template("edit-event.html", user=session['user'], clubs = clubs)

if __name__ == "__main__":
    app.run(debug=True)