from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> Welcome to CoreFizik Fitness </h1>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        
        username_or_email = request.form.get("username").lower()
        password = request.form.get("password")

        messages = []

        if not username_or_email:
            messages.append(("danger", "Username or email is required"))

        elif not password:
            messages.append(("danger", "Password is required"))

        if not messages:
            user_row = db.execute("SELECT id, username, hashed_password FROM users WHERE username = :user_id OR user_email = :user_or_email LIMIT 1", user_or_email=username_or_email)

            if len(user_row) != 1 or not check_password_hash(user_row[0]["hashed_password"], password):
                messages.append(("danger", "Invalid username, email, and/or password"))

        if messages:
            for error in messages:
                flash(error)
            return render_template("login.html", messages=messages, user_or_email=user_or_email)

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
       
        username = request.form.get("username").lower()
        email = request.form.get("email").lower()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        messages = []

        existing_username_rows = check_user_by_username(db, username)

        if existing_username_rows:
            messages.append(("danger", "Username already taken."))

        validate_username(username, messages)

        validate_existing_email(db, email, messages)

        validate_email(email, messages)

        validate_password(password, messages)

        validate_confirmation_password(password, confirmation, messages)

        if messages:
         
            for error in messages:
                flash(error)
            return render_template("register.html", messages=messages, username=username, email=email)
        else:
            new_user_rows = register_user(db, username, email, password)

            if not new_user_rows:
                messages.append(("danger", "An error occurred while creating your account. Please try again."))
            else:
                new_user_db = db.execute("SELECT id, username FROM users WHERE username = ?", username)[0]

                if new_user_db:
                    session["user_id"] = new_user_db["id"]
                    session["user_username"] = new_user_db["username"]

                    messages.append(("success", "Account successfully created."))

                    flash(messages[-1])

                    return redirect("/")

    else:
        return render_template("register.html")

@app.route('/workouts')
def workouts():
    page = int(request.args.get('page', 1))
    selected_category = request.args.get('category')

    workouts = get_workouts(db, selected_category, page, WORKOUTS_PER_PAGE)

    total_workouts = get_total_workouts(db, selected_category)
   
    total_pages = (total_workouts + WORKOUTS_PER_PAGE - 1) // WORKOUTS_PER_PAGE

    all_categories = db.execute("SELECT DISTINCT category FROM workouts")

    categories = [category['category'] for category in all_categories]

    workout_data = []
    for workout in workouts:
        workout_data.append({
            'name': workout['name'],
            'description': workout['description'],
            'image_path': workout['image_path'],
            'category': workout['category']
        })

    return render_template('workouts.html')
