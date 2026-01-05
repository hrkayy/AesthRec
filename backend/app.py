from flask import Flask, request, jsonify, send_from_directory
from aesthetics import AESTHETIC_CATALOGUE
from model import analyze_image
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    image_bytes = image.read()

    analysis = analyze_image(image_bytes, AESTHETIC_CATALOGUE)

    return jsonify({
        "total_aesthetics": len(AESTHETIC_CATALOGUE),
        "accuracy": analysis["accuracy"],
        "results": analysis["results"]
    })

@app.route("/")
def serve_frontend():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

if __name__ == "__main__":
    app.run(debug=True)
