from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/ecopulp'
db = SQLAlchemy(app)


class paper(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    instituteName = db.Column(db.String, nullable=False)
    instituteCode = db.Column(db.String, nullable=False)
    instituteEmail = db.Column(db.String, nullable=False)
    areacode = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    studentNumber = db.Column(db.Integer, nullable=False)
    address1 = db.Column(db.String, nullable=False)
    address2 = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)


class contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    areacode = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)


class purchasedata(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    notebook = db.Column(db.String, nullable=False)
    idcard = db.Column(db.String, nullable=False)
    diary = db.Column(db.String, nullable=False)
    clearbag = db.Column(db.String, nullable=False)
    area = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)


class stock(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    totalAmount = db.Column(db.Integer, nullable=False)
    soldAmount = db.Column(db.Integer, nullable=False)
    currentAmount = db.Column(db.Integer, nullable=False)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/buyer")
def buyer():
    return render_template('buyer.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/bill", methods=['POST', 'GET'])
def bill():
    price = {
        'notebook': 60,
        'diary': 110,
        'clearbag': 30,
        'idcard': 35,
    }
    if request.method == "POST":
        name = request.form.get('name')
        phone = request.form.get('phone')

        name = request.form.get('name')
        notebook = int(request.form.get('notebook'))
        idcard = int(request.form.get('idcard'))
        diary = int(request.form.get('diary'))
        clearbag = int(request.form.get('clearbag'))
        area = request.form.get('area')
        city = request.form.get('city')
        state = request.form.get('state')
        postcode = request.form.get('postcode')

        totalcost = int(notebook) * price["notebook"] + int(diary) * price["diary"] + int(
            clearbag) * price["clearbag"] + int(idcard) * price["idcard"]
        entry = purchasedata(name=name, phone=phone, notebook=notebook, diary=diary, clearbag=clearbag, idcard=idcard,
                             area=area, city=city, state=state, code=postcode, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        data = [[notebook, price['notebook'], notebook*price['notebook']],
                [diary, price['diary'], diary*price['diary']],
                [clearbag, price['clearbag'], clearbag*price['clearbag']],
                [idcard, price['idcard'], idcard*price['idcard']],
                [totalcost],
                [name],
                [str(area+","+city)],
                [str(state+","+postcode)],
                [datetime.now().strftime("%x")]
                ]

    return render_template('bill.html', data=data)


@app.route("/seller", methods=['POST', 'GET'])
def seller():
    if request.method == "POST":
        instituteName = request.form.get('instituteName')
        instituteCode = request.form.get('instituteCode')
        instituteEmail = request.form.get('instituteEmail')
        areacode = request.form.get('areacode')
        phone = request.form.get('phone')
        studentNumber = request.form.get('studentNumber')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        entry = paper(instituteName=instituteName, instituteCode=instituteCode,
                      instituteEmail=instituteEmail, areacode=areacode, phone=phone,
                      studentNumber=studentNumber, address1=address1, address2=address2,
                      date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('seller.html')   


@app.route("/achievement")
def achievement():
    data=[000,000,000,000]
    return render_template('achievement.html',data=data)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        areacode = request.form.get('areacode')
        phone = request.form.get('phone')
        msg = request.form.get('msg')

        entry = contacts(fname=fname, lname=lname, email=email, areacode=areacode,
                         phone=phone, date=datetime.now(), message=msg)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
