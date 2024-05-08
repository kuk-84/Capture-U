from flask import Flask, render_template, url_for,request,redirect
from werkzeug.utils import secure_filename
import sql
import os
import facerecog
app=Flask(__name__)
os.makedirs(os.path.join(app.instance_path, 'images'), exist_ok=True)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/generate', methods=['GET','POST'])
def generate():
    if request.method != 'POST':
        return render_template('generate.html')
    subject=request.form['subject']
    sql.printdata(subject)
    return redirect(url_for('index'))

@app.route('/new_student', methods=['GET','POST'])
def new_student():
    if request.method != 'POST':
        return render_template('new_student.html')
    enroll=request.form['enroll']
    name=request.form['name']
    batch=request.form['batch']
    f = request.files['file']
    f.filename=f"{enroll}.jpeg"
    f.save(os.path.join(app.instance_path, 'images',secure_filename(f.filename)))
    sql.insert_students(enroll,name,batch)
    return redirect(url_for('index'))

@app.route('/classes', methods=['GET','POST'])
def classes():
    if request.method != 'POST':
        return render_template('class.html')

    subject=request.form['subject']
    date=request.form['date']

    if request.form['button'] == 'TA':
        sql.addcolumn(subject,date)
        facerecog.run(subject,date)
        return redirect(url_for('generate'))
    elif request.form['button']=='NS':
        return redirect(url_for('new_student'))


@app.route('/authent', methods=['GET','POST'])
def authent():
    if request.method != 'POST':
        return render_template('authent.html')
    email=request.form['email']
    pas=request.form['password']
    ff=sql.check_teachers(email, pas)
    if ff==1:
        return redirect(url_for('classes'))
  



if __name__=='__main__':
    app.run(debug=True)