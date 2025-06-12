from flask import Blueprint, request, jsonify, render_template
from backend.app.langchain.agent import run_agent_with_tools


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@chat_bp.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot interactions."""
    data = request.get_json()
    user_message = data.get("message")

    response = run_agent_with_tools(user_input=user_message)
    return jsonify({"response": response})
