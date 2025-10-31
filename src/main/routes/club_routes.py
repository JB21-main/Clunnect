from flask import Blueprint, request, jsonify
from main.db.dbmgr import DBMgr

club_bp = Blueprint("club", __name__)
db = DBMgr()

# UC1: Create Club
@club_bp.route("/clubs", methods=["POST"])
def create_club():
    data = request.get_json()
    club_name = data.get("club_name")
    description = data.get("description")
    creator_id = data.get("creator_id")

    if not club_name or not creator_id:
        return jsonify({"error": "club_name and creator_id are required"}), 400

    result = db.create_club(club_name, description, creator_id)
    return jsonify(result), 201

# UC3: Join Club
@club_bp.route("/clubs/<int:club_id>/join", methods=["POST"])
def join_club(club_id):
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    result = db.join_club(user_id, club_id)
    return jsonify(result), 201
