from flask import request, jsonify
from threading import Thread
from models import create_model
from storage import (
    load_users, save_users, load_history, save_history,
    generate_title, format_history
)
from utils import generate_token, send_to_webhook

def register_routes(app):
    @app.route('/username', methods=['GET'])
    def username():
        username = request.args.get('username')
        token = request.args.get('token')

        if username:
            if any(name in username.lower() for name in ["tlodev", "tlo"]):
                return jsonify({"error": "Invalid username"}), 400

            users = load_users()
            if username in users.values():
                return jsonify({"error": "Username already exists"}), 400

            token = generate_token()
            users[token] = username
            save_users(users)

            return jsonify({"token": token, "username": username})

        elif token:
            users = load_users()
            username = users.get(token)
            return jsonify({"username": username}) if username else (jsonify({"error": "Invalid token"}), 401)
        
        return jsonify({"error": "Either 'username' or 'token' is required"}), 400

    @app.route('/chat', methods=['GET'])
    def chat():
        user_message = request.args.get('message')
        section = request.args.get('section')
        token = request.args.get('token')
        use_history = request.args.get('history', 'true').lower() == 'true'

        if not user_message or not token:
            return jsonify({"error": "Missing required parameters"}), 400

        if use_history and not section:
            return jsonify({"error": "'section' is required when 'history' is enabled"}), 400

        try:
            section = int(section) if use_history else None
        except ValueError:
            return jsonify({"error": "Invalid section number"}), 400

        users = load_users()
        if token not in users:
            return jsonify({"error": "Invalid token"}), 401

        try:
            username = users.get(token)
            model = create_model(username)
            history, title = load_history(token, section) if use_history else ([], None)

            formatted_history = []
            if use_history:
                for item in history:
                    formatted_history.append({"role": "user", "parts": [item["user"]]})
                    formatted_history.append({"role": "model", "parts": [item["bot"]]})

            chat_session = model.start_chat(history=formatted_history)
            response = chat_session.send_message(user_message)
            response_text = response.text

            if use_history:
                history.append({"user": user_message, "bot": response_text})
                if not title:
                    title = generate_title(history[0]['user'])
                save_history(token, history, section, title)

            Thread(target=send_to_webhook, 
                   args=(token, request.headers.get('User-Agent', "0")), 
                   daemon=True).start()

            return jsonify({"response": response_text})

        except Exception as e:
            print(f"Error in chat processing: {str(e)}")
            return jsonify({"error": "An error occurred processing your request"}), 500

    @app.route('/conversation', methods=['GET'])
    def conversation():
        token = request.args.get('token')
        section = request.args.get('section')

        if not token or not section:
            return jsonify({"error": "Both 'token' and 'section' are required"}), 400

        try:
            section = int(section)
        except ValueError:
            return jsonify({"error": "Invalid section number"}), 400

        users = load_users()
        if token not in users:
            return jsonify({"error": "Invalid token"}), 401

        history, title = load_history(token, section)
        username = users.get(token)
        conversation_history = format_history(json.dumps(history), username=username)

        return jsonify({"conversation": conversation_history, "title": title})

    @app.route('/history', methods=['GET'])
    def history():
        token = request.args.get('token')
        section = request.args.get('section')
        delete = request.args.get('delete')

        if not token or not section:
            return jsonify({"error": "Both 'token' and 'section' are required"}), 400

        try:
            section = int(section)
        except ValueError:
            return jsonify({"error": "Invalid section number"}), 400

        users = load_users()
        if token not in users:
            return jsonify({"error": "Invalid token"}), 401

        if delete == 'true':
            try:
                history_file = f"history_{token}_{section}.json"
                if os.path.exists(history_file):
                    os.remove(history_file)
                    return jsonify({"message": f"History for section {section} deleted successfully"})
                return jsonify({"error": f"No history found for section {section}"})
            except Exception as e:
                return jsonify({"error": f"Failed to delete history: {str(e)}"}), 500

        history, title = load_history(token, section)
        return jsonify({"history": history, "title": title})