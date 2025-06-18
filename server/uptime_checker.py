import requests
from models import db, Site, Status
from app import app
from datetime import datetime, timezone, timedelta

def check_sites():
    with app.app_context():
        sites = Site.query.all()
        for site in sites:
            try:
                r = requests.get(site.url, timeout=5)
                is_up = r.status_code == 200
            except Exception:
                is_up = False

            status = Status(site=site, is_up=is_up)
            db.session.add(status)

            site.is_up = is_up
            site.last_checked = datetime.now(timezone.utc)

            if not is_up:
                now = datetime.now(timezone.utc)
                if (not site.last_alert_time) or (now - site.last_alert_time > timedelta(hours=1)):
                    print(f"🚨 ALERT: {site.url} is DOWN! (No alert sent in last hour)")
                    
                    site.last_alert_time = now

            db.session.commit()
            print(f"[{datetime.now()}] Checked {site.url} - {'UP' if is_up else 'DOWN'}")

if __name__ == '__main__':
    check_sites()