"""Songs microservice - Flask REST API backed by MongoDB (IBM Back-End Development Capstone)."""
from flask import Flask, jsonify, request, abort
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["songsdb"]
songs = db["songs"]


def _serialize(doc):
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


@app.route("/health", methods=["GET"])
def health():
    client.admin.command("ping")
    return jsonify({"status": "OK", "db": "connected"}), 200


@app.route("/song", methods=["GET"])
def list_songs():
    return jsonify([_serialize(d) for d in songs.find()]), 200


@app.route("/song", methods=["POST"])
def create_song():
    data = request.get_json(force=True, silent=True) or {}
    if "title" not in data or "artist" not in data:
        return jsonify({"error": "title and artist are required"}), 400
    res = songs.insert_one({"title": data["title"], "artist": data["artist"]})
    return jsonify(_serialize(songs.find_one({"_id": res.inserted_id}))), 201


@app.route("/song/<song_id>", methods=["GET"])
def get_song(song_id):
    try:
        doc = songs.find_one({"_id": ObjectId(song_id)})
    except Exception:
        abort(400)
    if doc is None:
        abort(404)
    return jsonify(_serialize(doc)), 200


@app.route("/song/<song_id>", methods=["PUT"])
def update_song(song_id):
    data = request.get_json(force=True, silent=True) or {}
    try:
        res = songs.update_one(
            {"_id": ObjectId(song_id)},
            {"$set": {k: v for k, v in data.items() if k in ("title", "artist")}},
        )
    except Exception:
        abort(400)
    if res.matched_count == 0:
        abort(404)
    return jsonify(_serialize(songs.find_one({"_id": ObjectId(song_id)}))), 200


@app.route("/song/<song_id>", methods=["DELETE"])
def delete_song(song_id):
    try:
        res = songs.delete_one({"_id": ObjectId(song_id)})
    except Exception:
        abort(400)
    if res.deleted_count == 0:
        abort(404)
    return jsonify({"deleted": song_id}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
