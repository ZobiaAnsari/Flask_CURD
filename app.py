from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import openpyxl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///parsing.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db = SQLAlchemy(app)

class parsing(db.Model):
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer())



@app.route('/',methods = ['POST'])
def pras():
    data = request.files['file']
    workbook = openpyxl.load_workbook(data)
    print(workbook)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=True, values_only = True):
        name, age = row
        data2 = parsing(name = name, age=age)
        db.session.add(data2)
        db.session.commit()

    return ('msg : uploaded')
    
@app.route('/create',methods = ['POST'])
def add():
    if request.method == 'POST':
        name = request.json['name']
        age = request.json['age']
        new_user = parsing(name = name, age=age)
        db.session.add(new_user)
        db.session.commit()

    return ('data added')
    

@app.route('/update', methods = ['PUT'])
def update():
    if request.method == 'PUT':
        id= request.json['id']
        name = request.json['name']
        par = parsing.query.filter_by(id=id).first()
        par.name = name
        db.session.add(par)
        db.session.commit()
    return ('data : modified')


@app.route('/delete', methods = ['DELETE'])
def delete():
    if request.method == 'DELETE':
        id= request.json['id']
        par = parsing.query.filter_by(id=id).first()
        db.session.delete(par)
        db.session.commit()
    return ('data : deleted')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug= True)