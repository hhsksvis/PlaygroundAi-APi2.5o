from flask import Flask
from routes import register_routes
from config import DEFAULT_HOST, DEFAULT_PORT
from utils import find_free_port
import sys

def create_app():
    app = Flask(__name__)
    register_routes(app)
    return app

def run_server(host=DEFAULT_HOST, start_port=DEFAULT_PORT):
    app = create_app()
    port = find_free_port(start_port)
    
    if port is None:
        print(f"Could not find a free port after trying {start_port} through {start_port + 9}")
        sys.exit(1)

    print(f"Starting server on port {port}")
    try:
        app.run(host=host, port=port, debug=True)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run_server()