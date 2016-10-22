from controllers.app import app
import controllers.handlers

if __name__ == "__main__":
    app.run(port=5000, debug=True)