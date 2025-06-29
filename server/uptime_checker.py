import requests
from urllib.parse import urlparse
from models import db, Site, Status
from datetime import datetime, timezone, timedelta
from sqlalchemy import desc

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
DEFAULT_TIMEOUT = 15

def check_site_status(raw_url):
    url = raw_url
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url

    is_up = False
    response_time_ms = None
    error_message = None
    new_url_after_redirect = None

    start_time = datetime.now(timezone.utc)
    try:
        r = requests.get(url, timeout=DEFAULT_TIMEOUT, allow_redirects=True, headers=REQUEST_HEADERS)
        end_time = datetime.now(timezone.utc)
        response_time_ms = int((end_time - start_time).total_seconds() * 1000)

        is_up = r.status_code < 400
        if not is_up:
            error_message = f"HTTP Status Code: {r.status_code}"
        
        if url.rstrip('/') != r.url.rstrip('/') and urlparse(url).netloc == urlparse(r.url).netloc:
            new_url_after_redirect = r.url.rstrip('/')

    except requests.exceptions.Timeout:
        error_message = f"Request timed out after {DEFAULT_TIMEOUT} seconds."
    except requests.exceptions.ConnectionError as e:
        error_message = f"Connection Error: {e}"
    except requests.exceptions.RequestException as e:
        error_message = f"Request Exception: {e}"
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
    
    return is_up, response_time_ms, error_message, new_url_after_redirect

def check_sites(app):
    with app.app_context():
        print(f"Starting periodic uptime check at {datetime.now(timezone.utc)}")
        sites = Site.query.all()
        if not sites:
            print("No sites configured to check.")
            return

        for site in sites:
            is_up, response_time_ms, error_message, new_url = check_site_status(site.url)
            
            if new_url:
                site.url = new_url
                print(f"Updated URL for {site.user.username}'s site: {site.url} -> {new_url}")

            status = Status(site=site, is_up=is_up, response_time_ms=response_time_ms, error_message=error_message)
            db.session.add(status)

            site.is_up = is_up
            site.last_checked = datetime.now(timezone.utc)

            if not is_up:
                now = datetime.now(timezone.utc)
                last_alert = site.last_alert_time
                if last_alert and last_alert.tzinfo is None:
                    last_alert = last_alert.replace(tzinfo=timezone.utc)
                
                if (not last_alert) or (now - last_alert > timedelta(hours=1)):
                    print(f"🚨 ALERT: {site.url} is DOWN! Reason: {error_message}")
                    site.last_alert_time = now
            else:
                site.last_alert_time = None

            db.session.commit()
            print(f"[{datetime.now()}] Checked {site.url} - {'UP' if is_up else 'DOWN'}. Details: {error_message if error_message else f'Response Time: {response_time_ms}ms'}")

        MAX_STATUS_PER_SITE = 50
        print(f"Cleaning up old status records (keeping {MAX_STATUS_PER_SITE} per site)...")
        for site in Site.query.all():
            excess_statuses = Status.query.filter_by(site_id=site.id)\
                                    .order_by(Status.timestamp.desc())\
                                    .offset(MAX_STATUS_PER_SITE).all()
            for old_status in excess_statuses:
                db.session.delete(old_status)
        db.session.commit()
        print("Cleanup complete.")

if __name__ == '__main__':
    from app import app 
    with app.app_context():
        check_sites(app)
