# logging-service — Flask app (not FastAPI — intentional, see docs/specs.md)
#
# Run with:   flask run --port 8006
# Or:         python -m flask --app app.main run --port 8006
#
# YOUR TASK: implement the four consent endpoints and the log deletion endpoint.
# The response shapes are in docs/api-contracts.md.

import os
import threading
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from app.models import ActivityLog, Consent, db

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///./logging.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Start the RabbitMQ consumer in a background thread
    from app.consumer import start_consumer
    threading.Thread(target=start_consumer, args=(app,), daemon=True).start()


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "logging-service"})


# ---------------------------------------------------------------------------
# YOUR TASK — implement the five endpoints below
# ---------------------------------------------------------------------------

@app.post("/v1/consent/<user_id>")
def set_consent(user_id):
    """
    Record or update a user's GDPR consent decision.

    Request body: { "granted": true }

    Steps:
    1. Parse request.get_json() to get "granted" (bool)
    2. Look up or create a Consent row for user_id
    3. Set granted and updated_at, then db.session.commit()
    4. Return 200 with { "user_id", "granted", "updated_at" }
    """
    data = request.get_json()
    granted = data.get("granted", False)
    record = Consent.query.filter_by(user_id=user_id).first()
    if record is None:
        record = Consent(user_id=user_id, granted=granted)
        db.session.add(record)
    else:
        record.granted = granted
        record.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({
        "user_id": record.user_id,
        "granted": record.granted,
        "updated_at": record.updated_at.isoformat(),
    })


@app.get("/v1/consent/<user_id>")
def get_consent(user_id):
    """
    Check a user's current consent status.

    Steps:
    1. Query Consent by user_id
    2. If not found → 404 with { "detail": "No consent record found" }
    3. Otherwise → 200 with { "user_id", "granted", "updated_at" }
    """
    record = Consent.query.filter_by(user_id=user_id).first()
    if record is None:
        return jsonify({"detail": "No consent record found"}), 404
    return jsonify({
        "user_id": record.user_id,
        "granted": record.granted,
        "updated_at": record.updated_at.isoformat(),
    })


@app.delete("/v1/consent/<user_id>")
def withdraw_consent(user_id):
    """
    Withdraw consent — sets granted to False (does not delete the record).

    Steps:
    1. Look up the Consent row; 404 if missing
    2. Set granted=False, update updated_at, commit
    3. Return 200 with { "user_id", "granted", "updated_at" }
    """
    record = Consent.query.filter_by(user_id=user_id).first()
    if record is None:
        return jsonify({"detail": "No consent record found"}), 404
    record.granted = False
    record.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({
        "user_id": record.user_id,
        "granted": record.granted,
        "updated_at": record.updated_at.isoformat(),
    })


@app.delete("/v1/logs/<user_id>")
def delete_logs(user_id):
    """
    GDPR right to erasure — permanently delete all log entries for a user.

    Steps:
    1. Delete all ActivityLog rows where user_id matches
    2. Commit
    3. Return 200 with { "user_id", "deleted_entries": <count> }
    """
    count = ActivityLog.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"user_id": user_id, "deleted_entries": count})


@app.get("/v1/logs/<user_id>")
def get_logs(user_id):
    """
    List all stored log entries for a user (for testing/verification).

    Returns: { "items": [...], "total": N }
    Each item: { "id", "user_id", "game_id", "action", "message", "created_at" }
    """
    logs = ActivityLog.query.filter_by(user_id=user_id).all()
    return jsonify({
        "items": [
            {
                "id": l.id,
                "user_id": l.user_id,
                "game_id": l.game_id,
                "action": l.action,
                "message": l.message,
                "created_at": l.created_at.isoformat(),
            }
            for l in logs
        ],
        "total": len(logs),
    })