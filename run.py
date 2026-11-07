from dotenv import load_dotenv  # Load environment variables from .env file.
load_dotenv()                    # Must be called BEFORE create_app so config.py picks up the .env values.

from app import create_app   # Imports the function that creates and configures the Flask application.

app = create_app()            # Creates the Flask application instance using the application factory.

if __name__ == "__main__":     # Checks if this file is being run directly (not imported).
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=True, port=port)
    # Starts the Flask development server with debug mode enabled.
    # Debug mode automatically reloads changes and shows detailed errors.