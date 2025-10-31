from flask import Flask
from main.routes.club_routes import club_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprint
    app.register_blueprint(club_bp)

    # Define home route
    @app.route("/")
    def home():
        return "Server is running!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
