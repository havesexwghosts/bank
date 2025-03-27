from flask import Flask, render_template, request, redirect, url_for
from time import sleep
from database import Database

class MyApp:
    def __init__(self):
        # Initialize the Flask application and database connection
        self.app = Flask(__name__, template_folder="../frontend/templates")
        self.db = Database()  # Create a new instance of the Database class
        db = Database()  # Create another instance (unnecessary redundancy)
        db.init_db()  # Initialize the database (create tables if they don't exist)
        db.insert_sample_user()  # Insert a sample user into the database
        self.setup_routes()  # Register routes when an instance of MyApp is created

    def setup_routes(self): 
        # Home page route
        @self.app.route('/')
        def home():
            print("Watanabe Banking - Online")  # Print message when home route is accessed
            return render_template("home.html")  # Render the home page template
        
        # Login route
        @self.app.route('/login', methods=["POST", "GET"])
        def login():
            if request.method == 'GET':
                return render_template("login.html")  # Render login page when GET request is made
            
            elif request.method == 'POST':
                # Handle the login form submission
                name = request.form.get("name")  # Get the name from the form
                password = request.form.get("password")  # Get the password from the form

                # Check if the user exists in the database
                user = self.db.get_user_by_name(name)

                if user and user["password"] == str(password):  # Validate user credentials
                    balance = user["balance"]  # Get the user's balance
                    return redirect(url_for('account', name=name))  # Redirect to the account page if credentials are valid
                else:
                    return "Invalid Credentials, please try again."  # Return error if credentials are invalid
        
        # Signup route
        @self.app.route('/signup', methods=["POST", "GET"])
        def signup():
            if request.method == 'GET':
                return render_template("signup.html")  # Render signup page when GET request is made
            
            elif request.method == 'POST':
                # Handle the signup form submission
                name = str(request.form.get("name"))  # Get the name from the form
                password = str(request.form.get("password"))  # Get the password from the form

                # Check if the username already exists in the database
                if not self.db.user_exists(name):  # If the name does not exist
                    self.db.create_user(name=name, password=password, balance=0)  # Create a new user in the database
                    return redirect(url_for('login'))  # Redirect to the login page after successful signup
                else:
                    return "Name Unavailable"  # Return error if the username is already taken

        # Account page route
        @self.app.route('/account', methods=["POST", "GET"])
        def account():
            # This route is for displaying the user's account
            return render_template("account.html")  # Render the account page template
        
        # Transfer route
        @self.app.route('/transfer', methods=["POST", "GET"])
        def transfer():
            if request.method == "GET":
                # Fetch the 'name' and 'balance' from the URL query parameters
                name = request.args.get('name')  # Get the name from URL query
                balance = request.args.get('balance')  # Get the balance from URL query
                return render_template("transfer.html", name=name, balance=balance)  # Pass the name and balance to the transfer page
            
            if request.method == "POST":
                # Handle the transfer form submission
                pass  # Placeholder for the actual transfer logic (e.g., balance update)

    # Method to run the Flask app
    def run(self):
        self.app.run(debug=True)  # Start the Flask application with debugging enabled

# Create an instance of MyApp and run it when the script is executed
if __name__ == "__main__":
    app = MyApp()
    app.run()