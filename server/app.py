from flask import Flask, jsonify, request
from models import db, User, Site, Status
import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(config)
db.init_app(app)

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()

@app.route('/')
def home():
    return "Hello from Uptime Arena!"

@app.route('/api/sites', methods=['GET'])
def get_sites():
    sites = Site.query.all()
    data = []
    for site in sites:
        uptimes = [s.is_up for s in site.statuses]
        avg = round((sum(uptimes) / len(uptimes)) * 100, 2) if uptimes else 0
        data.append({
            'url': site.url,
            'user': site.user.username,
            'uptime': avg
        })
    return jsonify(data)

@app.route('/api/sites', methods=['POST'])
def add_site():
    data = request.json
    username = data['username']
    url = data['url']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    site = Site(url=url, user=user)
    db.session.add(site)
    db.session.commit()
    return jsonify({'message': 'Site added'}), 201

if __name__ == "__main__":
    app.run(debug=True)