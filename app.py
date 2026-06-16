from flask import Flask, request, render_template, Response, redirect, url_for
from analyzer import analyze_ticket
from datetime import datetime
from collections import Counter
import csv
import io
import os

app = Flask(__name__)

# In-memory ticket history for public demo.
# This avoids database errors on Render.
tickets = []
next_ticket_id = 1


@app.route("/", methods=["GET", "POST"])
def home():
    global next_ticket_id

    result = None
    ticket_message = ""
    error_message = ""

    if request.method == "POST":
        ticket_message = request.form.get("ticket_message", "").strip()

        if ticket_message == "":
            error_message = "Please enter a ticket message before analyzing."
        else:
            result = analyze_ticket(ticket_message)

            new_ticket = {
                "id": next_ticket_id,
                "message": ticket_message,
                "category": result.get("category", "Unknown"),
                "priority": result.get("priority", "Medium"),
                "team": result.get("team", "IT Service Desk"),
                "reply": result.get("reply", ""),
                "status": "Open",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            tickets.insert(0, new_ticket)
            next_ticket_id += 1

    recent_tickets = tickets[:5]

    total_tickets = len(tickets)
    urgent_tickets = sum(1 for ticket in tickets if ticket["priority"] == "Urgent")
    high_tickets = sum(1 for ticket in tickets if ticket["priority"] == "High")

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
    search_query = request.args.get("search", "").lower()
    priority_filter = request.args.get("priority", "")

    filtered_tickets = tickets

    if search_query:
        filtered_tickets = [
            ticket for ticket in filtered_tickets
            if search_query in ticket["message"].lower()
        ]

    if priority_filter:
        filtered_tickets = [
            ticket for ticket in filtered_tickets
            if ticket["priority"] == priority_filter
        ]

    recent_tickets = filtered_tickets[:10]

    total_tickets = len(tickets)
    urgent_tickets = sum(1 for ticket in tickets if ticket["priority"] == "Urgent")
    high_tickets = sum(1 for ticket in tickets if ticket["priority"] == "High")
    medium_tickets = sum(1 for ticket in tickets if ticket["priority"] == "Medium")
    low_tickets = sum(1 for ticket in tickets if ticket["priority"] == "Low")

    open_tickets = sum(1 for ticket in tickets if ticket["status"] == "Open")
    in_progress_tickets = sum(1 for ticket in tickets if ticket["status"] == "In Progress")
    resolved_tickets = sum(1 for ticket in tickets if ticket["status"] == "Resolved")

    priority_counts = {
        "Urgent": urgent_tickets,
        "High": high_tickets,
        "Medium": medium_tickets,
        "Low": low_tickets
    }

    category_counts = Counter(ticket["category"] for ticket in tickets)

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
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if status in ["Open", "In Progress", "Resolved"]:
                ticket["status"] = status
            break

    return redirect(url_for("dashboard"))


@app.route("/delete-ticket/<int:ticket_id>")
def delete_ticket(ticket_id):
    global tickets

    tickets = [
        ticket for ticket in tickets
        if ticket["id"] != ticket_id
    ]

    return redirect(url_for("dashboard"))


@app.route("/export")
def export_tickets():
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
            ticket["id"],
            ticket["message"],
            ticket["category"],
            ticket["priority"],
            ticket["team"],
            ticket["reply"],
            ticket["status"],
            ticket["created_at"]
        ])

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=helpdesk_tickets.csv"

    return response


@app.route("/health")
def health():
    return "HelpDesk Case Assistant is running."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
