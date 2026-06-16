from flask import Flask, request, render_template, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import Counter
from analyzer import analyze_ticket
import csv
import io
import sqlite3
import os

app = Flask(__name__)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tickets.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(100), nullable=False)
    reply = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def add_status_column_if_missing():
    db_path = os.path.join("instance", "tickets.db")

    if not os.path.exists(db_path):
        return

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(ticket)")
    columns = [column[1] for column in cursor.fetchall()]

    if "status" not in columns:
        cursor.execute("ALTER TABLE ticket ADD COLUMN status TEXT DEFAULT 'Open'")
        connection.commit()

    connection.close()


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    ticket_message = ""
    error_message = ""

    if request.method == "POST":
        ticket_message = request.form["ticket_message"].strip()

        if ticket_message == "":
            error_message = "Please enter a ticket message before analyzing."
        else:
            result = analyze_ticket(ticket_message)

            new_ticket = Ticket(
                message=ticket_message,
                category=result["category"],
                priority=result["priority"],
                team=result["team"],
                reply=result["reply"],
                status="Open"
            )

            db.session.add(new_ticket)
            db.session.commit()

    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()

    total_tickets = Ticket.query.count()
    urgent_tickets = Ticket.query.filter_by(priority="Urgent").count()
    high_tickets = Ticket.query.filter_by(priority="High").count()

    return render_template(
        "index.html",
        result=result,
        ticket_message=ticket_message,
        recent_tickets=recent_tickets,
        total_tickets=total_tickets,
        urgent_tickets=urgent_tickets,
        high_tickets=high_tickets,
        error_message=error_message
    )


@app.route("/dashboard")
def dashboard():
    search_query = request.args.get("search", "")
    priority_filter = request.args.get("priority", "")

    query = Ticket.query

    if search_query:
        query = query.filter(Ticket.message.ilike(f"%{search_query}%"))

    if priority_filter:
        query = query.filter_by(priority=priority_filter)

    filtered_tickets = query.order_by(Ticket.created_at.desc()).all()
    recent_tickets = filtered_tickets[:10]

    all_tickets = Ticket.query.all()

    total_tickets = Ticket.query.count()
    urgent_tickets = Ticket.query.filter_by(priority="Urgent").count()
    high_tickets = Ticket.query.filter_by(priority="High").count()
    medium_tickets = Ticket.query.filter_by(priority="Medium").count()
    low_tickets = Ticket.query.filter_by(priority="Low").count()

    open_tickets = Ticket.query.filter_by(status="Open").count()
    in_progress_tickets = Ticket.query.filter_by(status="In Progress").count()
    resolved_tickets = Ticket.query.filter_by(status="Resolved").count()

    priority_counts = {
        "Urgent": urgent_tickets,
        "High": high_tickets,
        "Medium": medium_tickets,
        "Low": low_tickets
    }

    category_counts = Counter(ticket.category for ticket in all_tickets)

    max_priority_count = max(priority_counts.values()) if priority_counts else 1
    max_category_count = max(category_counts.values()) if category_counts else 1

    return render_template(
        "dashboard.html",
        recent_tickets=recent_tickets,
        total_tickets=total_tickets,
        urgent_tickets=urgent_tickets,
        high_tickets=high_tickets,
        medium_tickets=medium_tickets,
        low_tickets=low_tickets,
        open_tickets=open_tickets,
        in_progress_tickets=in_progress_tickets,
        resolved_tickets=resolved_tickets,
        priority_counts=priority_counts,
        category_counts=category_counts,
        max_priority_count=max_priority_count,
        max_category_count=max_category_count,
        search_query=search_query,
        priority_filter=priority_filter
    )


@app.route("/update-status/<int:ticket_id>/<status>")
def update_status(ticket_id, status):
    ticket = Ticket.query.get_or_404(ticket_id)

    if status in ["Open", "In Progress", "Resolved"]:
        ticket.status = status
        db.session.commit()

    return redirect(url_for("dashboard"))


@app.route("/delete-ticket/<int:ticket_id>")
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    db.session.delete(ticket)
    db.session.commit()

    return redirect(url_for("dashboard"))


@app.route("/export")
def export_tickets():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Message",
        "Category",
        "Priority",
        "Suggested Team",
        "Suggested Reply",
        "Status",
        "Created At"
    ])

    for ticket in tickets:
        writer.writerow([
            ticket.id,
            ticket.message,
            ticket.category,
            ticket.priority,
            ticket.team,
            ticket.reply,
            ticket.status,
            ticket.created_at
        ])

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=smartdesk_tickets.csv"

    return response


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        add_status_column_if_missing()

    app.run(debug=True)
