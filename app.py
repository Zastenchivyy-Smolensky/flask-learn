from flask import Flask,render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///employee.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    name = db.Column(db.String(255))  # 社員名
    mail = db.Column(db.String(255))  # メール
    is_remote = db.Column(db.Boolean)  # リモート勤務しているか
    department = db.Column(db.String(255))  # 部署
    year = db.Column(db.Integer, default=0)  # 社歴
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

@app.route("/")

def index():
    my_dict = {
        'insert_something1': 'views.pyのinsert_something1部分です。',
        'insert_something2': 'views.pyのinsert_something2部分です。',
        'test_titles': ['title1', 'title2', 'title3']
    }
    return render_template("index.html", my_dict=my_dict)

@app.route("/test")
def index1():
    return render_template("index2.html")

@app.route("/sampleform")
def sample_form():
    return render_template("sampleform.html")

@app.route('/sampleform-post', methods=['POST'])
def sample_form_temp():
    print('POSTデータ受け取ったので処理します')
    req1 = request.form['data1']

    return f'POST受け取ったよ: {req1}'

@app.route("/add_employee", methods=["GET","POST"])

def add_employee():
    if request.method == "GET":
        return render_template("add_employee.html")
    if request.method == "POST":
        form_name = request.form.get("name")
        form_mail = request.form.get("mail")
        form_is_remote = request.form.get('is_remote', default=False, type=bool)
        form_department = request.form.get('department')
        form_year = request.form.get("year", default=0, type=int)

        employee = Employee(
            name=form_name,
            mail=form_mail,
            is_remote=form_is_remote,
            department=form_department,
            year=form_year
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('index'))
        
@app.route('/employees')
def employee_list():
    employees = Employee.query.all()
    return render_template('employee_list.html', employees=employees)

@app.route("/employees/<int:id>")
def employee_detail(id):
    employee = Employee.query.get(id)
    return render_template("employee_detail.html", employee=employee)
@app.route('/employees/<int:id>/edit', methods=['GET'])
def employee_edit(id):
    employee = Employee.query.get(id)
    return render_template('employee_edit.html', employee=employee)

@app.route('/employees/<int:id>/update', methods=['POST'])
def employee_update(id):
    employee = Employee.query.get(id)  # 更新するデータをDBから取得
    employee.name = request.form.get('name')
    employee.mail = request.form.get('mail')
    employee.is_remote = request.form.get('is_remote', default=False, type=bool)
    employee.department = request.form.get('department')
    employee.year = request.form.get('year', default=0, type=int)

    db.session.merge(employee)
    db.session.commit()
    return redirect(url_for('employee_list'))

@app.route('/employees/<int:id>/delete', methods=['POST'])  
def employee_delete(id):  
    employee = Employee.query.get(id)   
    db.session.delete(employee)  
    db.session.commit()  
    return redirect(url_for('employee_list'))