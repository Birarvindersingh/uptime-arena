import requests
from urllib.parse import urlparse
from models import db, Site, Status
from app import app
from datetime import datetime, timezone, timedelta

def check_sites():
    with app.app_context():
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        sites = Site.query.all()
        for site in sites:
            url = site.url
            parsed = urlparse(url)
            if not parsed.scheme:
                url = "https://" + url

            try:
                r = requests.get(url, timeout=5, allow_redirects=True)
                is_up = r.status_code < 400
                final_url = r.url.rstrip('/')
                original_url = url.rstrip('/')
                if original_url != final_url:
                    site.url = final_url
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
                if (not last_alert) or (now - last_alert > timedelta(hours=1)):
                    print(f"🚨 ALERT: {site.url} is DOWN! (No alert sent in last hour)")
                    site.last_alert_time = now

            db.session.commit()
            print(f"[{datetime.now()}] Checked {site.url} - {'UP' if is_up else 'DOWN'}")

if __name__ == '__main__':
    check_sites()
