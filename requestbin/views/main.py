import urllib

from flask import (flash, make_response, redirect, render_template, request, 
                   session, url_for)
from flask_login import current_user

from requestbin import app, config, socketio
from requestbin.database import db


def update_recent_bins(name):
    """Track recently viewed bins in session (for backwards compatibility)"""
    if "recent" not in session:
        session["recent"] = []
    if name in session["recent"]:
        session["recent"].remove(name)
    session["recent"].insert(0, name)
    if len(session["recent"]) > 10:
        session["recent"] = session["recent"][:10]
    session.modified = True


def expand_recent_bins():
    """Get recent bins - user-specific if authenticated, empty for non-authenticated"""
    from requestbin import config
    recent = []
    
    # Check if storage backend has changed - if so, clear session bins
    current_backend = config.STORAGE_BACKEND
    if "backend" not in session or session.get("backend") != current_backend:
        session["backend"] = current_backend
        session["recent"] = []
        session.modified = True
    
    # Only show history for authenticated users
    if current_user.is_authenticated:
        try:
            user_bins = db.get_bins_by_owner(current_user.email)
            # Sort by created time, most recent first
            user_bins.sort(key=lambda x: x.created, reverse=True)
            # Limit to 10 most recent
            recent = user_bins[:10]
        except Exception as e:
            print(f"Error fetching user bins: {e}")   
            recent = []
    # For non-authenticated users, return empty list (no history shown)
    
    return recent


def _get_session_recent_bins():
    """Get bins from session history (fallback for non-authenticated users)"""
    if "recent" not in session:
        session["recent"] = []
    recent = []
    for name in session["recent"][:]:  # Create a copy to safely modify during iteration
        try:
            recent.append(db.lookup_bin(name))
        except (KeyError, Exception) as e:
            # Remove bins that can't be found or cause errors (e.g., backend switch)
            try:
                session["recent"].remove(name)
                session.modified = True
            except (ValueError, KeyError):
                pass
    return recent


@app.endpoint("views.home")
def home():
    return render_template("home.html", recent=expand_recent_bins())


@app.endpoint("views.bin")
def bin(name):
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return "Bin Not found\n", 404
    if request.query_string.decode() == "inspect":
        # Require authentication to view inspect page
        if not current_user.is_authenticated:
            flash("Please login to view bin details.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        if bin.private and session.get(bin.name) != bin.secret_key:
            return "Private bin\n", 403
        update_recent_bins(name)
        return render_template(
            "bin.html", bin=bin, base_url=request.scheme + "://" + request.host,
            max_requests=config.MAX_REQUESTS, bin_ttl_hours=config.BIN_TTL // 3600
        )
    else:
        db.create_request(bin, request)
        # Emit WebSocket event for real-time update
        socketio.emit('bin_updated', {
            'bin_name': name,
            'request_count': len(bin.requests) if hasattr(bin, 'requests') and bin.requests else 1
        }, room=name)
        resp = make_response("ok\n")
        return resp


@app.endpoint("views.docs")
def docs(name):
    doc = db.lookup_doc(name)
    if doc:
        return render_template(
            "doc.html",
            content=doc["content"],
            title=doc["title"],
            recent=expand_recent_bins(),
        )
    else:
        return "Not found", 404


@app.endpoint("views.about")
def about():
    return render_template("about.html", recent=expand_recent_bins())
