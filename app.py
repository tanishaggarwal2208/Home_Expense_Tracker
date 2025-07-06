from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database setup
def init_db():
    if not os.path.exists("expenses.db"):
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# Home Page - View all expenses
@app.route("/")
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    total = sum([row[2] for row in expenses])
    conn.close()
    return render_template("index.html", expenses=expenses, total=total)

# Add Expense Page
@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        title = request.form["title"]
        amount = float(request.form["amount"])
        date = request.form["date"]

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)", (title, amount, date))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_expense.html")

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
