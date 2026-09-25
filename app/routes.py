from datetime import date, datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort

from app import db
from app.models import Application, Status

bp = Blueprint("main", __name__)

# Allowed status transitions: current -> [allowed next states]
TRANSITIONS = {
    Status.APPLIED: [Status.INTERVIEW, Status.REJECTED],
    Status.INTERVIEW: [Status.OFFER, Status.REJECTED],
    Status.OFFER: [],
    Status.REJECTED: [],
}


def valid_transition(current: Status, new: Status) -> bool:
    if current == new:
        return True
    return new in TRANSITIONS.get(current, [])


def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


# ---------- Web UI routes ----------

@bp.route("/")
def index():
    status_filter = request.args.get("status")
    query = Application.query
    if status_filter:
        query = query.filter_by(status=Status[status_filter])
    applications = query.order_by(Application.applied_date.desc()).all()

    soon = date.today() + timedelta(days=3)
    reminder_ids = {
        a.id for a in Application.query.filter(
            Application.reminder_date.isnot(None),
            Application.reminder_date <= soon,
        ).all()
    }

    return render_template(
        "index.html",
        applications=applications,
        statuses=Status,
        status_filter=status_filter,
        reminder_ids=reminder_ids,
    )


@bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        application = Application(
            company_name=request.form["company_name"],
            role=request.form.get("role"),
            applied_date=parse_date(request.form.get("applied_date")) or date.today(),
            reminder_date=parse_date(request.form.get("reminder_date")),
            notes=request.form.get("notes"),
        )
        db.session.add(application)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("form.html", application=None, statuses=Status)


@bp.route("/edit/<int:app_id>", methods=["GET", "POST"])
def edit(app_id):
    application = Application.query.get_or_404(app_id)

    if request.method == "POST":
        new_status = Status[request.form["status"]]
        if not valid_transition(application.status, new_status):
            return render_template(
                "form.html",
                application=application,
                statuses=Status,
                error=f"Cannot move from {application.status.value} to {new_status.value}",
            ), 400

        application.company_name = request.form["company_name"]
        application.role = request.form.get("role")
        application.status = new_status
        application.applied_date = parse_date(request.form.get("applied_date")) or application.applied_date
        application.reminder_date = parse_date(request.form.get("reminder_date"))
        application.notes = request.form.get("notes")
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("form.html", application=application, statuses=Status)


@bp.route("/delete/<int:app_id>", methods=["POST"])
def delete(app_id):
    application = Application.query.get_or_404(app_id)
    db.session.delete(application)
    db.session.commit()
    return redirect(url_for("main.index"))


# ---------- JSON API routes ----------

@bp.route("/api/applications", methods=["GET"])
def api_get_all():
    applications = Application.query.order_by(Application.applied_date.desc()).all()
    return jsonify([a.to_dict() for a in applications])


@bp.route("/api/applications/<int:app_id>", methods=["GET"])
def api_get_one(app_id):
    application = Application.query.get_or_404(app_id)
    return jsonify(application.to_dict())


@bp.route("/api/applications", methods=["POST"])
def api_create():
    data = request.get_json(force=True)
    if not data or not data.get("company_name"):
        abort(400, "company_name is required")

    application = Application(
        company_name=data["company_name"],
        role=data.get("role"),
        applied_date=parse_date(data.get("applied_date")) or date.today(),
        reminder_date=parse_date(data.get("reminder_date")),
        notes=data.get("notes"),
    )
    db.session.add(application)
    db.session.commit()
    return jsonify(application.to_dict()), 201


@bp.route("/api/applications/<int:app_id>", methods=["PUT"])
def api_update(app_id):
    application = Application.query.get_or_404(app_id)
    data = request.get_json(force=True) or {}

    if "status" in data:
        new_status = Status[data["status"]]
        if not valid_transition(application.status, new_status):
            return jsonify({"error": "invalid status transition"}), 400
        application.status = new_status

    for field in ("company_name", "role", "notes"):
        if field in data:
            setattr(application, field, data[field])

    if "applied_date" in data:
        application.applied_date = parse_date(data["applied_date"])
    if "reminder_date" in data:
        application.reminder_date = parse_date(data["reminder_date"])

    db.session.commit()
    return jsonify(application.to_dict())


@bp.route("/api/applications/<int:app_id>", methods=["DELETE"])
def api_delete(app_id):
    application = Application.query.get_or_404(app_id)
    db.session.delete(application)
    db.session.commit()
    return "", 204


@bp.route("/api/applications/reminders", methods=["GET"])
def api_reminders():
    soon = date.today() + timedelta(days=3)
    applications = Application.query.filter(
        Application.reminder_date.isnot(None),
        Application.reminder_date <= soon,
    ).all()
    return jsonify([a.to_dict() for a in applications])
