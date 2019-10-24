"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, redirect

import hackbright

app = Flask(__name__)

app.secret_key = "this-can-be-anything"


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    project_info = hackbright.get_grade_by_github(github)

    html = render_template("student_info.html", 
                            first=first, 
                            last=last,
                            github=github,
                            project_info=project_info)

    return html

@app.route("/student_search")
def search_students():
    """Show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/student_add")
def add_student():
    """Show form for adding a student"""

    return render_template("student_add.html")


@app.route("/student-add-db", methods=['POST'])
def update_student_db():
    """Update the DB for the new student"""
   
    first_name = request.form.get('first_name') 
    last_name = request.form.get('last_name')
    github = request.form.get('github')


    QUERY = """
        INSERT INTO students (first_name, last_name, github)
            VALUES (:first_name, :last_name, :github)
        """

    hackbright.db.session.execute(QUERY, {'first_name': first_name, 'last_name': last_name,
                                'github': github})

    hackbright.db.session.commit()

    # flash(f"Successfully added {first_name} {last_name} to the DB. Go to <a href='http://www.google.com'>Google!</a>")

    return render_template('student_confirmation.html', first_name=first_name, 
                            last_name=last_name,
                            github=github)

@app.route("/project")
def show_project():

    # psuedocode: from the student profile page, there will be a link to project
    # the project page needs to know which project to display
    # so that we can call the get_project_by_title function
    # and send those values from the query to a jinja template

    project_title = request.args.get('project_title')

    title, description, max_grade = hackbright.get_project_by_title(project_title)



    return render_template("project_info.html",
                            title=title,
                            description=description,
                            max_grade=max_grade)




if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
