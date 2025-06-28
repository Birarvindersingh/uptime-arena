import requests
from urllib.parse import urlparse
from models import db, Site, Status
from app import app
from datetime import datetime, timezone, timedelta
from sqlalchemy import desc

def check_site_status(raw_url):
    url = raw_url
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        is_up = r.status_code < 400
    except Exception:
        is_up = False
    return is_up

def check_sites():
    with app.app_context():
        sites = Site.query.all()
        for site in sites:
            is_up = check_site_status(site.url)
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
                    site.last_alert_time = now
            db.session.commit()

        MAX_STATUS_PER_SITE = 50
        for site in Site.query.all():
            excess_statuses = Status.query.filter_by(site_id=site.id).order_by(desc(Status.timestamp)).offset(MAX_STATUS_PER_SITE).all()
            for old_status in excess_statuses:
                db.session.delete(old_status)
        db.session.commit()

if __name__ == '__main__':
    check_sites()
