from flask import Flask, request, redirect, url_for, render_template
import todo_manager

app = Flask(__name__)

@app.route('/')
def home():
    tasks = todo_manager.load_tasks()
    return render_template('home.html', tasks=tasks)

@app.route('/view')
def view():
    tasks = todo_manager.load_tasks()
    html = "<h2>📋 Your Tasks:</h2><ul>"
    for i, task in enumerate(tasks):
        status = "✅" if task["completed"] else "❌"
        html += f"<li>{i+1}. {status} {task['description']} (Due: {task['due_date']}) [Priority: {task['priority'].capitalize()}]</li>"
    html += "</ul><br><a href='/'>⬅ Back</a>"
    return html

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]
        task = {
            "description": description,
            "due_date": due_date,
            "completed": False,
            "priority": priority
        }
        tasks = todo_manager.load_tasks()
        tasks.append(task)
        todo_manager.save_tasks(tasks)
        return redirect(url_for("view"))

    return """
    <h2>➕ Add New Task</h2>
    <form method="POST">
        Description: <input type="text" name="description"><br>
        Due Date (YYYY-MM-DD): <input type="text" name="due_date"><br>
        Priority: 
        <select name="priority">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
        </select><br><br>
        <input type="submit" value="Add Task">
    </form><br><a href='/'>⬅ Back</a>
    """

@app.route('/delete_task', methods=["GET", "POST"])
def delete_task():
    tasks = todo_manager.load_tasks()
    if request.method == "POST":
        index = int(request.form["index"])
        if 0 <= index < len(tasks):
            tasks.pop(index)
            todo_manager.save_tasks(tasks)
        return redirect(url_for("view"))

    form = '<h2>🗑️ Delete Task</h2><form method="POST">'
    form += '<select name="index">'
    for i, task in enumerate(tasks):
        form += f'<option value="{i}">{i+1}. {task["description"]}</option>'
    form += '</select><br><br>'
    form += '<input type="submit" value="Delete Task"></form>'
    form += "<br><a href='/'>⬅ Back</a>"
    return form

@app.route('/mark_completed', methods=["GET", "POST"])
def mark_completed():
    tasks = todo_manager.load_tasks()
    if request.method == "POST":
        index = int(request.form["index"])
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            todo_manager.save_tasks(tasks)
        return redirect(url_for("view"))

    form = '<h2>✅ Mark Task as Completed</h2><form method="POST">'
    form += '<select name="index">'
    for i, task in enumerate(tasks):
        if not task["completed"]:
            form += f'<option value="{i}">{i+1}. {task["description"]}</option>'
    form += '</select><br><br>'
    form += '<input type="submit" value="Mark Completed"></form>'
    form += "<br><a href='/'>⬅ Back</a>"
    return form

if __name__ == "__main__":
    app.run(debug=True)
