from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import os
import traceback

app = Flask(__name__)

# ✅ Docker-safe Mongo configuration
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://mongo:27017/mongotask"
)

app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)
CORS(app)

@app.route("/api/tasks", methods=["GET"])
def get_all_tasks():
    try:
        tasks = mongo.db.tasks
        result = []

        for task in tasks.find():
            result.append({
                "_id": str(task.get("_id")),
                "title": task.get("title", "")
            })

        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "details": str(e)}), 500

@app.route("/api/task", methods=["POST"])
def add_task():
    try:
        tasks = mongo.db.tasks
        title = None
        if request.is_json:
            title = request.json.get("title")

        if not title:
            return jsonify({"status": "error", "details": "missing title"}), 400

        task_id = tasks.insert_one({"title": title}).inserted_id
        new_task = tasks.find_one({"_id": task_id})

        return jsonify({
            "result": {
                "_id": str(new_task.get("_id")),
                "title": new_task.get("title")
            }
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "details": str(e)}), 500

@app.route("/api/task/<id>", methods=["PUT"])
def update_task(id):
    try:
        tasks = mongo.db.tasks
        title = None
        if request.is_json:
            title = request.json.get("title")

        if title is None:
            return jsonify({"status": "error", "details": "missing title"}), 400

        tasks.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"title": title}}
        )

        updated_task = tasks.find_one({"_id": ObjectId(id)})

        return jsonify({
            "result": {
                "_id": str(updated_task.get("_id")),
                "title": updated_task.get("title")
            }
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "details": str(e)}), 500

@app.route("/api/task/<id>", methods=["DELETE"])
def delete_task(id):
    try:
        tasks = mongo.db.tasks
        result = tasks.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 1:
            return jsonify({"message": "record deleted"})
        else:
            return jsonify({"message": "no record found"}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "details": str(e)}), 500

@app.route("/health")
def health():
    try:
        mongo.db.list_collection_names()
        return jsonify({"status": "ok", "mongo": "connected"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "details": str(e)}), 500


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    traceback.print_exc()
    resp = jsonify({"status": "error", "details": str(error)})
    resp.status_code = 500
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
