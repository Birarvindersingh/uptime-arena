import requests
from models import db, Site, Status
from app import app
from datetime import datetime, timezone, timedelta

def check_sites():
    with app.app_context():
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        sites = Site.query.all()
        for site in sites:
            try:
                r = requests.get(site.url, timeout=5)
                is_up = 200 <= r.status_code < 400
            except Exception:
                is_up = False

            status = Status(site=site, is_up=is_up)
            db.session.add(status)

            site.is_up = is_up
            site.last_checked = datetime.now(timezone.utc)

            if not is_up:
                now = datetime.now(timezone.utc)
                last_alert = site.last_alert_time
                if last_alert and last_alert.tzinfo is None:
                    last_alert = last_alert.replace(tzinfo=timezone.utc)
                if (not site.last_alert_time) or (now - last_alert > timedelta(hours=1)):
                    print(f"🚨 ALERT: {site.url} is DOWN! (No alert sent in last hour)")
                    site.last_alert_time = now

            db.session.commit()
            print(f"[{datetime.now()}] Checked {site.url} - {'UP' if is_up else 'DOWN'}")

if __name__ == '__main__':
    check_sites()
