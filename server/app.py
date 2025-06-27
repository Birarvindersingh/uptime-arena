from flask import Flask, jsonify, request, send_from_directory
from models import db, User, Site, Status
import config, os, re
from flask_cors import CORS

app = Flask(__name__, static_folder="../client/dist", static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(config)
db.init_app(app)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    file_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

def normalize_url(raw_url):
    url = raw_url.strip().lower()
    if url.startswith("www."):
        url = url[4:]
    return url

@app.route("/api/sites", methods=["GET"])
def get_sites():
    sites = Site.query.all()
    data = []
    for site in sites:
        uptimes = [status.is_up for status in site.statuses]
        avg_uptime = round((sum(uptimes) / len(uptimes)) * 100, 2) if uptimes else 0
        data.append({
            "url": site.url,
            "user": site.user.username if site.user else None,
            "uptime": avg_uptime
        })
    return jsonify(data)

@app.route("/api/sites", methods=["POST"])
def add_site():
    data = request.get_json()
    username = data.get("username", "").strip()
    raw_url = data.get("url", "").strip()

    if not username or not raw_url:
        return jsonify({"error": "Missing username or URL"}), 400

    normalized_url = normalize_url(raw_url)

    if not re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", normalized_url):
        return jsonify({"error": "Invalid domain format"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    existing = Site.query.filter_by(user_id=user.id, url=normalized_url).first()
    if existing:
        return jsonify({"error": "Site already exists"}), 409

    new_site = Site(user_id=user.id, url=normalized_url)
    db.session.add(new_site)
    db.session.commit()

    return jsonify({"message": "Site added successfully"}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
