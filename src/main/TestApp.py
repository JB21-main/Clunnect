from dotenv import load_dotenv
from datetime import datetime, date
import calendar
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from Controllers.AuthController import AuthController
from Controllers.ClubController import ClubController
from Controllers.EventController import EventController
from Controllers.JoinClubController import JoinClubController
from Controllers.SearchController import SearchController       
from Controllers.CalendarController import CalendarController
from Controllers.AccountController import AccountController
from Controllers.FacultyController import FacultyController
from Services.DBmgr import DBmgr
from Data.Level import Level
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
calendar_controller = CalendarController(dbmgr=dbmgr)
faculty_controller = FacultyController(dbmgr=dbmgr)  
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
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))

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
    
@app.route('/search')
def search_page():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    return render_template('search.html')

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

@app.route("/club/<int:club_id>")
def club_page(club_id):
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))

    return render_template("club_page.html", club_id=club_id)

@app.route("/api/club/<int:club_id>")
def api_club_page(club_id):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    club = dbmgr.get_club(club_id)
    events = dbmgr.get_event_by_club(club_id)
    if not club:
        return jsonify({"error": "Club not found"}), 404

    return jsonify({
    "id": club["id"],
    "name": club["name"],
    "description": club["description"],
    "meeting_day": club["meeting_day"],
    "meeting_time": club["meeting_time"],
    "events": events
})

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

@app.route('/account_settings', methods=['GET','POST'])
def account_settings():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    return render_template("account-settings.html", user=session['user'])

@app.route('/change_login_info', methods=['GET','POST'])
def change_login_info():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    return render_template("change-login-info.html", user=session['user'])

#not added
@app.route('/manage_preferences', methods=['GET','POST'])
def manage_preferences():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    return render_template("account-settings.html", user=session['user'])

#not functioning currently
@app.route('/profile_page', methods=['GET','POST'])
def profile_page():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    return render_template("profile.html", user=session['user'])

@app.route('/faculty_settings', methods=['GET', 'POST'])
def faculty_settings():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))

    if session['user']['level'] != "faculty":
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('homepage'))

    # types username
    if request.method == 'POST':
        username = request.form.get('username')

        # Look up user by username
        result = dbmgr.supabase.table("users") \
            .select("*") \
            .eq("username", username) \
            .execute()

        if not result.data:
            flash("No user found with that username.", "danger")
            return redirect(url_for('faculty_settings'))

        user_id = result.data[0]["id"]

        # Set permission level to faculty
        success, out = faculty_controller.set_user_permission(
            int(user_id),
            Level.FACULTY
        )

        if success:
            flash(f"{username} is now a faculty user", "success")
        else:
            flash(out, "danger")

        return redirect(url_for('faculty_settings'))

    return render_template('faculty-settings.html')

#calendar
@app.route('/calendar', endpoint='calendar')
def calendar_page():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))

    user_id = session['user']['id']

    month = request.args.get("month", type=int) or datetime.now().month
    year = request.args.get("year", type=int) or datetime.now().year

    # load user events
    success, events = calendar_controller.load_calendar_view(user_id)

    # calendar grid for each month
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)

    calendar_cells = []
    for d in month_days:
        if d == 0:
            calendar_cells.append({"empty": True})
        else:
            # checks if day has event
            has_event = any(
                e["date"] == f"{year}-{month:02d}-{d:02d}"
                for e in events
            )
            calendar_cells.append({
                "empty": False,
                "day": d,
                "has_event": has_event
            })

    month_name = calendar.month_name[month]

    return render_template(
        "calendar.html",
        month=month,
        year=year,
        month_name=month_name,
        calendar=calendar_cells,
        events=events
    )

if __name__ == "__main__":
    app.run(debug=True)